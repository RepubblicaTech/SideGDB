"""
Some useful macro-widgets for common components for SideGDB
"""

from io import SEEK_SET
from math import floor
import os
from pathlib import Path
from PySide6 import QtCore
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QPalette, QResizeEvent
from PySide6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QTextBrowser, QVBoxLayout, QWidget
from loguru import logger
from enum import Enum

class QDirectionFlag(Enum):
    QHorizontal = 0
    QVertical = 1

class QLabeledLineEdit(QWidget):
    def __init__(self, direction: QDirectionFlag, labelText: str, parent: QWidget | None = None, placeholderText: str = ""):
        super().__init__(parent)

        match direction:
            case QDirectionFlag.QHorizontal:
                layout = QHBoxLayout(self)
            case QDirectionFlag.QVertical:
                layout = QVBoxLayout(self)
            case _:
                raise ValueError("Invalid direction flag (there are only two directions how can you get this wrong lol, go read the manual), got " + direction)

        self.__input = QLineEdit(placeholderText=placeholderText)
        layout.addWidget(QLabel(labelText))
        layout.addWidget(self.__input)

        self.setLayout(layout)

    def inputText(self):
        return self.__input.text()

class QPathChoose(QWidget):
    def __init__(self, fileMode: QFileDialog.FileMode, filter: str = "", parent: QWidget | None = None, sideText: str = "Path:", lineEditPlaceholder: str = ""):
        super().__init__(parent)

        gridLayout = QGridLayout()

        self.sideLabel = QLabel(sideText)
        self.pathLine = QLineEdit(placeholderText=lineEditPlaceholder)
        self.choosePathButton = QPushButton("...")

        gridLayout.addWidget(self.sideLabel, 0, 0)
        gridLayout.addWidget(self.pathLine, 0, 1)
        gridLayout.addWidget(self.choosePathButton, 0, 2)

        self.setLayout(gridLayout)

        self.__fileDialog = QFileDialog(filter=filter)
        self.__fileDialog.setFileMode(fileMode)
        self.pathLine.setReadOnly(True)
        self.choosePathButton.clicked.connect(self.__spawnOpenDialog)

    @QtCore.Slot()
    def __spawnOpenDialog(self):
        logger.debug("huh?")
        match (self.__fileDialog.fileMode()):
            case QFileDialog.FileMode.ExistingFile | QFileDialog.FileMode.ExistingFiles:
                chosenFile = self.__fileDialog.getOpenFileName(self, f"Open {self.sideLabel.text()}", dir=os.getcwd())
                self.pathLine.setText(chosenFile[0])
            case QFileDialog.FileMode.Directory:
                chosenDir = self.__fileDialog.getExistingDirectory(self, "Select", os.getcwd(), QFileDialog.Option.ShowDirsOnly)
                self.pathLine.setText(chosenDir)

    def chosenPath(self):
        return self.pathLine.text()

class Resettable:
    def sgReset(self):
        raise NotImplementedError("This function should be overridden!")

class Updateable:
    def sgUpdate(self, frame: dict):
        raise NotImplementedError("This function should be overridden!")

class QSourceWidget(QWidget, Resettable):
    BAR_BASEW = 40
    BAR_RPADD = 10
    BAR_BPADD = 50

    def __init__(self):
        self.currentSource = ""
        self.lines = 0
        self.lineToHighlight = 0

        super().__init__()

    @staticmethod
    def digits(n):
        d = 1
        while (n >= 10):
            n /= 10
            d += 1
        return d

    def barWidth(self):
        return self.BAR_BASEW + (self.fontMetrics().horizontalAdvance("9") * self.digits(self.lines)) + self.BAR_RPADD

    def barHeight(self):
        return self.BAR_BPADD + (self.fontMetrics().height() * self.lines)

    def loadSource(self, path: str):
        if (path == self.currentSource or not path or not Path(path).exists()):
            return

        self.currentSource = path
        f = open(path)
        self.lines = len(f.readlines())

        f.seek(0, SEEK_SET)
        maxLineLength = 0
        for line in f.readlines():
            if (len(line) > maxLineLength):
                maxLineLength = len(line)
        f.close()

        self.setMinimumHeight(self.barHeight())
        self.setMinimumWidth(self.barWidth() + (self.fontMetrics().horizontalAdvance("9") * maxLineLength))

        self.update()

    def highlightLine(self, line: int):
        if (line < 0 or line > self.lines):
            return

        self.lineToHighlight = line
        self.update()

    def paintEvent(self, e: QPaintEvent, /) -> None:
        if (not self.currentSource):
            return

        painter = QPainter(self)

        painter.fillRect(0, 0, self.width(), self.height(), self.palette().color(QPalette.ColorRole.Base))
        barRect = QRect(0, 0, self.barWidth(), self.barHeight())
        painter.fillRect(barRect, self.palette().color(QPalette.ColorRole.AlternateBase))

        f = open(self.currentSource)
        for i in range(self.lines):
            painter.drawText(self.barWidth() - (self.fontMetrics().horizontalAdvance("9") * self.digits(i + 1)) - self.BAR_RPADD,
                             self.fontMetrics().height() * (i + 1),
                             str(i + 1))
            if (i + 1 == self.lineToHighlight):
                painter.fillRect(self.barWidth(),
                                 self.fontMetrics().height() * i,
                                 self.width(),
                                 self.fontMetrics().lineSpacing(),
                                 self.palette().color(QPalette.ColorRole.Accent))
            painter.drawText(self.barWidth(), self.fontMetrics().height() * (i + 1), f.readline())
        f.close()

        painter.end()
        return super().paintEvent(e)

    def sgReset(self):
        self.currentSource = ""
        self.lines = 0
        self.lineToHighlight = 0

        self.update()

class QCodeArea(QScrollArea, Resettable):
    def __init__(self):
        self.firstLine = 0  # first line on screen
        self.linesOnScreen = 0

        super().__init__()

        self.sourceWidget = QSourceWidget()
        self.setWidget(self.sourceWidget)
        self.setWidgetResizable(True)

    def loadSource(self, path: str):
        self.sourceWidget.loadSource(path)

    def highlightLine(self, line: int):
        self.sourceWidget.highlightLine(line)

    def scrollTo(self, line: int):
        if (line >= self.firstLine and line <= self.firstLine + self.linesOnScreen):
            return

        firstLine = floor(line - (self.linesOnScreen / 2))
        if (firstLine < 1):
            firstLine = 1

        self.verticalScrollBar().setValue(firstLine * self.viewport().fontMetrics().height())

    def scrollContentsBy(self, dx: int, dy: int, /) -> None:
        self.firstLine = self.firstLine - floor(dy / self.viewport().fontMetrics().height())
        return super().scrollContentsBy(dx, dy)

    def resizeEvent(self, arg__1: QResizeEvent, /) -> None:
        self.linesOnScreen = floor(self.viewport().height() / self.viewport().fontMetrics().height())
        return super().resizeEvent(arg__1)

    def sgReset(self):
        self.firstLine = 0
        self.linesOnScreen = 0

        self.sourceWidget.sgReset()
        self.update()

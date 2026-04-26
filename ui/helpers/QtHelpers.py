"""
Some useful macro-widgets for common components for SideGDB
"""

from math import floor
import os
from pathlib import Path
import traceback
from PySide6 import QtCore
from PySide6.QtCore import QEvent, QPoint, QRect, Qt
from PySide6.QtGui import QHoverEvent, QPaintEvent, QPainter, QPalette, QResizeEvent
from PySide6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget
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
    def reset(self):
        raise NotImplementedError("This function should be overridden!")

class Updateable:
    def sgUpdate(self, frame: dict):
        raise NotImplementedError("This function should be overridden!")

class QCodeBrowser(QWidget):
    LOCBAR_W_BASE = 40
    LOCBAR_RMARGIN = 8
    LOCBAR_BMARGIN = 50
    LOCBAR_MINMARGIN = 4
    BCIRCLE_RAD = 4

    def __init__(self, parent: QWidget | None = None):
        self.__loc = 0
        self.__currentSource = ""     # File we are showing on screen
        self.__currentLine = 0
        self.__highlightedLine = 0

        self.OverLOCBar = False

        super().__init__(parent)

    def loc(self):
        return self.__loc

    # the height of ONLY the lines, excluding the bottom margin
    def locBarHeight(self):
        return self.__loc * self.fontMetrics().height()

    def locBarWidth(self):
        loc = self.__loc
        digits = 1
        while (loc >= 10):
            digits += 1
            loc /= 10

        return QCodeBrowser.LOCBAR_W_BASE + (self.fontMetrics().horizontalAdvance("9") * digits)

    def maxLineLength(self, path: str):
        file = open(path, "r")

        maxLength = 0
        for line in file.readlines():
            if (len(line) > maxLength):
                maxLength = len(line)

        return self.fontMetrics().horizontalAdvance("W") * maxLength

    def loadFile(self, absPath: str):
        if (self.__currentSource == absPath or not(Path(absPath).exists)):
            return

        self.__currentSource = absPath
        file = open(self.__currentSource, "r")
        self.__loc = len(file.readlines())
        logger.debug(f"LOC: {self.__loc}")
        self.setMinimumWidth(self.locBarWidth() + self.maxLineLength(self.__currentSource))
        self.setMinimumHeight(self.locBarHeight() + QCodeBrowser.LOCBAR_BMARGIN)
        file.close()

        self.update()

    def highlightLine(self, line: int):
        logger.debug(f"Highlight {line}")
        if (line > self.__loc):
            return

        self.__highlightedLine = line

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        locBar = QRect(0, 0, self.locBarWidth(), self.locBarHeight() + QCodeBrowser.LOCBAR_BMARGIN)
        painter.fillRect(self.locBarWidth(), 0, self.width(), self.locBarHeight() + QCodeBrowser.LOCBAR_BMARGIN, self.palette().color(QPalette.ColorRole.Base))
        painter.fillRect(locBar, self.palette().color(QPalette.ColorRole.Mid))

        file = open(self.__currentSource)
        for i in range(self.__loc):
            painter.drawText(QCodeBrowser.LOCBAR_RMARGIN, self.fontMetrics().height() * (i + 1), f"{i + 1}")
            textfromLine = file.readline()
            if (i + 1 == self.__highlightedLine):
                painter.fillRect(self.locBarWidth(),
                                 (self.fontMetrics().height() * i),
                                 self.width(),
                                 self.fontMetrics().lineSpacing(),
                                 self.palette().color(QPalette.ColorRole.Accent))
            painter.drawText(self.locBarWidth(), self.fontMetrics().height() * (i + 1), textfromLine)

        painter.end()

class QCodeArea(QScrollArea):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.__codeBrowser = QCodeBrowser()
        self.setWidget(self.__codeBrowser)

        self.firstLineOnScreen = 1
        self.linesOnScreen = floor(self.height() / self.__codeBrowser.fontMetrics().height())

    def codeBrowser(self):
        return self.__codeBrowser

    def scrollTo(self, line):
        logger.debug(f"Line to display: {line}")
        logger.debug(f"Lines on screen: {self.firstLineOnScreen}-{self.firstLineOnScreen + self.linesOnScreen}")
        if (line > self.firstLineOnScreen and line < self.firstLineOnScreen + self.linesOnScreen):
            return

        fontHeight = self.__codeBrowser.fontMetrics().height()
        self.firstLineOnScreen = floor(line - (self.linesOnScreen / 2))
        logger.debug(f"First line to show: {self.firstLineOnScreen}")
        if (self.firstLineOnScreen < 1):
            self.firstLineOnScreen = 1

        self.verticalScrollBar().setValue(self.firstLineOnScreen * fontHeight)

    def loadFile(self, absPath: str):
        self.__codeBrowser.loadFile(absPath)
        self.firstLineOnScreen = 1

    def resizeEvent(self, event: QResizeEvent):
        vsb = self.verticalScrollBar()
        hsb = self.horizontalScrollBar()

        content_height = self.__codeBrowser.height()
        viewport_h = self.viewport().height()

        # Range: [0, contentHeight - viewportHeight]
        vsb.setPageStep(viewport_h)
        vsb.setRange(0, max(0, content_height - viewport_h))
        hsb.setRange(0, 0)

        self.linesOnScreen = floor(self.height() / self.__codeBrowser.fontMetrics().height())

        super().resizeEvent(event)

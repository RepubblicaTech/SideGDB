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

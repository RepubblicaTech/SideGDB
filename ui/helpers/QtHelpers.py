"""
Some useful macro-widgets for common components for SideGDB
"""

from enum import Enum
import os
from stat import filemode
from PySide6 import QtCore, QtWidgets
from loguru import logger

class QDirectionFlag(Enum):
    QHorizontal = 0
    QVertical = 1

class QLabeledLineEdit(QtWidgets.QWidget):
    def __init__(self, direction: QDirectionFlag, labelText: str, parent: QtWidgets.QWidget | None = None, placeholderText: str = ""):
        super().__init__(parent)

        match direction:
            case QDirectionFlag.QHorizontal:
                layout = QtWidgets.QHBoxLayout(self)
            case QDirectionFlag.QVertical:
                layout = QtWidgets.QVBoxLayout(self)
            case _:
                raise ValueError("Invalid direction flag (there are only two directions how can you get this wrong lol, go read the manual), got " + direction)


        self.__input = QtWidgets.QLineEdit(placeholderText=placeholderText)
        layout.addWidget(QtWidgets.QLabel(labelText))
        layout.addWidget(self.__input)

        self.setLayout(layout)

    def inputText(self):
        return self.__input.text()

class QPathChoose(QtWidgets.QWidget):
    def __init__(self, fileMode: QtWidgets.QFileDialog.FileMode, filter: str = "", parent: QtWidgets.QWidget | None = None, sideText: str = "Path:", lineEditPlaceholder: str = ""):
        super().__init__(parent)

        gridLayout = QtWidgets.QGridLayout()

        self.sideLabel = QtWidgets.QLabel(sideText)
        self.pathLine = QtWidgets.QLineEdit(placeholderText=lineEditPlaceholder)
        self.choosePathButton = QtWidgets.QPushButton("...")

        gridLayout.addWidget(self.sideLabel, 0, 0)
        gridLayout.addWidget(self.pathLine, 0, 1)
        gridLayout.addWidget(self.choosePathButton, 0, 2)

        self.setLayout(gridLayout)

        self.__fileDialog = QtWidgets.QFileDialog(filter=filter)
        self.__fileDialog.setFileMode(fileMode)
        self.pathLine.setReadOnly(True)
        self.choosePathButton.clicked.connect(self.__spawnOpenDialog)

    @QtCore.Slot()
    def __spawnOpenDialog(self):
        logger.debug("huh?")
        match (self.__fileDialog.fileMode()):
            case QtWidgets.QFileDialog.FileMode.ExistingFile | QtWidgets.QFileDialog.FileMode.ExistingFiles:
                chosenFile = self.__fileDialog.getOpenFileName(self, f"Open {self.sideLabel.text()}", dir=os.getcwd())
                self.pathLine.setText(chosenFile[0])
            case QtWidgets.QFileDialog.FileMode.Directory:
                chosenDir = self.__fileDialog.getExistingDirectory(self, "Select", os.getcwd(), QtWidgets.QFileDialog.Option.ShowDirsOnly)
                self.pathLine.setText(chosenDir)

    def chosenPath(self):
        return self.pathLine.text()

class Resettable:
    def reset(self):
        raise NotImplementedError("This function should be overridden!")

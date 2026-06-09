from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QDialog, QGridLayout, QLineEdit, QMessageBox, QPushButton, QTableView, QWidget
from loguru import logger

from backend.SideModel import SideModel

class BreakManager(QDialog):
    def __init__(self, parent: QWidget, model: SideModel):
        self.model = model
        super().__init__(parent)
        self.resize(600, 400)
        layout = QGridLayout()

        self.symbolInput = QLineEdit(placeholderText="Type a function or *address...")
        self.insertButton = QPushButton("Insert")
        self.table = QTableView()
        self.table.setModel(self.model.breakpointsStandardModel)
        self.deleteButton = QPushButton("DELETE selected breakpoint")

        layout.addWidget(self.symbolInput, 0, 0, 1, 1)
        layout.addWidget(self.insertButton, 0, 1, 1, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(self.deleteButton, 2, 0, 1, 2)

        self.setLayout(layout)

        self.insertButton.clicked.connect(self.sendInsertBreakpoint)
        self.deleteButton.clicked.connect(self.deleteSelectedBreakpoint)

    def deleteSelectedBreakpoint(self):
        selectedIndexes = self.table.selectionModel().selectedIndexes()
        for index in selectedIndexes:
            if (not index.isValid()):
                logger.warning(f"Index {str(index)} is invalid.")
                return

            row = index.row()
            breakpointNumber = int(self.model.breakpointsStandardModel.data(self.model.breakpointsStandardModel.index(row, 0)))
            response = self.model.deleteBreakpoint(breakpointNumber)
            if (response[0]["message"] != "done"):
                logger.warning(f"Couldn't delete breakpoint {breakpointNumber}: {response[0]["payload"]}".strip("\n"))
                continue
            logger.debug(f"Breakpoint {breakpointNumber} deleted.")

    def sendInsertBreakpoint(self):
        symbol = self.symbolInput.text()
        if (not symbol):
            return

        self.model.setBreakpoint(symbol)    # table model gets updated in here
        self.table.resizeColumnsToContents()

        self.symbolInput.setText("")

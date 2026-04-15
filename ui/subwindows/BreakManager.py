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

        self.symbolBreakpoint = QLineEdit(placeholderText="Type a function or *address...")
        self.insertButton = QPushButton("Insert")
        self.table = QTableView()
        self.deleteButton = QPushButton("DELETE selected breakpoint")

        self.model.breakpointsStandardModel.setHorizontalHeaderLabels(["No.", "Where[file:line]"])
        self.table.setModel(self.model.breakpointsStandardModel)
        self.table.resizeColumnsToContents()

        layout.addWidget(self.symbolBreakpoint, 0, 0, 1, 1)
        layout.addWidget(self.insertButton, 0, 1, 1, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(self.deleteButton, 2, 0, 1, 2)

        self.statusTip().__init__()

        self.setLayout(layout)

        self.model.loadBreakpointsListToModel()
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
            self.model.breakpointsStandardModel.removeRow(row)
            logger.debug(f"Breakpoint {breakpointNumber} deleted.")

    def sendInsertBreakpoint(self):
        symbol = self.symbolBreakpoint.text()
        if (not symbol):
            return

        try:
            breakpoint = self.model.setBreakpoint(symbol)
        except Exception as e:
            logger.error(f"Couldn't set breakpoint: {str(e)}")
            QMessageBox(QMessageBox.Icon.Critical, "Breakpoint error", f"Couldn't set breakpoint: {str(e)}", QMessageBox.StandardButton.Ok).exec()
            return

        if (not breakpoint):
            return

        bNumber = breakpoint.get("number")
        where = breakpoint.get("addr")
        if (breakpoint.get("where")):
            where = breakpoint.get("where")
        file = breakpoint.get("source")
        line = breakpoint.get("line")

        locationStr = str(where)
        if (file or line):
            locationStr += f"[{str(file) if file else "/???.?"}:{str(line) if line else "XX"}]"

        c1 = QStandardItem(str(bNumber))
        c2 = QStandardItem(locationStr)
        self.model.breakpointsStandardModel.appendRow([c1, c2])

        self.table.resizeColumnsToContents()

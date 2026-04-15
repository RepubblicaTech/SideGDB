from PySide6.QtWidgets import QDialog, QGridLayout, QLineEdit, QPushButton, QTableView, QWidget

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

        self.table.setModel(self.model.breakpointsStandardModel)
        self.table.resizeColumnsToContents()
        self.table.hideRow(0)

        layout.addWidget(self.symbolBreakpoint, 0, 0, 1, 1)
        layout.addWidget(self.insertButton, 0, 1, 1, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(self.deleteButton, 2, 0, 1, 2)

        self.setLayout(layout)

        self.model.loadBreakpointsListToModel()
        self.symbolBreakpoint.returnPressed.connect(self.sendInsertBreakpoint)

    def sendInsertBreakpoint(self):
        symbol = self.symbolBreakpoint.text()
        if (not symbol):
            return

        response = self.model.setBreakpoint(symbol)

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

class RightView(QtWidgets.QMdiSubWindow):
    def __init__(self, /, parent: QtWidgets.QWidget | None):
        super().__init__(parent)

        self.setWindowTitle("Variables and registers")
        self.resize(200, 600)

        self.tabView = QtWidgets.QTabWidget()

        self.tabView.addTab(QtWidgets.QWidget(), "Variables")
        self.tabView.addTab(QtWidgets.QWidget(), "Registers")

        self.setWidget(self.tabView)

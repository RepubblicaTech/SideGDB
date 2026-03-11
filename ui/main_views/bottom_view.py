from PySide6 import QtWidgets
from PySide6.QtCore import Qt

class BottomView(QtWidgets.QMdiSubWindow):
    def __init__(self, /, parent: QtWidgets.QWidget | None):
        super().__init__(parent)

        self.setWindowTitle("Memory and GDB output")
        self.resize(400, 400)

        self.tabView = QtWidgets.QTabWidget()

        self.tabView.addTab(QtWidgets.QWidget(), "Memory")
        self.tabView.addTab(QtWidgets.QWidget(), "GDB Console")

        self.setWidget(self.tabView)

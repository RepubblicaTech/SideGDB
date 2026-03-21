from PySide6 import QtWidgets

class GDBConsoleView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.gdbOutput = QtWidgets.QTextEdit(readOnly=True)
        self.gdbPrompt = QtWidgets.QLineEdit(placeholderText="Type any GDB command here (-thread-info)...")

        layout.addWidget(self.gdbOutput)
        layout.addWidget(self.gdbPrompt)

        self.setLayout(layout)

class BottomView(QtWidgets.QMdiSubWindow):
    def __init__(self, /, parent: QtWidgets.QWidget | None):
        super().__init__(parent)

        self.setWindowTitle("Memory and GDB output")
        self.resize(400, 400)

        self.tabView = QtWidgets.QTabWidget()

        self.tabView.addTab(QtWidgets.QWidget(), "Memory")
        self.gdbConsoleWidget = GDBConsoleView()
        self.tabView.addTab(self.gdbConsoleWidget, "GDB Console")

        self.setWidget(self.tabView)

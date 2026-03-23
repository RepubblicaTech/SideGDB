from PySide6 import QtWidgets

class GDBConsoleView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.gdbOutput = QtWidgets.QTextEdit(readOnly=True)

        gdbInputWidget = QtWidgets.QWidget()
        gdbInputLayout = QtWidgets.QHBoxLayout()

        self.gdbPrompt = QtWidgets.QLineEdit(placeholderText="Type any GDB command here (-thread-info)...")
        self.sendButton = QtWidgets.QPushButton("Send")

        gdbInputLayout.addWidget(self.gdbPrompt)
        gdbInputLayout.addWidget(self.sendButton)

        gdbInputWidget.setLayout(gdbInputLayout)

        layout.addWidget(self.gdbOutput)
        layout.addWidget(gdbInputWidget)

        self.setLayout(layout)

class BottomView(QtWidgets.QMdiSubWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory and GDB output")
        self.resize(400, 400)

        self.tabView = QtWidgets.QTabWidget()

        self.tabView.addTab(QtWidgets.QWidget(), "Memory")
        self.gdbConsoleView = GDBConsoleView()
        self.tabView.addTab(self.gdbConsoleView, "GDB Console")

        self.setWidget(self.tabView)

    def gdbPromptInput(self):
        return self.gdbConsoleView.gdbPrompt.text()

    def appendToGdbOut(self, text: str):
        self.gdbConsoleView.gdbOutput.append(text)

    def gdbSendButton(self):
        return self.gdbConsoleView.sendButton

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

testTest = r"""// THIS IS JUST A PLACEHOLDER NOT A REAL PROGRAM
#include <stdio.h>

int main() {
    printf("Hello World!\n");
    return 0;
}"""

class CodeDebugView(QtWidgets.QMdiSubWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code")
        self.resize(600, 400)

        self.splitter = QtWidgets.QSplitter(Qt.Orientation.Horizontal)

        self.textView = QtWidgets.QTextEdit()
        self.textView.setText(testTest)

        self.gdbButtonsWidget = QtWidgets.QWidget()
        self.gdbButtons = QtWidgets.QVBoxLayout(self.gdbButtonsWidget)
        self.gdbButtons.addWidget(QtWidgets.QPushButton("Continue"))
        self.gdbButtons.addWidget(QtWidgets.QPushButton("Step Over"))
        self.gdbButtons.addWidget(QtWidgets.QPushButton("Step Into"))
        self.gdbButtons.addStretch()

        self.splitter.addWidget(self.textView)
        self.splitter.addWidget(self.gdbButtonsWidget)
        self.splitter.setSizes([500, 100])

        self.setWidget(self.splitter)

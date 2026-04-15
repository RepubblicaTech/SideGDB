from pprint import pformat
from typing import List

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette, Qt

from backend.MIResponseManager import MIPromptManager
from backend.SideModel import SideModel
from PySide6.QtWidgets import QLineEdit, QTextBrowser, QVBoxLayout, QWidget

class MIPrompt(QWidget):
    def __init__(self, model: SideModel):
        self.canAutoscroll = True
        super().__init__()

        layout = QVBoxLayout()

        self.miPrompt = QLineEdit(placeholderText="Type any GDBMI command in here (-thread-info)")
        self.miOutput = QTextBrowser(self)
        self.miOutput.setPlaceholderText("Responses get printed here")
        self.miOutput.setReadOnly(True)
        self.miOutput.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        layout.addWidget(self.miPrompt)
        layout.addWidget(self.miOutput)

        self.setLayout(layout)

        self.miPrompt.returnPressed.connect(self.sendCommand)

        MIPromptManager.setOutputView(self.miOutput)
        self.model = model
        self.model.read(-1)

    def reset(self):
        self.miPrompt.setText("")
        self.miOutput.setPlainText("")

    def sendCommand(self):
        toSend = self.miPrompt.text()
        scrollbar = self.miOutput.verticalScrollBar()
        atBottom = scrollbar.value() >= scrollbar.maximum() - 10

        if (not toSend):
            return
        print(f"command: {toSend}")
        self.model.send(toSend)

        if atBottom and self.canAutoscroll:
            QTimer.singleShot(0, lambda: scrollbar.setValue(scrollbar.maximum()))

        self.miPrompt.setText("")

from typing import List

from PySide6.QtGui import QPalette, Qt
from loguru import logger

from backend.MIResponseManager import MIPromptManager
from backend.SideModel import SideModel
from PySide6.QtWidgets import QLineEdit, QTextBrowser, QVBoxLayout, QWidget

from ui.QtHelpers import Resettable

class MIPrompt(QWidget, Resettable):
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

        self.model = model
        self.model.miResponseReceived.connectHandler(self.miResponseHandler)
        self.model.read(-1)

    def sgReset(self):
        self.miPrompt.setText("")
        self.miOutput.setPlainText("")

    def sendCommand(self):
        toSend = self.miPrompt.text()
        if (not toSend):
            return

        print(f"command: {toSend}")
        self.model.send(toSend)
        self.miPrompt.setText("")

    def miResponseHandler(self, response: List[dict] | dict):
        if (type(response) is list):
            for r in response:
                self.miResponseHandler(r)
            return
        elif (type(response) is not dict):
            return

        match (response.get("message")):
            case "done":
                self.miOutput.setTextColor("#23c417")
            case "error":
                self.miOutput.setTextColor("#e93e3e")
            case _:
                self.miOutput.setTextColor(self.palette().color(QPalette.ColorRole.Text))

        self.miOutput.insertPlainText(MIPromptManager.formatResponseMessage(response))
        if (response.get("payload", None)):
            self.miOutput.insertPlainText(MIPromptManager.formatResponsePayload(response))

        currentScrollValue = self.miOutput.verticalScrollBar().value()
        currentMaximum = self.miOutput.verticalScrollBar().maximum()
        logger.debug(f"Current scrollbar value: {currentScrollValue}; Maximum: {currentMaximum}")

        if (self.canAutoscroll and (currentScrollValue < currentMaximum)):
            self.miOutput.verticalScrollBar().setValue(self.miOutput.verticalScrollBar().maximum())

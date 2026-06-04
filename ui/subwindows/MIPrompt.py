from PySide6.QtGui import Qt

from backend.MIResponseManager import MIPromptManager
from backend.SideModel import SideModel
from PySide6.QtWidgets import QLineEdit, QTextBrowser, QVBoxLayout, QWidget

from ui.helpers.QtHelpers import Resettable

class MIPrompt(QWidget, Resettable):
    def __init__(self, model: SideModel):
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

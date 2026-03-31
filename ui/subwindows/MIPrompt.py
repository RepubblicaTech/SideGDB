from pprint import pformat
from typing import Dict, List
from PySide6.QtWidgets import QLineEdit, QTextBrowser, QVBoxLayout, QWidget

from backend.SideModel import SideModel


class MIPrompt(QWidget):
    def __init__(self, model: SideModel):
        super().__init__()

        layout = QVBoxLayout()

        self.miPrompt = QLineEdit(placeholderText="Type any GDBMI command in here (-thread-info)")
        self.miResponses = QTextBrowser(self)
        self.miResponses.setPlaceholderText("Responses get printed here")

        layout.addWidget(self.miPrompt)
        layout.addWidget(self.miResponses)

        self.miPrompt.returnPressed.connect(self.sendCommand)

        self.setLayout(layout)

        self.model = model

        # some initialization
        read = self.model.read(-1)
        self.miResponses.setPlainText(self.formatResponse(list(read)))

    def reset(self):
        self.miPrompt.setText("")
        self.miResponses.setPlainText("")

    @staticmethod
    def formatResponse(gdbmiResponses: List[Dict]) -> str:
        formatted = ""

        for response in gdbmiResponses:
            match (response.get("message")):
                case None:
                    formatted += response.get("payload", "")
                    continue
                case "thread-group-added":
                    formatted += f"[THREAD] Thread group {response["payload"]["id"]} added"
                case "thread-group-started":
                    formatted += f"[THREAD] Thread group {response["payload"]["id"]} started"
                case "thread-created":
                    formatted += f"[THREAD] Thread {response["payload"]["id"]} (group {response["payload"]["group-id"]}) created"
                case "cmd-param-changed":
                    formatted += f"[GDBPARAM] {response["payload"]["param"]} set to {response["payload"]["value"]}"
                case "stopped":
                    formatted += "Program stopped."
                case "running":
                    formatted += "Program is running..."
                case _:
                    formatted += pformat(response)

            formatted += "\n"

        return formatted

    def sendCommand(self):
        toSend = self.miPrompt.text()
        if (not toSend):
            return
        print(f"command: {toSend}")

        response = self.model.send(toSend)
        self.miResponses.setPlainText(self.formatResponse(response))

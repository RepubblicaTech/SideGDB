from pprint import pformat
from typing import Dict, List

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette

from backend.SideModel import SideModel
from PySide6.QtWidgets import QLineEdit, QTextBrowser, QVBoxLayout, QWidget

class MIPrompt(QWidget):
    def __init__(self, model: SideModel):
        super().__init__()

        layout = QVBoxLayout()

        self.miPrompt = QLineEdit(placeholderText="Type any GDBMI command in here (-thread-info)")
        self.miOutput = QTextBrowser(self)
        self.miOutput.setPlaceholderText("Responses get printed here")

        layout.addWidget(self.miPrompt)
        layout.addWidget(self.miOutput)


        self.setLayout(layout)

        self.miPrompt.returnPressed.connect(self.sendCommand)

        self.model = model
        read = self.model.read(-1)
        self.printFormatted(list(read))

        self.canAutoscroll = True

    def reset(self):
        self.miPrompt.setText("")
        self.miOutput.setPlainText("")

    def formatResponse(self, miResponse: dict) -> str:
        match (miResponse.get("type")):
            case "log":
                return ""

        match (miResponse.get("message")):
            case "thread-group-added":
                formatted = f"[THREAD] Thread group {miResponse["payload"]["id"]} added"
            case "thread-group-started":
                formatted = f"[THREAD] Thread group {miResponse["payload"]["id"]} started"
            case "thread-created":
                formatted = f"[THREAD] Thread {miResponse["payload"]["id"]} (group {miResponse["payload"]["group-id"]}) created"
            case "cmd-param-changed":
                formatted = f"[GDBPARAM] {miResponse["payload"]["param"]} set to {miResponse["payload"]["value"]}"
            case "stopped":
                formatted = "Program stopped."
            case "running":
                formatted = "Program is running..."
            case "done":
                formatted = "Done."
            case "error":
                formatted = miResponse["payload"]["msg"]
            case None:
                return miResponse.get("payload", "")
            case _:
                return pformat(miResponse) + "\n"

        return formatted + "\n"

    def printFormatted(self, miResponses: List[dict]):
        for response in miResponses:
            match (response.get("message")):
                case "done":
                    self.miOutput.setTextColor("#23c417")
                    self.miOutput.insertPlainText("[DONE] ")
                case "error":
                    self.miOutput.setTextColor("#e93e3e")
                    self.miOutput.insertPlainText("[ERROR] ")
                case _:
                    self.miOutput.setTextColor(self.palette().color(QPalette.ColorRole.Text))

            self.miOutput.insertPlainText(self.formatResponse(response))

    def sendCommand(self):
        toSend = self.miPrompt.text()
        scrollbar = self.miOutput.verticalScrollBar()
        atBottom = scrollbar.value() >= scrollbar.maximum() - 10

        if (not toSend):
            return
        print(f"command: {toSend}")

        response = self.model.send(toSend)
        self.printFormatted(response)

        if atBottom and self.canAutoscroll:
            QTimer.singleShot(0, lambda: scrollbar.setValue(scrollbar.maximum()))

        self.miPrompt.setText("")

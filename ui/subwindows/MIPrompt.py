from pprint import pformat
from typing import List

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

        MIPromptManager.setOutputView(self.miOutput)

        self.model = model
        read = self.model.read(-1)
        MIPromptManager.printFormatted(list(read))

        self.canAutoscroll = True

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

        response = self.model.send(toSend)
        MIPromptManager.printFormatted(response)

        if atBottom and self.canAutoscroll:
            QTimer.singleShot(0, lambda: scrollbar.setValue(scrollbar.maximum()))

        self.miPrompt.setText("")

class MIPromptManager:
    miOutput: QTextBrowser

    @staticmethod
    def setOutputView(p: QTextBrowser):
        MIPromptManager.miOutput = p

    @staticmethod
    def formatResponseMessage(miResponse: dict) -> str:
        return f"[MI::{str(miResponse.get("message") if miResponse.get("message") else "unknown").upper()}] "

    @staticmethod
    def formatResponsePayload(miResponse: dict):
        payload = miResponse.get("payload", None)
        if (not payload):
            return ""

        formatted = ""

        if "bkpt" in payload:
            breakpoint = payload["bkpt"]
            formatted = f"Breakpoint {breakpoint.get("number", "X")} created: {breakpoint.get("func", "<unknown>")}() @ {breakpoint.get("file", "/???.?")}:{breakpoint.get("line", "??")}"
        elif "BreakpointTable" in payload:
            breakpointTable = dict(payload["BreakpointTable"])
            breakpointsList = list(breakpointTable["body"])
            for breakpoint in breakpointsList:
                formatted += f"Breakpoint {breakpoint.get("number", "X")}: {breakpoint.get("func", "<unknown>")}() @ {breakpoint.get("file", "/???.?")}:{breakpoint.get("line", "??")}\n"
        else:
            formatted = pformat(payload)

        return formatted

    @staticmethod
    def printFormatted(miResponses: List[dict]):
        for response in miResponses:
            match (response.get("message")):
                case "done":
                    MIPromptManager.miOutput.setTextColor("#23c417")
                case "error":
                    MIPromptManager.miOutput.setTextColor("#e93e3e")
                case _:
                    MIPromptManager.miOutput.setTextColor(MIPromptManager.miOutput.palette().color(QPalette.ColorRole.Text))

            MIPromptManager.miOutput.insertPlainText(MIPromptManager.formatResponseMessage(response))
            if (response.get("payload", None)):
                MIPromptManager.miOutput.insertPlainText(MIPromptManager.formatResponsePayload(response) + "\n")

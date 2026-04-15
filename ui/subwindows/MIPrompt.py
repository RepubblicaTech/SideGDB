from pprint import pformat
from typing import List

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette, Qt

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
        read = self.model.read(-1)
        MIPromptManager.printFormatted(list(read))

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
        if (miResponse.get("message")):
            return f"[MI::{str(miResponse.get("message")).upper()}] "
        else:
            return ""

    @staticmethod
    def formatResponsePayload(miResponse: dict):
        payload = miResponse.get("payload", None)
        if (not payload):
            return ""

        formatted = ""

        match(miResponse.get("type")):
            case "log":
                return ""
            case "console":
                return str(payload)
            case "result" | "notify":
                pass
            case _:
                return pformat(payload) + "\n"

        match(miResponse.get("message")):
            case "thread-group-added":
                return f"Thread group {miResponse["payload"]["id"]} added\n"
            case "thread-group-started":
                return f"Thread group {miResponse["payload"]["id"]} started\n"
            case "thread-created":
                thread = miResponse["payload"]
                return f"Thread {thread["id"]} (group {thread["group-id"]}) created\n"
            case "cmd-param-changed":
                cmdParam = dict(miResponse["payload"])
                return f"{cmdParam["param"]} set to {cmdParam["value"]}\n"
            case "stopped":
                return f"Program stopped @ {miResponse["payload"]["frame"]["addr"]}\n"
            case None:
                return str(payload)
            case _:
                pass

        payloadKeys = list(dict(payload).keys())
        match(payloadKeys[0]):
            case "msg":
                formatted = payload["msg"]
            case "bkpt":
                breakpoint = payload["bkpt"]
                formatted = f"Breakpoint {breakpoint.get("number", "X")} created: {breakpoint.get("func", "<unknown>")}() @ {breakpoint.get("file", "/???.?")}:{breakpoint.get("line", "??")}"
            case "BreakpointTable":
                breakpointTable = dict(payload["BreakpointTable"])
                breakpointsList = list(breakpointTable["body"])
                if (not breakpointsList):
                    return "No breakpoints set."
                formatted = "Breakpoints list:\n"
                for breakpoint in breakpointsList:
                    formatted += f"\t[{breakpoint.get("number", "X")}]: {breakpoint.get("func", "<unknown>")}() @ {breakpoint.get("file", "/???.?")}:{breakpoint.get("line", "??")}\n"
                    return formatted
            case _:
                formatted = pformat(payload)

        return formatted + "\n"

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
                MIPromptManager.miOutput.insertPlainText(MIPromptManager.formatResponsePayload(response))

from pprint import pformat
from ui import model
from ui.subwindows import magic_view

class MagicController:
    def __init__(self, view: magic_view.MagicView, model: model.SGDBModel) -> None:
        self.view = view
        self.model = model

        self.view.magicButton.clicked.connect(self.sendCommand)

    def sendCommand(self):
        toSend = self.view.magicInput.text()
        print(f"command: {toSend}")
        response = self.model.gdbMI.sendCmd(toSend)
        self.view.magicTextArea.setText(pformat(response))

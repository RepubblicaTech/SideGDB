from pprint import pformat

from PySide6 import QtCore
from loguru import logger
from backend.model import SideModel
from ui.main_views.BottomView import BottomView

class BottomController:
    def __init__(self, view: BottomView, model: SideModel):
        self.view = view
        self.model = model

        self.view.gdbSendButton().clicked.connect(self.sendToMI)

    @QtCore.Slot()
    def sendToMI(self):
        command = self.view.gdbPromptInput()
        logger.debug(f"Sending: {command}")
        response = self.model.send(command)

        self.view.appendToGdbOut(pformat(response))

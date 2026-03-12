from loguru import logger
from ui import main_view
from ui.launcher import launcher_view
from ui import model

class LauncherController:
    def __init__(self, view: launcher_view.LauncherView):
        self.view = view

        self.view.openButton.clicked.connect(self.openSession)
        self.view.createButton.clicked.connect(self.startSession)

    def openSession(self):
        logger.debug(f"Using config")

    def startSession(self):
        logger.debug("Starting main UI")
        # destroy launcher window
        pass

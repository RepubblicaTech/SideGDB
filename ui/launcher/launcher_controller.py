from loguru import logger
from ui.launcher import launcher_view

class LauncherController:
    def __init__(self, view: launcher_view.LauncherView):
        self.view = view

        self.view.openButton.clicked.connect(self.openSession)
        self.view.createButton.clicked.connect(self.startSession)

    def openSession(self):
        logger.debug("Using config")

        self.startSession()

    def startSession(self):
        logger.debug("Starting main UI")
        self.view.close()

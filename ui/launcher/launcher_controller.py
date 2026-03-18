from pathlib import Path
import traceback
from loguru import logger
from backend import SGDBConfig
from ui import observer
from ui.launcher import launcher_view

class LauncherController:
    def __init__(self, view: launcher_view.LauncherView):
        self.view = view

        self.view.openButton.clicked.connect(self.openSession)
        self.view.createButton.clicked.connect(self.createSession)

    def createSession(self):
        observer.notify(observer.SGSignals.SGDB_SIGCREATE)

    def openSession(self):
        chosenFile = self.view.openFile()
        if (chosenFile[0] == ""):
            return
        logger.debug(f"Using file {chosenFile[0]}")
        try:
            currentConfig = SGDBConfig.ConfigManager.load(Path(chosenFile[0]))
        except ValueError as ex:
            traceback.print_exc()
            logger.debug(ex)
            logger.critical("Invalid configuration. Please choose a valid configuration file.")
            return

        self.view.close()
        observer.notify(observer.SGSignals.SGDB_SIGLAUNCH, config=currentConfig)

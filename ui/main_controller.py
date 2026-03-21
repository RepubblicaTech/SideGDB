import subprocess
from PySide6.QtGui import QCloseEvent
from loguru import logger
from backend import GdbMi, SGDBConfig
from ui import observer
from ui.main_view import MainView, SGDBConfigView

class SGDBController:
    def __init__(self, view: MainView):
        self.view = view

        observer.subscribe(observer.SGSignals.SGDB_SIGCREATE, self.spawnConfigureGDB)
        observer.subscribe(observer.SGSignals.SGDB_SIGLAUNCH, self.startDebugging)

        self.view.closeEvent = self.closeEvent

        self.view.quitSessionQMenu.triggered.connect(self.terminateSession)

    def terminateSession(self):
        logger.debug("Terminating GDBMI...")
        self.gdbMi.terminate()

    def closeEvent(self, event: QCloseEvent):
        logger.debug("Wooo i'm overriding the close event!!!")
        self.terminateSession()

        event.accept()

    def startDebugging(self, config: SGDBConfig.Config):
        logger.debug(f"Debugging program: {str(config.programPath)}")
        if (config.dotGdbPath is not None):
            logger.debug(f"GDB script: {str(config.dotGdbPath)}")

        # preRunCommands
        if (config.preRunCommands is not None):
            for command in config.preRunCommands:
                logger.debug(f"Command {command}")
                out = subprocess.check_output(command.split(" "), text=True, cwd=config.envPrefix)
                logger.debug(f"Output:\n{out}")

        self.gdbMi = GdbMi.GdbMI(SGDBConfig.SGDBConfigManager.toGDBArgs(config))

        # set up UI elements
        self.view.loadMainUI()

    def spawnConfigureGDB(self):
        self.sgdbConfig = SGDBConfigView(self.view)
        self.sgdbConfig.show()

        # self.sgdbConfig.close()

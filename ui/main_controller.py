from loguru import logger
from ui import observer
from ui.main_view import MainView, SGDBConfigView

class SGDBController:
    def __init__(self, view: MainView):
        self.view = view

        observer.subscribe(observer.SGSignals.SGDB_SIGCREATE, self.spawnConfigureGDB)
        observer.subscribe(observer.SGSignals.SGDB_SIGLAUNCH, self.startDebugging)

    def startDebugging(self, config):
        logger.debug(f"Given config {config}")
        # parse JSON
        # set up GDB

        # set up UI elements
        self.view.loadMainUI()

    def spawnConfigureGDB(self):
        self.sgdbConfig = SGDBConfigView(self.view)
        self.sgdbConfig.show()

        # self.sgdbConfig.close()

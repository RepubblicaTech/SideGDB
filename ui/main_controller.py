from ui import observer
from ui.main_view import MainView, SGDBConfigView

class SGDBController:
    def __init__(self, view: MainView):
        self.view = view

        observer.subscribe(observer.SGSignals.SGDB_SIGCREATE, self.spawnConfigureGDB)
        observer.subscribe(observer.SGSignals.SGDB_SIGLAUNCH, self.setupMainUI)

    def setupMainUI(self):
        self.view.loadMainUI()

    def spawnConfigureGDB(self):
        self.sgdbConfig = SGDBConfigView(self.view)
        self.sgdbConfig.show()

        # self.sgdbConfig.close()

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
        observer.notify(observer.SGSignals.SGDB_SIGLAUNCH, config=chosenFile[0])

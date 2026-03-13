from ui import observer
from ui.main_view import MainView

class SGDBController:
    def __init__(self, view: MainView):
        self.view = view

        observer.subscribe(observer.SGSignals.SGDB_SIGSTART, self.view.loadMainUI)

from PySide6.QtWidgets import QDockWidget
from ui.helpers.QtHelpers import Resettable, Updateable
from ui.subwindows.QCodeWidgets.QCodeArea import QCodeArea

class CodeDock(QDockWidget, Updateable, Resettable):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Source code view")
        self.codeView = QCodeArea()
        self.setWidget(self.codeView)

    def loadSource(self, path: str):
        self.codeView.loadSource(path)

    def highlightLine(self, line: int):
        self.codeView.highlightLine(line)
        self.codeView.scrollTo(line)

    def sgUpdate(self, frame: dict):
        file = frame.get("fullname", None)
        line = int(frame["line"])
        if (file):
            self.loadSource(file)
        if (line):
            self.highlightLine(line)

    def sgReset(self):
        self.codeView.sgReset()

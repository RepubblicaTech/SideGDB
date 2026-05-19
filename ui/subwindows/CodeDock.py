from PySide6.QtWidgets import QDockWidget
from ui.helpers.QtHelpers import QCodeArea, Updateable

class CodeDock(QDockWidget, Updateable):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code")
        self.codeView = QCodeArea()
        self.setWidget(self.codeView)

    def loadSource(self, path: str):
        self.codeView.loadSource(path)

    def highlightLine(self, line: int):
        self.codeView.highlightLine(line)
        self.codeView.scrollTo(line)

    def sgUpdate(self, frame: dict):
        file = frame.get("fullname", None)
        if (file):
            self.loadSource(file)
        try:
            line = int(frame["line"])
            if (line):
                self.highlightLine(line)
        except Exception as e:
            print(str(e))

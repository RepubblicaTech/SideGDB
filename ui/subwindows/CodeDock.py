from PySide6.QtWidgets import QDockWidget
from ui.helpers.QtHelpers import QCodeArea, Updateable

class CodeDock(QDockWidget, Updateable):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code")

        self.codeArea = QCodeArea()
        self.setWidget(self.codeArea)

    def sgUpdate(self, frame: dict):
        file = frame.get("fullname", None)
        if (file):
            self.codeArea.codeBrowser().loadFile(file)
        try:
            line = int(frame["line"])
            if (line):
                self.codeArea.codeBrowser().highlightLine(line)
                self.codeArea.scrollTo(line)
                self.codeArea.update()
        except Exception as e:
            print(str(e))

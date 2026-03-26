from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMenuBar, QToolBar
from assets.QFugueAssets import FugueIconSize, QFugueManager

class DebuggerToolBar(QToolBar):
    def __init__(self, parent, title: str = ""):
        super().__init__(title)

        openTQAction = QAction(icon=QFugueManager.loadIcon("disc", "plus", FugueIconSize.FUGUE_32), parent=parent)
        openTQAction.setToolTip("New debugger instance")

        self.addAction(openTQAction)

class DebuggerMenuBar():
    def __init__(self, menuBar: QMenuBar, appTitle: str) -> None:

        fileQMenu = menuBar.addMenu("File")
        helpQMenu = menuBar.addMenu("Help")
        openQAction = fileQMenu.addAction("Open configuration...")
        aboutQAction = helpQMenu.addAction(f"About{f" {appTitle}" if appTitle else ""}")

class DebuggerUI(QMainWindow):
    def __init__(self, appTitle: str):
        super().__init__()

        self.appTitle = appTitle or "pyDearGDB"     # easter egg

        self.setWindowTitle(f"{self.appTitle} Debugger")
        self.resize(1200, 800)

        DebuggerMenuBar(self.menuBar(), self.appTitle)
        self.addToolBar(DebuggerToolBar(self))

        label = QLabel("Hi there! Check out the menubar (or the toolbar) to create (or re-use) a GDB Session.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

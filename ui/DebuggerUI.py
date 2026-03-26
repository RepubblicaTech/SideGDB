from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMenu, QMenuBar


class DebuggerUI(QMainWindow):
    def __init__(self, appTitle: str):
        super().__init__()

        self.appTitle = appTitle or "pyDearGDB"     # easter egg

        self.setWindowTitle(f"{self.appTitle} Debugger")
        self.resize(1200, 800)

        menubar = self.menuBar()
        fileQMenu = menubar.addMenu("File")
        helpQMenu = menubar.addMenu("Help")

        openQAction = fileQMenu.addAction("Open configuration...")
        aboutQAction = helpQMenu.addAction(f"About {self.appTitle}")

        label = QLabel("Hi there! Check out this neat thing called the menu bar to create (or re-use) a GDB Session.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, appTitle):
        super().__init__()

        self.setWindowTitle(appTitle)

        self.fileMenu = QtWidgets.QMenu("File")
        self.fileMenu.addAction("Open Session...")
        self.fileMenu.addAction("Save Session")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Configure GDB...")

        self.setMenuBar(QtWidgets.QMenuBar(self))
        self.menuBar().addMenu(self.fileMenu)

        self.resize(1000, 800)

        self.mdiArea = QtWidgets.QMdiArea()
        self.mdiArea.setBackground(QImage("bg.png"))

        self.setCentralWidget(self.mdiArea)

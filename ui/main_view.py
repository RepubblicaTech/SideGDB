from PySide6 import QtWidgets
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage

from ui.main_views import bottom_view, code_view, right_view

class MainView(QtWidgets.QMainWindow):
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

    def loadMainUI(self):
        self.update()

        # Update menu bar
        self.fileMenu.addAction("Quit Session")
        self.codeMenu = QtWidgets.QMenu("Code")
        self.codeMenu.addAction("Manage breakpoints...")
        self.menuBar().addMenu(self.codeMenu)

        # create UI elements
        self.codeSubWindow = code_view.CodeDebugView(self.mdiArea)
        self.rightSubWindow = right_view.RightView(self.mdiArea)
        self.bottomSubWindow = bottom_view.BottomView(self.mdiArea)

        cWindowWidth = 600
        cWindowHeight = 400

        self.codeSubWindow.setGeometry(0, 0, cWindowWidth, cWindowHeight)
        self.rightSubWindow.setGeometry(cWindowWidth,
                                        0,
                                        self.width() - cWindowWidth,
                                        self.height() - self.menuBar().height())
        self.bottomSubWindow.setGeometry(0, cWindowHeight,
                                         cWindowWidth,
                                         self.height() - cWindowHeight - self.menuBar().height())

        # idk why
        self.codeSubWindow.show()
        self.rightSubWindow.show()
        self.bottomSubWindow.show()

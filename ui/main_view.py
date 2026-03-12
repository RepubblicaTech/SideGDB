from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

from ui.main_window_view import MainWindow
from ui.main_views import bottom_view, code_view, right_view

class MainView():
    def __init__(self, mainWindow: MainWindow):
        self.mainWindow = mainWindow

        # Update menu bar
        self.mainWindow.fileMenu.addAction("Quit Session")
        self.codeMenu = QtWidgets.QMenu("Code")
        self.codeMenu.addAction("Manage breakpoints...")
        self.mainWindow.menuBar().addMenu(self.codeMenu)

        self.codeSubWindow = code_view.CodeDebugView(self.mainWindow.mdiArea)
        self.rightSubWindow = right_view.RightView(self.mainWindow.mdiArea)
        self.bottomSubWindow = bottom_view.BottomView(self.mainWindow.mdiArea)

        self.codeSubWindow.setGeometry(0, 0, 600, 400)
        self.rightSubWindow.setGeometry(self.codeSubWindow.width(),
                                        0,
                                        self.mainWindow.width() - self.codeSubWindow.width(),
                                        self.mainWindow.height() - self.mainWindow.menuBar().height())
        self.bottomSubWindow.setGeometry(0, self.codeSubWindow.height(),
                                         self.codeSubWindow.width(),
                                         self.mainWindow.height() - self.codeSubWindow.height() - self.mainWindow.menuBar().height())

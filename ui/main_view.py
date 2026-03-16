from PySide6 import QtWidgets
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QDragLeaveEvent, QImage

from ui.main_views import bottom_view, code_view, right_view

class MainView(QtWidgets.QMainWindow):
    def __init__(self, appTitle):
        super().__init__()

        self.setWindowTitle(appTitle)

        self.fileMenu = QtWidgets.QMenu("File")
        self.openSessionQMenu = self.fileMenu.addAction("Open Session...")

        self.setMenuBar(QtWidgets.QMenuBar(self))
        self.menuBar().addMenu(self.fileMenu)

        self.resize(1000, 800)

        self.mdiArea = QtWidgets.QMdiArea()
        self.mdiArea.setBackground(QImage("bg.png"))

        self.setCentralWidget(self.mdiArea)

    def loadMainUI(self):
        self.update()

        self.saveSessionQMenu = self.fileMenu.addAction("Save Session...")
        self.fileMenu.addSeparator()
        self.quitSessionQMenu = self.fileMenu.addAction("Quit Session")

        self.codeMenu = QtWidgets.QMenu("Code")
        self.breakManQMenu = self.codeMenu.addAction("Manage breakpoints...")
        self.menuBar().addMenu(self.codeMenu)

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

        self.codeSubWindow.show()
        self.rightSubWindow.show()
        self.bottomSubWindow.show()

class SGDBConfigView(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__(parent)
        self.setWindowTitle("GDB Configuration")
        self.setModal(True)

        self.resize(600,200)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        gdbConfTab = QtWidgets.QWidget()
        gdbConfGrid = QtWidgets.QGridLayout()

        self.configNameIn = QtWidgets.QLineEdit(placeholderText="A beautiful GDB configuration")
        self.programPathIn = QtWidgets.QLineEdit(placeholderText="/some/path/to/a.out")
        self.dotGdbPathIn = QtWidgets.QLineEdit(placeholderText="/path/to/script.gdb")
        self.programPathChoose = QtWidgets.QPushButton("...")
        self.dotGdbPathChoose = QtWidgets.QPushButton("...")
        gdbConfGrid.addWidget(QtWidgets.QLabel("Config name*"), 0, 0)
        gdbConfGrid.addWidget(QtWidgets.QLabel("Program path*"), 1, 0)
        gdbConfGrid.addWidget(QtWidgets.QLabel("GDB Script"), 2, 0)
        gdbConfGrid.addWidget(self.configNameIn, 0, 1, 1, 2)
        gdbConfGrid.addWidget(self.programPathIn, 1, 1, 1, 1)
        gdbConfGrid.addWidget(self.programPathChoose, 1, 2, 1, 1)
        gdbConfGrid.addWidget(self.dotGdbPathIn, 2, 1, 1, 1)
        gdbConfGrid.addWidget(self.dotGdbPathChoose, 2, 2, 1, 1)

        gdbConfTab.setLayout(gdbConfGrid)
        self.tabWidget.addTab(gdbConfTab, "GDB Settings")

        envConfTab = QtWidgets.QWidget()
        envConfGrid = QtWidgets.QGridLayout()

        self.envPathIn = QtWidgets.QLineEdit(placeholderText="/likely/path/to/your/project")
        self.envPathChoose = QtWidgets.QPushButton("...")
        self.preRunCommandsIn = QtWidgets.QPlainTextEdit(placeholderText="make debug-remote... or something like that lol")
        self.preRunCommandsIn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        envConfGrid.addWidget(QtWidgets.QLabel("Environment path"), 0, 0)
        envConfGrid.addWidget(self.envPathIn, 0, 1)
        envConfGrid.addWidget(self.envPathChoose, 0, 2)
        envConfGrid.addWidget(QtWidgets.QLabel("Pre-run commands"), 1, 0)
        envConfGrid.addWidget(self.preRunCommandsIn, 2, 0, 1, 3)

        envConfTab.setLayout(envConfGrid)
        self.tabWidget.addTab(envConfTab, "Environment")

        self.doneButton = QtWidgets.QPushButton("Done")

        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.doneButton, alignment=Qt.AlignmentFlag.AlignRight)
        mainLayout.addStretch()

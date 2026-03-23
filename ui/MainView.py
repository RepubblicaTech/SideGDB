import subprocess
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QImage
from loguru import logger

from backend import GDBMI, SGDBConfig
from backend.model import SideModel
from ui import observer
from ui.helpers import QtHelpers
from ui.main_views import BottomView, CodeView, RightView
from ui.main_views.BottomController import BottomController

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

        observer.subscribe(observer.SGSignals.SGDB_SIGCREATE, self.spawnConfigureGDB)
        observer.subscribe(observer.SGSignals.SGDB_SIGLAUNCH, self.startDebugging)

    def loadMainUI(self):
        self.saveSessionQMenu = self.fileMenu.addAction("Save Session...")
        self.fileMenu.addSeparator()
        self.quitSessionQMenu = self.fileMenu.addAction("Quit Session")

        self.codeMenu = QtWidgets.QMenu("Code")
        self.breakManQMenu = self.codeMenu.addAction("Manage breakpoints...")
        self.menuBar().addMenu(self.codeMenu)

        self.codeSubWindow = CodeView.CodeDebugView()
        self.rightSubWindow = RightView.RightView()
        self.bottomSubWindow = BottomView.BottomView()

        self.mdiArea.addSubWindow(self.codeSubWindow)
        self.mdiArea.addSubWindow(self.rightSubWindow)
        self.mdiArea.addSubWindow(self.bottomSubWindow)

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

    def startDebugging(self, config: SGDBConfig.Config):
        logger.debug(f"Debugging program: {str(config.programPath)}")
        if (config.dotGdbPath is not None):
            logger.debug(f"GDB script: {str(config.dotGdbPath)}")

        # preRunCommands
        if (config.preRunCommands is not None):
            for command in config.preRunCommands:
                logger.debug(f"Command {command}")
                logger.debug(f"Output:\n{subprocess.check_output(command.split(" "), text=True, cwd=config.envPrefix)}")

        logger.success("preRunCommands OK!")

        self.gdbMi = GDBMI.GdbMI(SGDBConfig.SideConfigManager.toGDBArgs(config))
        self.model = SideModel(self.gdbMi)
        logger.success("GDB-MI initialization OK!")

        # set up UI elements
        self.loadMainUI()
        self.quitSessionQMenu.triggered.connect(self.terminateSession)

        # set up some controllers
        BottomController(self.bottomSubWindow, self.model)

    @QtCore.Slot()
    def terminateSession(self):
        logger.debug("Terminating GDBMI...")
        self.gdbMi.terminate()

    def closeEvent(self, event: QCloseEvent):
        logger.debug("Wooo i'm overriding the close event!!!")
        self.terminateSession()

        event.accept()

    def spawnConfigureGDB(self):
        self.sgdbConfig = SGDBConfigView(self)
        self.sgdbConfig.show()

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
        gdbConfV = QtWidgets.QVBoxLayout()

        self.configName = QtHelpers.QLabeledLineEdit(QtHelpers.QDirectionFlag.QHorizontal, "Config name*", placeholderText="A beautiful GDB configuration")
        self.programPath = QtHelpers.QPathChoose(QtWidgets.QFileDialog.FileMode.ExistingFile, sideText="Program path*", lineEditPlaceholder="/some/path/to/a.out")
        self.dotGdbPath = QtHelpers.QPathChoose(QtWidgets.QFileDialog.FileMode.ExistingFile, sideText="GDB Script", lineEditPlaceholder="/path/to/script.gdb")

        gdbConfV.addWidget(self.configName)
        gdbConfV.addWidget(self.programPath)
        gdbConfV.addWidget(self.dotGdbPath)

        gdbConfTab.setLayout(gdbConfV)
        self.tabWidget.addTab(gdbConfTab, "GDB Settings")

        envConfTab = QtWidgets.QWidget()
        envConfGrid = QtWidgets.QVBoxLayout()

        self.envPath = QtHelpers.QPathChoose(QtWidgets.QFileDialog.FileMode.Directory, sideText="Environment path", lineEditPlaceholder="/likely/path/to/your/project")
        self.preRunCommandsIn = QtWidgets.QPlainTextEdit(placeholderText="make debug-remote... or something like that lol")
        self.preRunCommandsIn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        envConfGrid.addWidget(self.envPath)
        envConfGrid.addWidget(QtWidgets.QLabel("Pre-run commands"))
        envConfGrid.addWidget(self.preRunCommandsIn)

        envConfTab.setLayout(envConfGrid)
        self.tabWidget.addTab(envConfTab, "Environment")

        self.doneButton = QtWidgets.QPushButton("Done")

        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.doneButton, alignment=Qt.AlignmentFlag.AlignRight)
        mainLayout.addStretch()

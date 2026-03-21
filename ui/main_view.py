from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

from ui.helpers import QtHelpers
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

        self.__codeSubWindow = code_view.CodeDebugView(self.mdiArea)
        self.__rightSubWindow = right_view.RightView(self.mdiArea)
        self.__bottomSubWindow = bottom_view.BottomView(self.mdiArea)

        cWindowWidth = 600
        cWindowHeight = 400

        self.__codeSubWindow.setGeometry(0, 0, cWindowWidth, cWindowHeight)
        self.__rightSubWindow.setGeometry(cWindowWidth,
                                        0,
                                        self.width() - cWindowWidth,
                                        self.height() - self.menuBar().height())
        self.__bottomSubWindow.setGeometry(0, cWindowHeight,
                                         cWindowWidth,
                                         self.height() - cWindowHeight - self.menuBar().height())

        self.__codeSubWindow.show()
        self.__rightSubWindow.show()
        self.__bottomSubWindow.show()

    def appendGDBMIOutput(self, more: str):
        self.__bottomSubWindow.gdbConsoleWidget.gdbOutput.append(more)

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

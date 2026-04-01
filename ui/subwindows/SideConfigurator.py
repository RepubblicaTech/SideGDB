from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QFileDialog, QLabel, QPlainTextEdit, QPushButton, QSizePolicy, QTabWidget, QVBoxLayout, QWidget

from ui.helpers import QtHelpers

class GDBConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.__configName = QtHelpers.QLabeledLineEdit(QtHelpers.QDirectionFlag.QHorizontal, "Config name*", placeholderText="A beautiful GDB configuration")
        self.__programPath = QtHelpers.QPathChoose(QFileDialog.FileMode.ExistingFile, sideText="Program path*", lineEditPlaceholder="/some/path/to/a.out")
        self.__dotGdbPath = QtHelpers.QPathChoose(QFileDialog.FileMode.ExistingFile, sideText="GDB Script", lineEditPlaceholder="/path/to/script.gdb")

        layout.addWidget(self.__configName)
        layout.addWidget(self.__programPath)
        layout.addWidget(self.__dotGdbPath)

        self.setLayout(layout)

    def sessionTitle(self):
        return self.__configName.inputText()

    def programPath(self):
        return self.__programPath.chosenPath()

    def dotGdbPath(self):
        return self.__dotGdbPath.chosenPath()

class EnvConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.__envPath = QtHelpers.QPathChoose(QFileDialog.FileMode.Directory, sideText="Environment path", lineEditPlaceholder="/likely/path/to/your/project")
        self.__preRunCommandsIn = QPlainTextEdit(placeholderText="make debug-remote... or something like that lol")
        self.__preRunCommandsIn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.__envPath)
        layout.addWidget(QLabel("Pre-run commands"))
        layout.addWidget(self.__preRunCommandsIn)

        self.setLayout(layout)

    def envPath(self):
        return self.__envPath.chosenPath()

    def preRunCommands(self):
        return self.__preRunCommandsIn.toPlainText()

class SideConfigurator(QDialog):
    def __init__(self, parent, appTitle: str):
        super().__init__(parent)
        self.appTitle = appTitle or "pyGDBView" # easter egg 2

        self.setWindowTitle(f"New {self.appTitle} Session")
        self.resize(600,200)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.__gdbConfig = GDBConfig()
        self.__envConfig = EnvConfig()

        self.tabWidget.addTab(self.__gdbConfig, "GDB Settings")
        self.tabWidget.addTab(self.__envConfig, "Environment")

        self.doneButton = QPushButton("Done")

        self.doneButton.clicked.connect(self.accept)

        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.doneButton, alignment=Qt.AlignmentFlag.AlignRight)
        mainLayout.addStretch()

    def sessionTitle(self):
        return self.__gdbConfig.sessionTitle()

    def programPath(self):
        return self.__gdbConfig.programPath()

    def dotGdbPath(self):
        return self.__gdbConfig.dotGdbPath()

    def envPath(self):
        return self.__envConfig.envPath()

    def preRunCommands(self):
        return self.__envConfig.preRunCommands()

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QFileDialog, QLabel, QPlainTextEdit, QPushButton, QSizePolicy, QTabWidget, QVBoxLayout, QWidget

from ui.helpers import QtHelpers

class GDBConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.configName = QtHelpers.QLabeledLineEdit(QtHelpers.QDirectionFlag.QHorizontal, "Config name*", placeholderText="A beautiful GDB configuration")
        self.programPath = QtHelpers.QPathChoose(QFileDialog.FileMode.ExistingFile, sideText="Program path*", lineEditPlaceholder="/some/path/to/a.out")
        self.dotGdbPath = QtHelpers.QPathChoose(QFileDialog.FileMode.ExistingFile, sideText="GDB Script", lineEditPlaceholder="/path/to/script.gdb")

        layout.addWidget(self.configName)
        layout.addWidget(self.programPath)
        layout.addWidget(self.dotGdbPath)

        self.setLayout(layout)

class EnvConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.envPath = QtHelpers.QPathChoose(QFileDialog.FileMode.Directory, sideText="Environment path", lineEditPlaceholder="/likely/path/to/your/project")
        self.preRunCommandsIn = QPlainTextEdit(placeholderText="make debug-remote... or something like that lol")
        self.preRunCommandsIn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.envPath)
        layout.addWidget(QLabel("Pre-run commands"))
        layout.addWidget(self.preRunCommandsIn)

        self.setLayout(layout)

class SideConfigurator(QDialog):
    def __init__(self, parent, appTitle: str):
        super().__init__(parent)
        self.appTitle = appTitle or "pyGDBView"

        self.setWindowTitle(f"New {self.appTitle} Session")
        self.setModal(True)
        self.resize(600,200)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.tabWidget.addTab(GDBConfig(), "GDB Settings")
        self.tabWidget.addTab(EnvConfig(), "Environment")

        self.doneButton = QPushButton("Done")

        self.doneButton.clicked.connect(self.accept)

        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.doneButton, alignment=Qt.AlignmentFlag.AlignRight)
        mainLayout.addStretch()

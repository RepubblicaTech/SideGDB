import os
from pathlib import Path
from pprint import pformat
import traceback
import subprocess
from PySide6.QtGui import QCloseEvent
from loguru import logger

from assets.QFugueAssets import FugueIconSize, QFugueManager
from backend.SGDBConfig import SGDBConfig, SGDBConfigManager
from backend.GDBMI import GdbMI

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFileDialog, QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit, QToolBar, QVBoxLayout, QWidget

from backend.SideModel import SideModel
from ui.subwindows.SideConfigurator import SideConfigurator

class MIPrompt(QWidget):
    def __init__(self, model: SideModel):
        super().__init__()

        layout = QVBoxLayout()

        self.miPrompt = QLineEdit(placeholderText="Type any GDBMI command in here (-thread-info)")
        self.miResponses = QPlainTextEdit(placeholderText="Responses get printed here", readOnly=True)

        layout.addWidget(self.miPrompt)
        layout.addWidget(self.miResponses)

        self.miPrompt.returnPressed.connect(self.sendCommand)

        self.setLayout(layout)

        self.model = model

        # some initialization
        read = self.model.read(-1)
        self.miResponses.setPlainText(pformat(read))

    def reset(self):
        self.miPrompt.setText("")
        self.miResponses.setPlainText("")

    def sendCommand(self):
        toSend = self.miPrompt.text()
        if (not toSend):
            return
        print(f"command: {toSend}")

        response = self.model.send(toSend)
        self.miResponses.setPlainText(pformat(response))

class DebuggerUI(QMainWindow):
    def __init__(self, appTitle: str):
        super().__init__()

        self.appTitle = appTitle or "pyDearGDB"     # easter egg

        self.setWindowTitle(self.appTitle)
        self.resize(1200, 800)

        # MENU BAR
        menuBar = self.menuBar()
        # FILE
        fileQMenu = menuBar.addMenu("File")
        newQAction = fileQMenu.addAction("New Session...")
        openQAction = fileQMenu.addAction("Open configuration...")
        # HELP
        helpQMenu = menuBar.addMenu("Help")
        aboutQAction = helpQMenu.addAction(f"About{f" {appTitle}" if appTitle else ""}")

        # MAIN TOOLBAR (NEW, OPEN, SAVE, ETC.)
        self.mainToolbar = QToolBar("Main toolbar")
        self.mainToolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.newQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("bug--plus", FugueIconSize.FUGUE_32), "New")
        self.openQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("folder-horizontal-open", FugueIconSize.FUGUE_32), "Open")
        self.saveAsQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("disk-rename", FugueIconSize.FUGUE_32), "")
        # self.saveQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("disk", FugueIconSize.FUGUE_32), "")
        self.endQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("plug-disconnect-prohibition", FugueIconSize.FUGUE_32), "Terminate")
        self.saveAsQAction.setToolTip("Save As...")
        # self.saveQAction.setToolTip("Save")

        # DEBUG TOOLBAR (CONTINUE, STEP)
        self.debugToolbar = QToolBar("Debugging toolbar")
        self.debugToolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.breakPointsQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("table-delete-row", FugueIconSize.FUGUE_32), "Breakpoints")
        self.continueQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("control", FugueIconSize.FUGUE_32), "")
        self.stepOverQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("arrow-step-over", FugueIconSize.FUGUE_32), "")
        self.stepIntoQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("arrow-step", FugueIconSize.FUGUE_32), "")
        self.stepOutQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("arrow-step-out", FugueIconSize.FUGUE_32), "")

        # WIDGETS TOOLBAR (SHOW/HIDE)
        self.widgetsToolbar = QToolBar("Widgets toolbar")
        self.widgetsToolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.codeQAction = self.widgetsToolbar.addAction(QFugueManager.loadIcon("script-code", FugueIconSize.FUGUE_32), "")
        self.disasmQAction = self.widgetsToolbar.addAction(QFugueManager.loadIcon("script-binary", FugueIconSize.FUGUE_32), "")
        self.varsQAction = self.widgetsToolbar.addAction(QFugueManager.loadIcon("block", FugueIconSize.FUGUE_32), "")
        self.regsQAction = self.widgetsToolbar.addAction(QFugueManager.loadIcon("processor", FugueIconSize.FUGUE_32), "")
        self.codeQAction.setCheckable(True)
        self.disasmQAction.setCheckable(True)
        self.varsQAction.setCheckable(True)
        self.regsQAction.setCheckable(True)
        self.codeQAction.setToolTip("Showw code")
        self.disasmQAction.setToolTip("Show disassembly")
        self.varsQAction.setToolTip("Show variables")
        self.regsQAction.setToolTip("Show registers")

        self.addToolBar(self.mainToolbar)

        self.__fileDialog = QFileDialog()

        self.newQAction.triggered.connect(self.spawnConfigureGDB)
        self.openQAction.triggered.connect(self.openConfig)
        self.saveAsQAction.triggered.connect(self.saveAs)
        self.endQAction.triggered.connect(self.terminateSession)

        # to check if a program is being debugged.
        self.running = False

    def saveAs(self):
        try:
            self.currentConfig
        except AttributeError:
            QMessageBox(QMessageBox.Icon.Warning, "No configuration", "No current configuration is available. Please create a new session before saving.", QMessageBox.StandardButton.Ok).exec()
            return

        self.__fileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        destinationFile = self.__fileDialog.getSaveFileName(self, dir=os.getcwd(), filter="JSON (*.json)")
        if (destinationFile[0] == ""):
            return
        logger.debug(f"Saving to file {destinationFile[0]}")
        SGDBConfigManager.save(self.currentConfig, Path(destinationFile[0]))

    def spawnConfigureGDB(self):
        if (self.running):
            QMessageBox(QMessageBox.Icon.Warning, "Running session", "An instance of GDB is already running. Make sure to terminate the current session before starting a new one.", QMessageBox.StandardButton.Ok).exec()
            return

        self.statusBar().showMessage("Showing configuration")
        configurator = SideConfigurator(self, self.appTitle)
        if not configurator.exec():
            logger.warning("Bro quit. Doing nothing.")
            self.statusBar().showMessage("Configuration cancelled.")
            return

        try:
            if (not configurator.programPath()):
                raise TypeError("programPath")
            elif (configurator.preRunCommands() and (not configurator.envPath())):
                raise TypeError("envPath")

            sessionTitle = configurator.sessionTitle()
            program = Path(configurator.programPath())
            dotGdb = Path(configurator.dotGdbPath()) if configurator.dotGdbPath() else None
            envPath = Path(configurator.envPath()) if configurator.envPath() else None
            preRunCommands = (configurator.preRunCommands()).split("\n") if configurator.preRunCommands() else None
        except TypeError as e:
            error = QMessageBox(QMessageBox.Icon.Critical, "Missing field", f"The following field is missing: {str(e)}", QMessageBox.StandardButton.Ok)
            error.exec()
            self.statusBar().showMessage("Invalid configuration. Please check your settings again.")

            return

        config = SGDBConfig(sessionTitle, program, dotGdb, envPath, preRunCommands)

        self.statusBar().showMessage("Starting up GDBMI...")
        self.launchGDBMI(config)

    def openConfig(self):
        if (self.running):
            QMessageBox(QMessageBox.Icon.Warning, "Running session", "An instance of GDB is already running. Make sure to terminate the current session before starting a new one.Another instance of", QMessageBox.StandardButton.Ok).exec()
            return

        self.__fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        openFilename = self.__fileDialog.getOpenFileName(dir=os.getcwd(), filter="JSON (*.json)")
        if (openFilename[0] == ""):
            return
        logger.debug(f"Using file {openFilename[0]}")
        try:
            currentConfig = SGDBConfigManager.load(Path(openFilename[0]))
        except ValueError as e:
            QMessageBox(QMessageBox.Icon.Critical, "Config error", f"An error occurred when loading {Path(openFilename[0]).name}: {str(e)}", QMessageBox.StandardButton.Ok).exec()
            return

        self.launchGDBMI(currentConfig)

    def launchGDBMI(self, config: SGDBConfig):
        logger.debug(f"Debugging program: {str(config.programPath)}")
        self.statusBar().showMessage(f"Initializing {config.sessionTitle}...")
        if (config.dotGdbPath is not None):
            logger.debug(f"GDB script: {str(config.dotGdbPath)}")

        # preRunCommands
        if (config.preRunCommands is not None):
            QMessageBox(QMessageBox.Icon.Information, "Pre-run commands", "Make sure to check the terminal for any input (eg. sudo)", QMessageBox.StandardButton.Ok).exec()
            for command in config.preRunCommands:
                logger.debug(f"Command {command}")
                ret = subprocess.call(command.split(" "), text=True, cwd=config.envPrefix)
                logger.debug(f"Command returned: {ret}")

                if (ret != 0):
                    logger.warning("ERROR when running commands. Check the output above")
                    return

        logger.success("preRunCommands OK!")

        gdbArgs = SGDBConfigManager.toGDBArgs(config)
        self.gdbMi = GdbMI(gdbArgs)
        self.model = SideModel(self.gdbMi)
        logger.success("GDB-MI initialization OK!")

        self.currentConfig = config

        self.setDebuggerUI(config)

        self.running = True
        self.statusBar().showMessage("Debugger launched.")

    def setDebuggerUI(self, config: SGDBConfig):
        self.miPrompt = MIPrompt(self.model)
        self.setCentralWidget(self.miPrompt)
        self.endQAction.toggled.connect(self.terminateSession)

        self.addToolBar(self.debugToolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.widgetsToolbar)

        # they may have been hidden
        self.debugToolbar.show()
        self.widgetsToolbar.show()

        self.setWindowTitle(f"{config.sessionTitle} - {self.appTitle}")

    def resetDebuggerUI(self):
        # reset the widgets toolbar buttons to OFF
        self.centralWidget().hide()
        self.debugToolbar.hide()
        self.widgetsToolbar.hide()

        self.miPrompt.reset()

        # reset widgets toolbar
        self.codeQAction.setChecked(False)
        self.disasmQAction.setChecked(False)
        self.varsQAction.setChecked(False)
        self.regsQAction.setChecked(False)

        self.setWindowTitle(self.appTitle)

    def closeEvent(self, event: QCloseEvent):
            logger.debug("Wooo i'm overriding the close event!!!")
            self.terminateSession()

            event.accept()

    def terminateSession(self):
        logger.debug("Terminating GDBMI...")

        try:
            self.gdbMi.terminate()
            self.gdbMi = None
            logger.success("GDBMI terminated.")

            self.resetDebuggerUI()

            self.running = False
            self.statusBar().showMessage("Debugger terminated.")
        except AttributeError:
            logger.debug("No GDBMI instance...")

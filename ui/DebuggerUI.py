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

from PySide6.QtCore import Qt
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

        self.setWindowTitle(f"{self.appTitle} Debugger")
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
        self.mainToolbar = QToolBar(self)
        self.mainToolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.newQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("bug--plus", FugueIconSize.FUGUE_32), "New")
        self.openQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("folder-horizontal-open", FugueIconSize.FUGUE_32), "Open")
        self.saveAsQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("disk-rename", FugueIconSize.FUGUE_32), "")
        self.saveQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("disk", FugueIconSize.FUGUE_32), "")
        self.endQAction = self.mainToolbar.addAction(QFugueManager.loadIcon("plug-disconnect-prohibition", FugueIconSize.FUGUE_32), "Terminate")
        self.saveAsQAction.setToolTip("Save As...")
        self.saveQAction.setToolTip("Save")

        # DEBUG TOOLBAR (CONTINUE, STEP)
        self.debugToolbar = QToolBar(self)
        self.debugToolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.breakPointsQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("table-delete-row", FugueIconSize.FUGUE_32), "Breakpoints")
        self.continueQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("control", FugueIconSize.FUGUE_32), "")
        self.stepOverQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("arrow-step-over", FugueIconSize.FUGUE_32), "")
        self.stepIntoQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("arrow-step", FugueIconSize.FUGUE_32), "")
        self.stepOutQAction = self.debugToolbar.addAction(QFugueManager.loadIcon("arrow-step-out", FugueIconSize.FUGUE_32), "")

        # WIDGETS TOOLBAR (SHOW/HIDE)
        self.widgetsToolbar = QToolBar(self)
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
        self.addToolBar(self.debugToolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.widgetsToolbar)

        self.__fileDialog = QFileDialog()
        self.__fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        self.newQAction.triggered.connect(self.spawnConfigureGDB)
        self.openQAction.triggered.connect(self.openConfig)
        self.endQAction.triggered.connect(self.terminateSession)

    def spawnConfigureGDB(self):
        self.statusBar().showMessage("Showing configuration")
        configurator = SideConfigurator(self, self.appTitle)
        if not configurator.exec():
            logger.warning("Bro quit. Doing nothing.")
            self.statusBar().showMessage("Configuration cancelled.")
            return

        # TODO: create GDB configuration
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
            logger.debug(preRunCommands)
        except TypeError as e:
            error = QMessageBox(QMessageBox.Icon.Critical, "Missing field", f"The following field is missing: {str(e)}", QMessageBox.StandardButton.Ok)
            error.exec()
            self.statusBar().showMessage("Invalid configuration. Please check your settings again.")

            return

        config = SGDBConfig(sessionTitle, program, dotGdb, envPath, preRunCommands)

        self.statusBar().showMessage("Starting up GDBMI...")
        self.launchGDBMI(config)

    def openConfig(self):
        openFilename = self.__fileDialog.getOpenFileName(dir=os.getcwd(), filter="JSON (*.json)")
        if (openFilename[0] == ""):
            return
        logger.debug(f"Using file {openFilename[0]}")
        try:
            currentConfig = SGDBConfigManager.load(Path(openFilename[0]))
        except ValueError as ex:
            traceback.print_exc()
            logger.debug(ex)
            logger.critical("Invalid configuration. Please choose a valid configuration file.")
            return

        self.launchGDBMI(currentConfig)

    def launchGDBMI(self, config: SGDBConfig):
        logger.debug(f"Debugging program: {str(config.programPath)}")
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

        # set up debugger UI
        self.setWindowTitle(f"{config.sessionTitle} - {self.appTitle}")
        self.setCentralWidget(MIPrompt(self.model))
        self.endQAction.triggered.connect(self.terminateSession)

        # show GDBMI prompt
        self.statusBar().showMessage("Debugger launched.")

    def closeEvent(self, event: QCloseEvent):
            logger.debug("Wooo i'm overriding the close event!!!")
            try:
                self.terminateSession()
            except AttributeError:
                logger.debug("No GDBMI instance...")

            event.accept()

    def terminateSession(self):
        logger.debug("Terminating GDBMI...")
        self.gdbMi.terminate()
        logger.success("GDBMI terminated.")
        self.statusBar().showMessage("Debugger terminated.")

        self.centralWidget().close()

import os
from pathlib import Path
from pprint import pformat
import subprocess
from typing import List, override
from loguru import logger

from assets.QFugueAssets import FugueIconSize, QFugueManager
from backend.SGDBConfig import SGDBConfig, SGDBConfigManager
from backend.GDBMI import GdbMI

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QToolBar

from backend.SideModel import SideModel
from ui.helpers.QtHelpers import Resettable
from ui.subwindows.AboutBox import AboutBox
from ui.subwindows.BreakManager import BreakManager
from ui.subwindows.CodeDock import CodeDock
from ui.subwindows.MIPrompt import MIPrompt
from ui.subwindows.SideConfigurator import SideConfigurator

class MainToolbar(QToolBar, Resettable):
    def __init__(self, title: str):
        super().__init__(title)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.newConfig = self.addAction(QFugueManager.loadIcon("bug--plus", FugueIconSize.FUGUE_32), "New")
        self.openConfig = self.addAction(QFugueManager.loadIcon("folder-horizontal-open", FugueIconSize.FUGUE_32), "Open")
        self.saveAsConfig = self.addAction(QFugueManager.loadIcon("disk-rename", FugueIconSize.FUGUE_32), "")
        # self.saveQAction = self.addAction(QFugueManager.loadIcon("disk", FugueIconSize.FUGUE_32), "")
        self.terminateDebug = self.addAction(QFugueManager.loadIcon("plug-disconnect-prohibition", FugueIconSize.FUGUE_32), "Terminate")
        self.saveAsConfig.setToolTip("Save As...")
        # self.saveQAction.setToolTip("Save")

class DebugToolbar(QToolBar, Resettable):
    def __init__(self, title: str):
        super().__init__(title)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.breakpointsMan = self.addAction(QFugueManager.loadIcon("table-delete-row", FugueIconSize.FUGUE_32), "Breakpoints")
        self.continueExec = self.addAction(QFugueManager.loadIcon("control", FugueIconSize.FUGUE_32), "")
        self.stepOver = self.addAction(QFugueManager.loadIcon("arrow-step-over", FugueIconSize.FUGUE_32), "")
        self.stepInto = self.addAction(QFugueManager.loadIcon("arrow-step", FugueIconSize.FUGUE_32), "")
        self.stepOut = self.addAction(QFugueManager.loadIcon("arrow-step-out", FugueIconSize.FUGUE_32), "")

class ShowHideToolbar(QToolBar, Resettable):
    def __init__(self, title: str):
        super().__init__(title)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.showCode = self.addAction(QFugueManager.loadIcon("script-code", FugueIconSize.FUGUE_32), "")
        self.showDisasm = self.addAction(QFugueManager.loadIcon("script-binary", FugueIconSize.FUGUE_32), "")
        self.showVars = self.addAction(QFugueManager.loadIcon("block", FugueIconSize.FUGUE_32), "")
        self.showRegs = self.addAction(QFugueManager.loadIcon("processor", FugueIconSize.FUGUE_32), "")
        self.showCode.setCheckable(True)
        self.showDisasm.setCheckable(True)
        self.showVars.setCheckable(True)
        self.showRegs.setCheckable(True)
        self.showCode.setToolTip("Show code")
        self.showDisasm.setToolTip("Show disassembly")
        self.showVars.setToolTip("Show variables")
        self.showRegs.setToolTip("Show registers")

    @override
    def reset(self):
        self.showCode.setChecked(False)
        self.showDisasm.setChecked(False)
        self.showVars.setChecked(False)
        self.showRegs.setChecked(False)

class DebuggerUI(QMainWindow):
    def __init__(self, appTitle: str):
        super().__init__()
        self.appTitle = appTitle or "pyDearGDB"     # easter egg

        self.setWindowTitle(self.appTitle)
        self.resize(1200, 800)

        self.resettables: List[Resettable] = []

        # MENU BAR
        menuBar = self.menuBar()
        fileQMenu = menuBar.addMenu("File")
        helpQMenu = menuBar.addMenu("Help")
        self.newSession = fileQMenu.addAction("New Session...")
        self.openSession = fileQMenu.addAction("Open configuration...")
        self.aboutProgram = helpQMenu.addAction(f"About{f" {appTitle}" if appTitle else ""}")

        self.mainToolbar = MainToolbar("Main toolbar")
        self.debugToolbar = DebugToolbar("Debugging toolbar")
        self.widgetsToolbar = ShowHideToolbar("Widgets toolbar")
        self.addToolBar(self.mainToolbar)

        self.codeDock = CodeDock()

        self.__fileDialog = QFileDialog()

        self.mainToolbar.newConfig.triggered.connect(self.showConfigureGDB)
        self.newSession.triggered.connect(self.showConfigureGDB)
        self.mainToolbar.openConfig.triggered.connect(self.openConfig)
        self.openSession.triggered.connect(self.openConfig)
        self.mainToolbar.saveAsConfig.triggered.connect(self.saveAs)
        self.mainToolbar.terminateDebug.triggered.connect(self.terminateSession)

        self.debugToolbar.breakpointsMan.triggered.connect(self.showBreakpointsManager)
        self.debugToolbar.continueExec.triggered.connect(self.sendContinue)
        self.debugToolbar.stepOver.triggered.connect(self.sendStepOver)
        self.debugToolbar.stepInto.triggered.connect(self.sendStepInto)
        self.debugToolbar.stepOut.triggered.connect(self.sendStepOut)

        self.aboutProgram.triggered.connect(self.showAboutBox)

        self.resettables.append(self.widgetsToolbar)

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

    def showConfigureGDB(self):
        if (self.running):
            QMessageBox(QMessageBox.Icon.Warning, "Running session", "An instance of GDB is already running. Make sure to terminate the current session before starting a new one.", QMessageBox.StandardButton.Ok).exec()
            return

        self.statusBar().showMessage("Showing configuration")
        configurator = SideConfigurator(self, self.appTitle)
        if not configurator.exec():
            logger.warning("Nothing.")
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

    def showAboutBox(self):
        aboutBox = AboutBox(self, self.appTitle)
        aboutBox.exec()

    def showBreakpointsManager(self):
        breakpointsManager = BreakManager(self, self.model)
        breakpointsManager.show()

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
        except Exception as e:
            logger.error(f"Error {type(e)} occurred when loading {Path(openFilename[0]).name}: {str(e)}")
            QMessageBox(QMessageBox.Icon.Critical, "Config error", f"Error {type(e)} occurred when loading {Path(openFilename[0]).name}: {str(e)}", QMessageBox.StandardButton.Ok).exec()
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

    def updateDebugger(self, threadInfo):
        logger.debug(pformat(threadInfo))

        threadId = threadInfo.get("currentThread")
        threads = threadInfo.get("threads")
        if ((threadId == 0) or ((not threads) or (type(threads) is not list))):
            return
        try:
            thread = threads[int(threadId) - 1]
        except ValueError as v:
            print(str(v))
            return

        frame = thread.get("frame", None)
        if (not frame):
            return

        self.codeDock.sgUpdate(frame)

    def sendContinue(self):
        threadInfo = self.model.continueExecution()
        self.updateDebugger(threadInfo)

    def sendStepOver(self):
        frame = self.model.stepOver()
        self.updateDebugger(frame)

    def sendStepInto(self):
        frame = self.model.stepInto()
        self.updateDebugger(frame)

    def sendStepOut(self):
        frame = self.model.stepOut()
        self.updateDebugger(frame)

    def setDebuggerUI(self, config: SGDBConfig):
        self.miPrompt = MIPrompt(self.model)
        self.setCentralWidget(self.miPrompt)
        self.mainToolbar.terminateDebug.toggled.connect(self.terminateSession)

        self.addToolBar(self.debugToolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.widgetsToolbar)

        # they may have been hidden
        self.debugToolbar.show()
        self.widgetsToolbar.show()

        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.codeDock)
        self.codeDock.setMinimumHeight(400)

        self.setWindowTitle(f"{config.sessionTitle} - {self.appTitle}")

    def resetDebuggerUI(self):
        # reset the widgets toolbar buttons to OFF
        self.centralWidget().close()
        self.debugToolbar.close()
        self.widgetsToolbar.close()
        self.codeDock.close()

        self.miPrompt.reset()

        # reset toolbars
        for resettable in self.resettables:
            resettable.reset()

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

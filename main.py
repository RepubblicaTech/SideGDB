import argparse
import sys

from PySide6.QtWidgets import QApplication

from ui.launcher.launcher_controller import LauncherController
from ui.launcher.launcher_view import LauncherView
from ui.main_controller import SGDBController
from ui.main_view import MainView

APPLICATION_TITLE = "SideGDB"

mainWindow: MainView
launcherView: LauncherView

if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainView(APPLICATION_TITLE)
    launcherView = LauncherView(mainWindow.mdiArea)
    launcherView.setGeometry(int((mainWindow.width() - 600) / 2),
                              int((mainWindow.height() - 400) / 2),
                              600,
                              400)
    launcherController = LauncherController(launcherView)
    sgdbController = SGDBController(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())

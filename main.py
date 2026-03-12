import argparse
import sys

from PySide6.QtWidgets import QApplication

from ui.launcher.launcher_controller import LauncherController
from ui.launcher.launcher_view import LauncherView
from ui.main_view import MainView
from ui.main_window_view import MainWindow

APPLICATION_TITLE = "SideGDB"

if __name__ == "__main__":
    ourParser = argparse.ArgumentParser(prog=sys.argv[0], description="A custom GDB TUI made in Python")
    ourParser.add_argument("-c", "--config", metavar="/path/to/config.yml", type=str, nargs=1, help="Path to a SideGDB configuration", required=False)
    parsedArgs = ourParser.parse_args()

    app = QApplication()
    mainWindow = MainWindow(APPLICATION_TITLE)
    launcherView = LauncherView(mainWindow.mdiArea)
    launcherView.setGeometry(int((mainWindow.width() - 600) / 2),
                              int((mainWindow.height() - 400) / 2),
                              600,
                              400)
    launcherController = LauncherController(launcherView)
    mainWindow.show()
    sys.exit(app.exec())

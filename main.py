import sys

from PySide6.QtWidgets import QApplication

from ui.launcher.LauncherController import LauncherController
from ui.launcher.LauncherView import LauncherView
from ui.MainView import MainView

APPLICATION_TITLE = "SideGDB"

if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainView(APPLICATION_TITLE)
    launcherView = LauncherView(mainWindow.mdiArea)
    launcherView.setGeometry(int((mainWindow.width() - 600) / 2),
                              int((mainWindow.height() - 400) / 2),
                              600,
                              400)
    launcherController = LauncherController(launcherView)
    mainWindow.show()
    sys.exit(app.exec())

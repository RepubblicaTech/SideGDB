import json
import logging
from PySide6.QtCore import QFile, QIODeviceBase, QTextStream
from PySide6.QtGui import QIcon
from loguru import logger

from PySide6.QtWidgets import QApplication, QMessageBox
from ui.DebuggerUI import DebuggerUI

APPLICATION_TITLE = "SideGDB"
ABOUTJSON_PATH = ":/app-assets/about"

if __name__ == "__main__":
    logger.info("Reset.")
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication([])
    windowIcon = QIcon("assets/sidegdb_logo.png")
    app.setWindowIcon(windowIcon)
    app.setApplicationName(APPLICATION_TITLE)
    window = DebuggerUI(APPLICATION_TITLE)

    aboutJson = QFile(ABOUTJSON_PATH)
    if (not aboutJson.open(QFile.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text)):
        logger.error("Missing about.json. Quitting.")
        window.close()
        app.exit(-1)

    f = QTextStream(aboutJson)
    obj = json.loads(f.readAll())

    semVersion = f"{obj["major"]}.{obj["minor"]}.{obj["patch"]}"
    if (obj.get("prerelease", None)):
        semVersion += f"-{obj["prerelease"]["version"]}.{obj["prerelease"]["id"]}"
        match (obj["prerelease"]["version"]):
            case "alpha":
                QMessageBox(QMessageBox.Icon.Warning,
                            "SideGDB development release",
                            "This is alpha software.\n"
                            "Do NOT report bugs to the developer as he might be fixing them right now...").exec()
            case _:
                QMessageBox(QMessageBox.Icon.Warning,
                            "SideGDB development release",
                            "This is beta/prerelease software.\n"
                            "Make sure to report any bugs on the repo's Issues tab.\n"
                            "https://github.com/RepubblicaTech/SideGDB/issues").exec()

    app.setApplicationVersion(semVersion)

    window.show()
    window.statusBar().showMessage("Ready.")

    app.exec()

import json
import logging
from PySide6.QtGui import QIcon
from loguru import logger

from PySide6.QtWidgets import QApplication, QMessageBox
from ui.DebuggerUI import DebuggerUI

APPLICATION_TITLE = "SideGDB"
ABOUTJSON_PATH = "assets/about.json"

if __name__ == "__main__":
    logger.info("Reset.")
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication([])
    windowIcon = QIcon("assets/sidegdb_logo.png")
    app.setWindowIcon(windowIcon)
    app.setApplicationName(APPLICATION_TITLE)
    window = DebuggerUI(APPLICATION_TITLE)

    with open(ABOUTJSON_PATH, "r") as f:
        obj = json.load(f)
        semVersion = f"{obj["major"]}.{obj["minor"]}.{obj["patch"]}"
        if (obj.get("prerelease", None)):
            semVersion += f"-{obj["prerelease"]["version"]}.{obj["prerelease"]["id"]}"
        app.setApplicationVersion(semVersion)

        if (obj.get("prerelease", None)):
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

    window.show()
    window.statusBar().showMessage("Ready.")

    app.exec()

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
    window = DebuggerUI(APPLICATION_TITLE)

    with open(ABOUTJSON_PATH, "r") as f:
        obj = json.load(f)
        if (obj.get("prerelease", None)):
            QMessageBox(QMessageBox.Icon.Warning,
                        "SideGDB development release",
                        "This is alpha/prerelease software.\n"
                        "It might be subject to unknown bugs or straight up crashes/hangups.\n"
                        "Do NOT report these issues as the developer might be fixing them.").exec()

    window.show()
    window.statusBar().showMessage("Ready.")

    app.exec()

import logging
from PySide6.QtGui import QIcon
from loguru import logger

from PySide6.QtWidgets import QApplication
from ui.DebuggerUI import DebuggerUI

APPLICATION_TITLE = "SideGDB"

if __name__ == "__main__":
    logger.info("Reset.")
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication([])
    windowIcon = QIcon("assets/sidegdb_logo.png")
    app.setWindowIcon(windowIcon)
    window = DebuggerUI(APPLICATION_TITLE)
    window.show()
    window.statusBar().showMessage("Ready.")

    app.exec()

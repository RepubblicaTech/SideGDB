import logging
from loguru import logger

from PySide6.QtWidgets import QApplication
from ui.DebuggerUI import DebuggerUI

APPLICATION_TITLE = "SideGDB"

if __name__ == "__main__":
    logger.info("Reset.")
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication([])
    window = DebuggerUI(APPLICATION_TITLE)
    window.show()
    window.statusBar().showMessage("Ready.")

    app.exec()

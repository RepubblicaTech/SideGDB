from loguru import logger
from PySide6.QtWidgets import QApplication

from ui.DebuggerUI import DebuggerUI

APPLICATION_TITLE = "SideGDB"

if __name__ == "__main__":
    logger.info("Reset.")

    app = QApplication([])
    window = DebuggerUI(APPLICATION_TITLE)
    window.show()
    app.exec()

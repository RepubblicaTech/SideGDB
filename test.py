import argparse
import sys

import pprint
from loguru import logger as console
from misc import misc

from PySide6.QtWidgets import QApplication
from ui.gallery_test import WidgetGallery

APPLICATION_NAME = "SideGDB"

if __name__ == "__main__":
    app = QApplication()
    view = WidgetGallery()
    view.show()
    sys.exit(app.exec())

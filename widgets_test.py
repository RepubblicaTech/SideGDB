import sys

from PySide6.QtWidgets import QApplication
from ui.GalleryTest import WidgetGallery

if __name__ == "__main__":
    app = QApplication()
    view = WidgetGallery()
    view.show()
    sys.exit(app.exec())

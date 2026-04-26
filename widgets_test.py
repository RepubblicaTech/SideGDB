import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from ui.subwindows.CodeDock import CodeDock

if __name__ == "__main__":
    app = QApplication()
    # view = WidgetGallery()
    # view.show()

    view = QMainWindow()
    view.resize(800, 400)
    codeDock = CodeDock()
    view.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, codeDock)
    view.show()
    sys.exit(app.exec())

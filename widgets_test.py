import sys

from PySide6.QtCore import QAbstractItemModel
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
from ui.GalleryTest import WidgetGallery

class AnotherTest(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 500)

        model = QStandardItemModel(0, 2)
        model.setHorizontalHeaderLabels(["No.", "Where[file:line]"])
        for i in range(5):
            item1 = QStandardItem(f"Item {i}")
            item2 = QStandardItem(f"Value {i * 10}")
            model.appendRow([item1, item2])

        view = QTableView()
        view.setModel(model)
        view.resizeColumnsToContents()

        layout = QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication()
    view = WidgetGallery()
    view2 = AnotherTest()
    view.show()
    view2.show()
    sys.exit(app.exec())

from PySide6 import QtWidgets

class LauncherView(QtWidgets.QMdiSubWindow):
    def __init__(self, /, parent: QtWidgets.QMdiArea):
        super().__init__(parent)

        if (parent.parent() is None):
            self.windowParent = parent
        else:
            self.windowParent = parent.parent()

        self.setWindowTitle("SideGDB Launcher")
        self.resize(600, 400)

        self.createButton = QtWidgets.QPushButton("New GDB Session...")
        self.openButton = QtWidgets.QPushButton("Open GDB Session...")

        self.sessionsList = QtWidgets.QListWidget()
        self.sessionsList.addItem("Session name [path to config]")

        self.mainWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.createButton, 0, 0)
        self.gridLayout.addWidget(self.openButton, 1, 0)
        self.gridLayout.addWidget(QtWidgets.QLabel("Recent Sessions:"), 0, 1)
        self.gridLayout.addWidget(self.sessionsList, 1, 1, 2, 1)
        self.mainWidget.setLayout(self.gridLayout)

        self.setWidget(self.mainWidget)

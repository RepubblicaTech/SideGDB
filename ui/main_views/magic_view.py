from PySide6 import QtWidgets

class MagicView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magic window")

    def initWidgets(self):
        self.magicInput = QtWidgets.QLineEdit()
        self.magicButton = QtWidgets.QPushButton("Buttn :)")
        self.scrollArea = QtWidgets.QScrollArea()
        self.magicTextArea = QtWidgets.QTextEdit()

    def showWidgets(self):
        self.mainContainer = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainContainer)
        self.upperBox = QtWidgets.QWidget()
        self.upperLayout = QtWidgets.QHBoxLayout(self.upperBox)

        self.magicTextArea.setReadOnly(True)

        self.scrollArea.setWidget(self.magicTextArea)
        self.scrollArea.setWidgetResizable(True)
        self.magicTextArea.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.upperLayout.addWidget(self.magicInput)
        self.upperLayout.addWidget(self.magicButton)

        self.mainLayout.addWidget(self.upperBox)
        self.mainLayout.addWidget(self.scrollArea)

        self.setCentralWidget(self.mainContainer)
        self.setLayout(self.mainLayout)

        self.magicInput.setPlaceholderText("Insert a GDB-MI command here...")
        self.magicTextArea.setPlaceholderText("Response gets printed here...")

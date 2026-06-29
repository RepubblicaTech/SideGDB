import json
from venv import logger
from PySide6.QtCore import QFile, QIODeviceBase, QTextStream, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication

ABOUTJSON_PATH = ":/app-assets/about"

class AboutBox(QDialog):
    def __init__(self, parent: QWidget, appTitle: str):
        super().__init__(parent)
        self.appTitle = appTitle or "SideGDB"
        self.setWindowTitle(f"About {appTitle}")
        self.setFixedSize(450,300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        banner = QLabel()
        banner.setPixmap(QPixmap(":/app-assets/banner").scaledToWidth(self.width() - 10, Qt.TransformationMode.SmoothTransformation))

        aboutJson = QFile(ABOUTJSON_PATH)
        if (not aboutJson.open(QFile.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text)):
            logger.error("Missing about.json. Quitting.")
            return
        f = QTextStream(aboutJson)
        obj = json.loads(f.readAll())
        codeName = obj["codename"] or ""

        aboutLabel = QLabel(f"{self.appTitle} {codeName}\nVersion {QApplication.instance().applicationVersion()}")
        creditsLabel = QLabel("Some icons by <a href=\"http://p.yusukekamiyamane.com/\">Yusuke Kamiyamane</a>")
        creditsLabel.setTextFormat(Qt.TextFormat.RichText)
        creditsLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        creditsLabel.setOpenExternalLinks(True)

        okButton = QPushButton("Ok")
        okButton.clicked.connect(self.accept)

        layout.addWidget(banner, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(aboutLabel)
        layout.addStretch()
        layout.addWidget(creditsLabel)
        layout.addWidget(okButton, alignment=Qt.AlignmentFlag.AlignRight)

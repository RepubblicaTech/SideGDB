import json
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QWidget

ABOUTJSON_PATH = "assets/about.json"

class AboutBox(QDialog):
    def __init__(self, parent: QWidget, appTitle: str):
        super().__init__(parent)
        self.appTitle = appTitle or "SideGDB"
        self.setWindowTitle(f"About {appTitle}")
        self.setFixedSize(600,400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        banner = QLabel()
        banner.setPixmap(QPixmap("assets/sidegdb_banner.png").scaledToWidth(575, Qt.TransformationMode.SmoothTransformation))

        # json thingies
        codeName = ""
        semVersion = ""
        with open(ABOUTJSON_PATH, "r") as f:
            obj = json.load(f)
            codeName = obj["codename"] or ""
            semVersion = f"{obj["major"]}.{obj["minor"]}.{obj["patch"]}"
            if (obj.get("prerelease", None)):
                semVersion += f"-{obj["prerelease"]["version"]}.{obj["prerelease"]["id"]}"

        aboutLabel = QLabel(f"{self.appTitle} {codeName}\nv{semVersion}")
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

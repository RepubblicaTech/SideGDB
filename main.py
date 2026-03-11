import argparse
import sys

from PySide6.QtWidgets import QApplication

from ui.main_view import MainView

APPLICATION_TITLE = "SideGDB"

if __name__ == "__main__":
    ourParser = argparse.ArgumentParser(prog=sys.argv[0], description="A custom GDB TUI made in Python")
    ourParser.add_argument("-c", "--config", metavar="/path/to/config.yml", type=str, nargs=1, help="Path to a SideGDB configuration", required=False)
    parsedArgs = ourParser.parse_args()

    app = QApplication()
    mainView = MainView(APPLICATION_TITLE)
    mainView.show()
    sys.exit(app.exec())

# Custom class for loading Fugue Icons
# (i kinda wanted to make it more abstract but it's just too much for now)

from enum import IntEnum

from PySide6.QtGui import QIcon
from assets_helpers import assets

class FugueIconSize(IntEnum):
    FUGUE_NORMAL = 0
    FUGUE_24 = 3
    FUGUE_32 = 4

ASSETS_PREFIX = "assets/"

class QFugueManager:
    @staticmethod
    def loadIcon(iconName: str, iconSize: FugueIconSize = FugueIconSize.FUGUE_NORMAL, shadowless: bool = False):
        resourcePrefix = f"fugue{f"-{iconSize * 8}" if iconSize is not FugueIconSize.FUGUE_NORMAL else ""}"

        return QIcon(f":/{resourcePrefix}/{iconName}")

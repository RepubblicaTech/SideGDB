# Custom class for loading Fugue Icons
# (i kinda wanted to make it more abstract but it's just too much for now)

from enum import Enum
from pathlib import Path
from PySide6.QtGui import QIcon
from loguru import logger

class FugueIconSize(Enum):
    FUGUE_NORMAL = 0
    FUGUE_24 = 1
    FUGUE_32 = 2

ASSETS_PREFIX = "assets/"

class QFugueManager:
    @staticmethod
    def loadIcon(iconName: str, iconSize: FugueIconSize = FugueIconSize.FUGUE_NORMAL, shadowless: bool = False):
        # assemble a first path
        match (iconSize):
            case FugueIconSize.FUGUE_NORMAL:
                pathToLoad = f"{ASSETS_PREFIX}fugue/icons{"-shadowless" if shadowless else ""}/{iconName}.png"
            case FugueIconSize.FUGUE_24:
                pathToLoad = f"{ASSETS_PREFIX}fugue/icons{"-shadowless" if shadowless else ""}-24/{iconName}.png"
            case FugueIconSize.FUGUE_32:
                pathToLoad = f"{ASSETS_PREFIX}fugue/icons{"-shadowless" if shadowless else ""}-32/{iconName}.png"
                if (not Path(pathToLoad).exists()):
                    pathToLoad = f"{ASSETS_PREFIX}fugue-2x/icons{"-shadowless" if shadowless else ""}/{iconName}.png"

        logger.debug(f"Loading {pathToLoad}")

        if (not Path(pathToLoad).exists()):
            logger.warning(f"Icon {iconName} not found")
            return QIcon()

        return QIcon(pathToLoad)

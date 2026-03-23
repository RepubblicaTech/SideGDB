from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import List, Optional

@dataclass
class Config:
    sessionTitle: str

    programPath: Path
    dotGdbPath: Optional[Path]

    envPrefix: Optional[Path]
    preRunCommands: Optional[List[str]] = field(default_factory=list)

# Perplexity
class SideConfigManager:
    @staticmethod
    def load(config_path: Path) -> Config:
        if (not config_path.exists()):
            raise FileNotFoundError(f"Missing file {str(config_path)}")
        with open(config_path) as f:
            data = json.load(f)

        configDict = dict(data)

        if (configDict.get("programPath") is None):
            raise ValueError("No program path has been given")
        elif ((configDict.get("preRunCommands") is not None) and (configDict.get("envPrefix") is None)):
            raise ValueError("An environment path must be given for pre-run commands")

        return Config(**data)

    @staticmethod
    def toGDBArgs(config: Config):
        if (not Path(config.programPath).exists()):
            return None

        gdbArgs: list = [config.programPath]

        if (config.dotGdbPath is not None):
            gdbArgs.extend(["-x" , str(config.dotGdbPath)])

    @staticmethod
    def save(config: Config, config_path: Path):
        data = asdict(config)
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)

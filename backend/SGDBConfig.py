from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any, List, Optional

@dataclass
class SGDBConfig:
    sessionTitle: str

    programPath: Path
    dotGdbPath: Optional[Path]

    envPrefix: Optional[Path]
    preRunCommands: Optional[List[str]] = field(default_factory=list)

class SGDBConfigEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, Path):
            return str(o)
        return super().default(o)

# Perplexity
class SGDBConfigManager:
    @staticmethod
    def load(config_path: Path) -> SGDBConfig:
        if (not config_path.exists()):
            raise FileNotFoundError(f"Missing file {str(config_path)}")
        with open(config_path) as f:
            data = json.load(f)

        configDict = dict(data)

        if (configDict.get("programPath") is None):
            raise ValueError("No program path has been given")
        elif ((configDict.get("preRunCommands") is not None) and (configDict.get("envPrefix") is None)):
            raise ValueError("An environment path must be given for pre-run commands")

        return SGDBConfig(**data)

    @staticmethod
    def toGDBArgs(config: SGDBConfig):
        if (not Path(config.programPath).exists()):
            return None

        gdbArgs: list = [str(config.programPath)]

        if (config.dotGdbPath is not None):
            gdbArgs.extend(["-x" , str(config.dotGdbPath)])

        return gdbArgs

    @staticmethod
    def save(config: SGDBConfig, savePath: Path):
        data = asdict(config)

        with savePath.open("w") as f:
            json.dump(data, f, indent=2, cls=SGDBConfigEncoder)

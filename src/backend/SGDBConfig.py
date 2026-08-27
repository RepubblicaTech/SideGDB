import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import override


@dataclass
class SGDBConfig:
    sessionTitle: str

    programPath: Path
    dotGdbPath: Path | None

    envPrefix: Path | None
    preRunCommands: list[str] | None = field(default_factory=list)

class SGDBConfigEncoder(json.JSONEncoder):
    @override
    def default(self, o):
        if isinstance(o, Path):
            return str(o)
        return super().default(o)

# Perplexity
class SGDBConfigManager:
    @staticmethod
    def load(config_path: Path) -> SGDBConfig:
        if (not config_path.exists()):
            raise FileNotFoundError(f"Missing file {config_path!s}")
        with open(config_path) as f:
            data = json.load(f)

        configDict = dict(data)

        if (configDict.get("programPath") is None):
            raise ValueError("No program path has been given")
        elif (not Path(str(configDict.get("programPath"))).exists()):
            raise FileNotFoundError("Program path is non-existent.")
        elif ((configDict.get("preRunCommands") is not None) and (configDict.get("envPrefix") is None)):
            raise ValueError("An environment path must be given for pre-run commands")

        return SGDBConfig(**data)

    @staticmethod
    def toGDBArgs(config: SGDBConfig):
        if (not Path(config.programPath).exists()):
            return None

        gdbArgs: list[str] = [str(config.programPath)]

        if (config.dotGdbPath is not None):
            gdbArgs.extend(["-x" , str(config.dotGdbPath)])

        return gdbArgs

    @staticmethod
    def save(config: SGDBConfig, savePath: Path):
        data = asdict(config)

        with savePath.open("w") as f:
            json.dump(data, f, indent=2, cls=SGDBConfigEncoder)

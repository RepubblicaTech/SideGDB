from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import List, Optional

@dataclass
class SGDBConfig:
    sessionTitle: str

    programPath: Path
    dotGdbPath: Optional[Path]

    envPrefix: Optional[Path]
    preRunCommands: Optional[List[str]] = field(default_factory=list)

# Perplexity
class ConfigManager:
    @staticmethod
    def load(config_path: Path) -> SGDBConfig:
        with open(config_path) as f:
            data = json.load(f)

        return SGDBConfig(**data)

    @staticmethod
    def save(config: SGDBConfig, config_path: Path):
        data = asdict(config)
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)

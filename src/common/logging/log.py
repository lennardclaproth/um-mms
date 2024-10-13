from dataclasses import dataclass, field
from typing import Dict, Any
import json
from cryptography.fernet import Fernet


@dataclass
class Log:
    level: str
    str_repr: str
    message: str
    timestamp: str
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        j = json.dumps({
            "level": self.level,
            "str_repr": self.str_repr,
            "message": self.message,
            "timestamp": self.timestamp,
            "kwargs": self.kwargs
        })
        return j

    @staticmethod
    def from_json(json_str: str) -> 'Log':
        data = json.loads(json_str)

        return Log(level=data["level"], str_repr=data["str_repr"], message=data["message"], timestamp=data["timestamp"], kwargs=data["kwargs"])

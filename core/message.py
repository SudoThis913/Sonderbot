# core/models.py

from dataclasses import dataclass, field
from typing import Optional
import datetime

@dataclass
class Message:
    host_id: str
    hostname: str
    channel: str
    user: str
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    def __str__(self):
        return f"[{self.timestamp.isoformat()}] <{self.user}@{self.channel}>: {self.content}"

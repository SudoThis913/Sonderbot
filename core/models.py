# core/models.py

from dataclasses import dataclass, field
from typing import Optional, Literal, DefaultDict, List, Dict
from pydantic import BaseModel
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


@dataclass
class ConnectionConfig(BaseModel):
    host_id: str
    protocol: Literal["irc", "discord"]
    hostname: Optional[str] = None
    port: Optional[int] = None
    use_ssl: bool = True
    botnick: Optional[str] = None
    botnick2: Optional[str] = None
    botnick3: Optional[str] = None
    botpass: Optional[str] = None
    token: Optional[str] = None  # For Discord bots
    default_channel: Optional[str] = None
    chanserv_user: Optional[str] = None
    chanserv_pass: Optional[str] = None
    extra_channels: Optional[List[str]] = None
    channels: Optional[Dict[str, List[str]]] = None  # key = channel, value = list of apps names

    def is_irc(self) -> bool:
        return self.protocol == "irc"

    def is_discord(self) -> bool:
        return self.protocol == "discord"

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
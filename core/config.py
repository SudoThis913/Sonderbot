# core/config.py

import json
from typing import List, Dict, Optional
from pydantic import BaseModel
from core.secrets import resolve_secret

class ConnectionConfig(BaseModel):
    host_id: str
    protocol: str
    hostname: str
    port: int
    use_ssl: Optional[bool] = True
    botnick: str
    botnick2: Optional[str] = None
    botnick3: Optional[str] = None
    botpass: Optional[str] = None
    default_channel: Optional[str] = None
    chanserv_user: Optional[str] = None
    chanserv_pass: Optional[str] = None
    extra_channels: Optional[List[str]] = []
    channels: Optional[Dict[str, List[str]]] = {}
    channel_defaults: Optional[Dict[str, List[str]]] = {}
    host_defaults: Optional[List[str]] = []
    protocol_defaults: Optional[List[str]] = []
    trigger_char: Optional[str] = "!"

    def is_irc(self) -> bool:
        return self.protocol.lower() == "irc"

    def resolve_secrets(self):
        self.botpass = resolve_secret(self.botpass, f"{self.protocol}/{self.hostname}/botpass")
        self.chanserv_pass = resolve_secret(self.chanserv_pass, f"{self.protocol}/{self.hostname}/chanserv")

def load_config(path="data/config.json") -> List[ConnectionConfig]:
    with open(path, "r") as f:
        data = json.load(f)
        connections = [ConnectionConfig(**conn) for conn in data.get("connections", [])]
        for conn in connections:
            conn.resolve_secrets()
        return connections


# (Optional) numeric handler decorator for IRC responses
dispatch_table = {}

def numeric_handler(code):
    def wrapper(fn):
        dispatch_table[str(code)] = fn
        return fn
    return wrapper

async def dispatch_numeric_response(conn, parts):
    handler = dispatch_table.get(parts[1])
    if handler:
        await handler(conn, parts)

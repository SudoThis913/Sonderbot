# core/session_manager.py

import asyncio
from core.config import load_config, ConnectionConfig
from core.db import DatabaseManager
from core.session_queues import SessionQueues
from core.app_manager import AppManager
from protocols.irc import IRCConnection
from core.logger import setup_logger

logger = setup_logger("session")

class SessionManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.queues = SessionQueues()
        self.app_manager = AppManager()
        self.connections: list[IRCConnection] = []
        self.queue_lookup = {}

    async def start_all(self):
        await self.db.initialize()
        configs = load_config()

        for config in configs:
            queue = self.queues.get(config.host_id)
            self.queue_lookup[config.host_id] = queue

            if config.is_irc():
                connection = IRCConnection(config, queue)
                self.connections.append(connection)

                # Resolve default apps: channel > host > protocol > fallback
                global_defaults = ["db"]
                protocol_defaults = config.protocol_defaults if hasattr(config, "protocol_defaults") else []
                host_defaults = config.host_defaults if hasattr(config, "host_defaults") else []
                channel_map = config.channels or {}

                for chan, apps in channel_map.items():
                    chan_defaults = config.channel_defaults.get(chan, []) if hasattr(config, "channel_defaults") else []
                    combined_apps = list(dict.fromkeys(chan_defaults + host_defaults + protocol_defaults + global_defaults + apps))
                    await self.app_manager.load_apps(config.host_id, chan, combined_apps)

        tasks = [conn.connect() for conn in self.connections]
        await asyncio.gather(*tasks)

    async def shutdown(self):
        for conn in self.connections:
            await conn.disconnect()
        await self.db.close()
        await self.app_manager.unload_all()

    async def dispatch_message(self, message):
        await self.app_manager.dispatch_message(message)

    async def tick_all(self):
        await self.app_manager.tick_all()

    async def send_direct(self, host_id: str, channel: str, content: str):
        queue = self.queue_lookup.get(host_id)
        if not queue:
            logger.warning(f"No queue for host: {host_id}")
            return

        from core.models import Message
        msg = Message(
            host_id=host_id,
            hostname=host_id,
            channel=channel,
            user="cli",
            content=content
        )
        await queue.put_outgoing(msg)

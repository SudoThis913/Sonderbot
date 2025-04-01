# apps/dblogger/dblogger.py

from core.models import Message
from core.db import DatabaseManager
from core.sonderbot_app import SonderbotApp

class DBLoggerApp(SonderbotApp):

    @classmethod
    def friendly_name(cls) -> str:
        return "db_logger"

    @classmethod
    def module_name(cls): return "dblogger"

    def __init__(self, channel: str, host_id: str):
        super().__init__(channel, host_id)
        self.db = DatabaseManager()

    async def setup(self):
        # Could be used to open connections or perform migrations
        pass

    async def teardown(self):
        # Close any open resources (none required here for pooled access)
        pass

    async def on_message(self, message: Message):
        await self.db.log_irc_message(
            host_id=message.host_id,
            hostname=message.hostname,
            channel=message.channel,
            user=message.user,
            content=message.content
        )

    async def on_command(self, message: Message, command: str, args: str):
        # This apps does not respond to commands by default
        pass

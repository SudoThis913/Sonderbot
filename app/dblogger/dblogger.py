# apps/dblogger.py

from core.sonderbot_app import SonderbotApp
from core.models import Message
from core.db import DatabaseManager

class App(SonderbotApp):
    def __init__(self, channel: str, host_id: str):
        super().__init__(channel, host_id)
        self.db = DatabaseManager()

    async def setup(self):
        await self.db.initialize()

    async def on_message(self, message: Message):
        await self.db.log_message(
            host_id=message.host_id,
            hostname=message.hostname,
            channel=message.channel,
            user=message.user,
            message=message.content
        )

    async def on_command(self, message: Message, command: str, args: str):
        pass  # dblogger does not respond to commands

    async def teardown(self):
        await self.db.close()

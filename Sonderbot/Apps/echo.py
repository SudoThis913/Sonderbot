# apps/echo.py

from core.sonderbot_app import SonderbotApp
from core.models import Message

class App(SonderbotApp):
    async def setup(self):
        pass

    async def on_message(self, message: Message):
        if message.content.startswith("!echo"):
            content = message.content[5:].strip()
            if content:
                await message.reply(f"Echo: {content}")

    async def teardown(self):
        pass
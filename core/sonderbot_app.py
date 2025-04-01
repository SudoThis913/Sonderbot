# core/sonderbot_app.py

from abc import ABC, abstractmethod
from core.models import Message

class SonderbotApp(ABC):

    def __init__(self, channel: str, host_id: str):
        self.channel = channel
        self.host_id = host_id
        self.enabled = True  # apps can opt-out of processing if needed

    @classmethod
    def friendly_name(cls) -> str:
        return "base_class"
    @abstractmethod
    async def setup(self):
        """Prepare the app (DB access, caches, etc)"""
        pass

    @abstractmethod
    async def on_message(self, message: Message):
        """Handle an incoming message."""
        pass

    @abstractmethod
    async def teardown(self):
        """Cleanup when the app is unloaded."""
        pass

    async def on_tick(self):
        """Optional: periodic update (e.g., reminders, cleanups)."""
        pass

    async def on_command(self, message: Message, command: str, args: str):
        """Optional: handle !commands sent to the channel."""
        pass

    def should_handle(self, message: Message) -> bool:
        """Apps can override this to filter messages before processing."""
        return self.enabled and message.channel == self.channel and message.host_id == self.host_id

    async def handle(self, message: Message):
        """Entry point to route messages through command or default handling."""
        if not self.should_handle(message):
            return

        if message.content.startswith("!"):
            split = message.content[1:].split(maxsplit=1)
            command = split[0]
            args = split[1] if len(split) > 1 else ""
            await self.on_command(message, command, args)
        else:
            await self.on_message(message)

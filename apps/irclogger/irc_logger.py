# apps/irclogger/irc_logger.py

import os
import re
from datetime import datetime
from core.models import Message
from core.sonderbot_app import SonderbotApp

SAFE_FILENAME = re.compile(r'[^\w\-#]+')

def sanitize(text: str) -> str:
    return text.replace('\n', ' ').replace('\r', ' ').strip()

def safe_filename(name: str) -> str:
    return SAFE_FILENAME.sub('_', name)

class IRCLogger(SonderbotApp):
    @classmethod
    def friendly_name(cls) -> str:
        return "irc_logger"

    @classmethod
    def module_name(cls):
        return "irc_logger"

    async def setup(self):
        host_dir = os.path.join("data", "irc", safe_filename(self.host_id))
        os.makedirs(host_dir, exist_ok=True)
        chan_file = safe_filename(self.channel) + ".log"
        self.path = os.path.join(host_dir, chan_file)

    async def handle(self, message: Message):
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] <{message.user}> {sanitize(message.content)}\n"
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            print(f"[irclog] Failed to write: {e}")

    async def teardown(self):
        pass

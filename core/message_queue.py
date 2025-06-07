# core/message_queue.py

import asyncio
from core.models import Message

class MessageQueue:
    def __init__(self):
        self._incoming: asyncio.Queue[Message] = asyncio.Queue()
        self._outgoing: asyncio.Queue[Message] = asyncio.Queue()

    async def put_incoming(self, msg: Message):
        await self._incoming.put(msg)

    async def get_incoming(self) -> Message:
        return await self._incoming.get()

    async def put_outgoing(self, msg: Message):
        await self._outgoing.put(msg)

    async def get_outgoing(self) -> Message:
        return await self._outgoing.get()

    def incoming_empty(self) -> bool:
        return self._incoming.empty()

    def outgoing_empty(self) -> bool:
        return self._outgoing.empty()

    def clear(self):
        while not self._incoming.empty():
            self._incoming.get_nowait()
        while not self._outgoing.empty():
            self._outgoing.get_nowait()

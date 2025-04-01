# core/session_queues.py

from typing import Dict
from core.message_queue import MessageQueue

class SessionQueues:
    def __init__(self):
        self._queues: Dict[str, MessageQueue] = {}

    def get(self, session_id: str) -> MessageQueue:
        if session_id not in self._queues:
            self._queues[session_id] = MessageQueue()
        return self._queues[session_id]

    def has(self, session_id: str) -> bool:
        return session_id in self._queues

    def all(self) -> Dict[str, MessageQueue]:
        return self._queues

    def remove(self, session_id: str) -> bool:
        return self._queues.pop(session_id, None) is not None

    def clear_all(self):
        for mq in self._queues.values():
            mq.clear()
        self._queues.clear()

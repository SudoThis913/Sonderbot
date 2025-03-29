# core/session_queues.py

from typing import Dict
from core.message_queue import MessageQueue

class SessionQueues:
    def __init__(self):
        self._queues: Dict[str, MessageQueue] = {}

    def get(self, session_id: str) -> MessageQueue:
        """
        Returns the MessageQueue for the given session_id, creating one if it doesn't exist.
        """
        if session_id not in self._queues:
            self._queues[session_id] = MessageQueue()
        return self._queues[session_id]

    def has(self, session_id: str) -> bool:
        """
        Check if a queue exists for the given session_id.
        """
        return session_id in self._queues

    def all(self) -> Dict[str, MessageQueue]:
        """
        Returns all session queues.
        """
        return self._queues

    def remove(self, session_id: str) -> bool:
        """
        Removes a session queue. Returns True if removed, False if not found.
        """
        return self._queues.pop(session_id, None) is not None

    def clear_all(self):
        """
        Clears and removes all queues.
        """
        for mq in self._queues.values():
            mq.clear()
        self._queues.clear()

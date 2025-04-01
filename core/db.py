# core/db.py

import aiosqlite
import asyncio
import datetime
from pathlib import Path
from typing import Optional, Any

DB_PATH = Path("data/sonderbot.db")


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._pool: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()

    async def initialize(self):
        async with self._lock:
            if not self._pool:
                self._pool = await aiosqlite.connect(self.db_path)
                await self._pool.execute("PRAGMA journal_mode=WAL;")
                await self._setup_tables()
                await self._pool.commit()

    async def _setup_tables(self):
        await self._pool.execute("""
            CREATE TABLE IF NOT EXISTS IRCLOG (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TIMESTAMP TEXT NOT NULL,
                HOSTID TEXT NOT NULL,
                HOSTNAME TEXT NOT NULL,
                CHANNEL TEXT,
                USER TEXT,
                MESSAGE TEXT
            )
        """)

        await self._pool.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CONTYPE TEXT NOT NULL,
                HOSTNAME TEXT NOT NULL,
                USER TEXT NOT NULL,
                ACCESS INTEGER
            )
        """)

    async def log_message(self, host_id: str, hostname: str, channel: str, user: str, message: str):
        timestamp = datetime.datetime.utcnow().isoformat()
        async with self._lock:
            await self._pool.execute("""
                INSERT INTO IRCLOG (TIMESTAMP, HOSTID, HOSTNAME, CHANNEL, USER, MESSAGE)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, host_id, hostname, channel, user, message))
            await self._pool.commit()

    async def query_logs(self, hostname: str, channel: str, limit: int = 100):
        async with self._lock:
            cursor = await self._pool.execute("""
                SELECT * FROM IRCLOG
                WHERE HOSTNAME = ? AND CHANNEL = ?
                ORDER BY TIMESTAMP DESC
                LIMIT ?
            """, (hostname, channel, limit))
            return await cursor.fetchall()

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

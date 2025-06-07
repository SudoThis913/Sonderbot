# core/acl.py

import aiosqlite

DEFAULT_GROUPS = {
    "administrators": 100,
    "users": 10,
    "banned": 0,
    "ignore": -1
}

class ACLManager:
    def __init__(self, db):
        self.db = db

    async def initialize(self):
        await self.db.connection.execute("""
        CREATE TABLE IF NOT EXISTS ACL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            protocol TEXT NOT NULL,
            hostname TEXT NOT NULL,
            channel TEXT,
            username TEXT NOT NULL,
            permission TEXT NOT NULL
        )""")

        await self.db.connection.execute("""
        CREATE TABLE IF NOT EXISTS ACLGroups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL UNIQUE,
            priority INTEGER NOT NULL
        )""")

        await self.db.connection.execute("""
        CREATE TABLE IF NOT EXISTS ACLGroupMembers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            protocol TEXT NOT NULL,
            hostname TEXT NOT NULL,
            channel TEXT,
            username TEXT NOT NULL,
            group_name TEXT NOT NULL
        )""")

        for group, priority in DEFAULT_GROUPS.items():
            await self.db.connection.execute(
                "INSERT OR IGNORE INTO ACLGroups (group_name, priority) VALUES (?, ?)",
                (group, priority)
            )

    async def check(self, username, protocol, hostname, channel, permission):
        query = """
        SELECT 1 FROM ACL WHERE
            protocol = ? AND hostname = ? AND username = ? AND permission = ?
            AND (channel = ? OR channel IS NULL)
        LIMIT 1
        """
        async with self.db.execute(query, (protocol, hostname, username, permission, channel)) as cursor:
            result = await cursor.fetchone()
            return result is not None

    async def get_groups(self, username, protocol, hostname, channel=None):
        query = """
        SELECT group_name FROM ACLGroupMembers WHERE
            protocol = ? AND hostname = ? AND username = ?
            AND (channel = ? OR channel IS NULL)
        """
        async with self.db.execute(query, (protocol, hostname, username, channel)) as cursor:
            return [row[0] async for row in cursor]

    async def in_group(self, username, group_name, protocol, hostname, channel=None):
        query = """
        SELECT 1 FROM ACLGroupMembers WHERE
            group_name = ? AND protocol = ? AND hostname = ? AND username = ?
            AND (channel = ? OR channel IS NULL)
        LIMIT 1
        """
        async with await self.db.connection.execute(query, (group_name, protocol, hostname, username, channel)) as cursor:
            return await cursor.fetchone() is not None

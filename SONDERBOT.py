import asyncio
import functools
import logging
import sys


class botState():
    botConnected = False
    commandsList = {}
    connections = {}
    accessList = {}

class BOT():
    bs = botState
    async def connectionManager(self, state):
        pass
    async def botFunctions(self, state):
        pass

    await asyncio.gather(connectionManager(bs), botFunctions(bs))





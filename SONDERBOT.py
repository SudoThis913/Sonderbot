import asyncio
import functools
import logging
import sys
import json

from .Apps.AppManager import sba_context, SonderbotApp
from .CONNECTIONS import SBConnections, MessageQueues


class BotState:
    botConnected = False
    commandsList = {}
    connections = []
    accessList = {}


class BOTCLIENT:
    bs = BotState()
    trigger = "!"
    msgQ = MessageQueues()
    appsList = {}
    activeApps = {"hostname": {
        "channel": {
            "application"}}}
    activeCommands = {}

    def __init__(self):
        self.mqLock = asyncio.Lock()
        asyncio.run(self.botHandler())
        pass

    async def botHandler(self, commands=None):
        await self._get_bot_params()
        await asyncio.gather(self.connection_handler(
            self.msgQ), self.bot_commands(),
            self._local_commands(), return_exceptions=True)

    async def connection_handler(self, messageQueue):

        # TODO handle connections
        pass

    async def bot_commands(self):
        # TODO bot level commands, connection level commands, app level commands
        botCommands = {
            'get_bot_params': self._get_bot_params(),
        }

        # TODO command scheduler / dispatch tables
        pass

    async def bot_commands_scheduler(self):
        pass

    async def _get_bot_params(self):
        # TODO get bot paramters from file
        # Will eventually incorporate sqlite logging
        pass

    async def _local_commands(self):
        # TODO take commands from command line
        pass

    async def bot_logging(self):
        pass

    async def bot_print(self):
        async with self.mqLock:
            newmq = self.msgQ.queue.copy()
            for hostnames in newmq.keys():
                if self.msgQ.queue[hostnames]["incomming"]:
                    print(self.msgQ.queue[hostnames]["incomming"].popleft())

    async def sba_apps(self):
        # TODO integrate Sonderbot Apps
        pass

    async def set_trigger(self):
        pass

    async def bot_die(self):
        # DIE!
        pass

if __name__ == '__main__':
    connection1 = {'hostname': "irc.wetfish.net", 'port': 6697,
                   'botnick': "sonderbot", 'botnick2': "Biggus", 'botnick3': "Henry", 'botpass': "sonderbotpw",
                   'messagequeue': MessageQueues()}
    bot = BOTCLIENT()

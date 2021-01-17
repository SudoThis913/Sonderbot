import asyncio
import functools
import logging
import sys
from .Apps.AppManager import sba_context, SonderbotApp
from .CONNECTIONS import SBConnections, MessageQueues
class botState():
    botConnected = False
    commandsList = {}
    connections = []
    accessList = {}


class BOTCLIENT():
    bs = botState()
    msgQ = MessageQueues()
    appsList = {}
    activeApps = {}

    def __init__(self):
        pass

    async def botHandler(self):
        #TODO handle bot functions


        pass
    async def connectionHandler(self, messageQueue):
        #TODO handle connections
        pass
    async def botCommands(self, state):
        #TODO command scheduler / dispatch tables
        pass
    async def getBotParams(self):
        #TODO get bot paramters from file
        pass

    async def localCommands(self):
        #TODO take commands from command line
        pass
    async def botLogging(self):
        pass
    async def sbaApps(self):
        #TODO integrate Sonderbot Apps
        pass


if __name__ == '__main__':
    bot = BOTCLIENT()
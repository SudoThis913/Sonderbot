import asyncio
import ssl
from collections import deque
from IRCCON_OLD_ASYC import IRCCON as IRC
from Queues import MessageQueues
'''
*Asynchronous connections over SSL. Supports IRC client operations.
*Shares a messageQueues class to transport data between IRC and bot client.
Instantiate w/ IRC credentials before running .connect()

Currently uses hard-coded values for development.
'''


# Used to send data between IRCCON and Sonderbot


class Connection:
    def __init__(self, contype, **kwargs):
        irc_req = ['contype','ssl', 'hostname', 'port', 'botnick',
               'botnick1', 'botnick2', 'botnick3', 'botpass']
        discord_req = []
        asyncio.create_task(IRC(kwargs))


class SBConnections:
    connections = [{"type": "IRC"}]
    connected = False
    CH_commands = {
    }

    def __init__(self, connectionsList):
        pass

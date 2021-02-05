import asyncio
import ssl
from collections import deque

'''
*Asynchronous connections over SSL. Supports IRC client operations.
*Shares a messageQueues class to transport data between IRC and bot client.
Instantiate w/ IRC credentials before running .connect()

Currently uses hard-coded values for development.
'''


# Used to send data between IRCCON and Sonderbot
# Probably switch to Pandas DF in future update.

class MessageQueues:
    queue = {
        "hostname": {
            'incomming': deque(),
            'outgoing': deque(),
            'commands': deque({'default_command': 'default params'})
        }
    }

    @property
    def __str__(self):
        output = ''
        for msg in self.queue:
            output = output + "\n" + msg
        return output


class Connection:
    def __init__(self, hostname=None, port=None,
                 botnick="SonderBot", botnick2="Biggus",
                 botnick3="Maximus", botpass="SonderbotPW",
                 messagequeue=MessageQueues):
        self.hostname = hostname
        self.port = port
        self.botnick = botnick
        self.botnick2 = botnick2
        self.botnick3 = botnick3
        self.botpass = botpass
        self.messagequeue = messagequeue


class SBConnections:
    connections = [{"type": "IRC"}]
    connected = False
    CH_commands = {
    }

    def __init__(self, connectionsList):
        pass

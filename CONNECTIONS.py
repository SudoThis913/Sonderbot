import asyncio
import ssl
from collections import deque

'''
Asynchronous connections over SSL. Supports IRC client operations.
Shares a messageQueues class to transport data between IRC and bot client.
Instantiate w/ IRC credentials before running .connect()

'''

#Used to send data between IRCCON and Sonderbot
#Probably switch to Pandas DF in future update.

class MessageQueues:
    queue = {
        "hostname": {
            'incomming': deque(),
            'outgoing': deque(),
            'commands': deque({'default_command': 'default params'})
        }
    }
    def __str__(self):
        for msg in self.queue:
            print(msg)

class SBConnections:
   connections = {'default': deque()}
   connected = False
   CH_commands = {
   }
   def __init__(self):
       pass



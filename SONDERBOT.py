import asyncio
import functools
import logging
import sys
from Apps.AppManager import sba_context, SonderbotApp
from CONNECTIONS import All_Connections
from Queues import MessageQueues
from sql.SQLL_CON import DBconn as DB
import queue

"""
(C) Gregory Norris 2020
      ___        ___       ___        ______      ___        ___         ___        ___       ___      
     /  /\      /  /\     /__/\      /  /:::\    /  /\      /  /\       /  /\      /  /\     /  /\     
    /  /:/_    /  /::\    \  \:\    /  /:/\::\  /  /:/_    /  /::\     /  /::\    /  /::\   /  /:/       
###/  /:/ /\##/  /:/\:\####\  \:\##/  /:/  \::\/  /:/ /\##/  /:/\:\###/  /:/\:\##/  /:/\:\#/  /:/###### 
##/  /:/ /::\/  /:/  \:\____\__\:\/__/:/#\__\:/  /:/ /:/_/  /:/ /:/##/  /:/ /::\/  /:/  \:/  /::\###### 
#/__/:/ /:/\/__/:/#\__/__/::::::::\  \:\#/   /__/:/ /:/ /__/:/ /:/__/__/:/ /:/\/__/:/#\__/__/:/\:\#####   
#\  \:\/:/~/\  \:\#/  \  \: ~~-~~ :\  \:\   /\  \:\/:/ /\  \:\/:::::\  \:\/:/ /\  \:\#/  \__\/  \:\#### 
##\  \::/ /:/\  \:\  //\  \:\##\__\/\  \:\ /::\  \::/ /:/\  \::/~~~~~\  \::/ /:/\  \:\  /:/###\  \:\### 
###\__\/ /:/##\  \:\/:/#\  \:\#######\  \ /::/#\  \:\/:/##\  \:\######\  \:\/:/##\  \:\/:/#####\  \:\##
#####/__/:/####\  \::/###\  \:\#######\  \::/###\  \::/####\  \:\######\  \::/####\  \::/#######\  \:\#
#####\__\/######\__\/#####\__\/########\__\/#####\__\/######\__\/#######\__\/######\__\/#########\__\/#
#######################################################################################################

$$$$$     SONDERBOT IRC CLIENT     $$$$$
Supports multiple asynchronous IRC connections.

"""


class BOTCLIENT:
    Bot_Context = {
        'Access_List': {
            '0': {
                "Sonder": {
                    'hostid': 1,
                    'note': "owner",
                    'access': 0,
                }}},
        'Connections': {
            'hostID': {
                    'connection_parameters': {
                        'HOSTID':   None,
                        'CONTYPE':  None,
                        'HOSTNAME': None,
                        'PORT':     None,
                        'BOTNICK':  None,
                        'BOTNICK2': None,
                        'BOTNICK3': None,
                        'BOTPASS':  None
                    },
                    'CONNECTION':   None,
                    'hostname':     None,
                    'channels': {
                        "users":            None,
                        "active_commands":  None
                    },
                    'incomming': None,
                    'outgoing':  None,
                }},
        'Commands': None,
        'Sonderbot_Apps': None,
        'Database': {'path': None},
    }

    """
            {hostID:{username:access}}
    """
    botConnected = False
    commandsList = {}
    """"
        {hostID{channel:{command:program}}}()
    """
    connections_list = []
    """
        {hostID{}}
    """
    connections = None
    trigger = "!"
    msgQ = MessageQueues()
    appsList = {}
    activeApps = {"hostname": {
        "channel": {
            "application": []
        }}}
    activeCommands = {}

    def __init__(self):
        # Sonderbot Context
        self.bot = self.initialize_context()
        # Initialze database connection
        # Get connection parameters
        self.db = DB()
        # TODO Dynamic Import Programs
        self.connections_list = self.db.get_connections()
        self.connections = All_Connections()
        # TODO Initiate Connections
        self.botMaker(self.connections_list, self.connections_list)

    def initialize_context(self):
        # Initialize new bot context.
        new_context = self.Bot_Context.copy()
        # Erase reference formatting from context file
        erase_ctx_formatting = {"Access_List": {}, "Connections": {}, "Commands": {}, "Sonderbot_Apps": {}}
        new_context.update(erase_ctx_formatting)

        #TODO Database
        db = DB()
        # Initialize SQLite3 database handler class
        # Save as object in context
        new_context["Database"] = db
        # TODO Connections
        new_connections = db.get_connections()
        # Query connections information from db
        for c in new_connections:
            new_context['Connections'][c['hostID']]['connection_parameters'] = c.copy()
        # TODO Dynamic App Loading
        # TODO Commands


        # TODO Message_Queue
        self.Bot_Context["Message_Queue"] = MessageQueues()
        # TODO Access_List
        return

    def botMaker(self, in_connections, in_connections_list):
        Sonderbot = asyncio.run(self.botHandler(in_connections, in_connections_list))

    async def botHandler(self, in_connections, in_connections_list):
        await self._get_bot_params()
        await asyncio.gather(self.connection_handler(self.msgQ, in_connections), self.bot_commands(),
                             self._local_commands(), return_exceptions=True)

    async def connection_handler(self, messageQueue, connections_list):
        loop = asyncio.get_running_loop()
        for connection_parameters in connections_list:
            await self.connections.add_connection(messageQueue, loop, **connection_parameters)

        # TODO handle connections
        pass

    async def bot_commands(self):
        # TODO bot level commands, connection level commands, app level commands
        """ Compiles all commmands into a dispatch table"""
        botCommands = {
            'get_bot_params': self._get_bot_params(),
        }

        # TODO command scheduler / dispatch tables
        pass

    async def bot_commands_scheduler(self):
        pass

    async def _get_bot_params(self):
        # TODO get bot paramters from file
        return self.db.get_connections()
        pass

    async def _local_commands(self):
        # TODO take commands from command line
        pass

    async def bot_logging(self):
        pass

    async def bot_print(self):
        # Test print function, consumes queue, will turn into non-consuming function.
        newmq = self.msgQ.queue.copy()
        for hostnames in newmq.keys():
            if self.msgQ.queue[hostnames]["incomming"]:
                print(self.msgQ.queue[hostnames]["incomming"].popleft())

    async def sba_apps(self):
        # TODO integrate Sonderbot Apps
        pass

    async def set_trigger(self, user=None, trigger="!"):
        if user in self.accessList:
            if self.accessList[user] > 5:
                self.trigger = trigger

    async def bot_die(self):
        # If user has >4 ACL or is channel mod:
        # Close connections
        # Log commands
        # Write pending queue to DB.
        # Close apps
        # Close Sonderbot
        pass


if __name__ == '__main__':
    connection1 = {'hostname': "irc.wetfish.net", 'port': 6697,
                   'botnick': "sonderbot", 'botnick2': "Biggus", 'botnick3': "Henry", 'botpass': "sonderbotpw",
                   'messagequeue': MessageQueues()}
    bot = BOTCLIENT()

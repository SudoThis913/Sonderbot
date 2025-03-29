import asyncio
from .IRCCON import IRC_Connection as IRC

'''
*Asynchronous connections over SSL. Supports IRC client operations.
*Shares a messageQueues class to transport data between IRC and bot client.
Instantiate w/ IRC credentials before running .connect()

Currently uses hard-coded values for development.


Asynchronous IRC connection class.
Queue: { hostname:
            hostnameID: int
            incomming: deque([Message,Message,Message])
            outgoing:  deque([Message,Message,Message])
            commands:  deque()
}
Message: {
    channel:
    message:
    user:
}

'''


# Used to send data between IRCCON and Sonderbot
class All_Connections:
    def __init__(self):
        self.active_connections_list = []
        self.active_connections = {}

    async def add_connection(self,msg, in_loop=asyncio.get_running_loop(),**con_params,):
        try:
            if con_params["hostID"] not in self.active_connections_list:
                self.active_connections_list.append(con_params["hostID"])
                newIRC = IRC(**con_params)
                newCon = await in_loop.create_task(newIRC.connect(msg, **con_params))
                self.active_connections[con_params["hostID"]] = newCon
            else:
                raise ConnectionAbortedError
        except Exception as e:
            print(e)
        return False




class IRCConnection:
    def __init__(self, contype, **kwargs):
        asyncio.create_task(IRC(**kwargs))


class SBConnections:
    connections = [{"type": "IRC"}]
    connected = False
    CH_commands = {
    }

    def __init__(self, connectionsList):
        pass

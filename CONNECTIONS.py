import asyncio
import ssl
from collections import deque

'''
Asynchronous IRC connection.
Sends and receives in 'Channel User Message' format.
Initiates connection upon creation.
Shares a messageQueues class to transport data between IRC and bot client.

'''


class messageQueues:
    queue = {"hostname": {
        'incomming': deque(),
        'outgoing': deque()}
    }


class IRCCON:
    def __init__(self, hostname, port,
                 botnick, botnick2, botnick3, botpass,
                 async_loop, messageQueue=messageQueues):
        self.msgQ = messageQueue
        self.connected = False
        self.async_loop = async_loop
        self.channels = ['#botspam']
        self.hostname = hostname
        self.port = port
        self.botnick = botnick
        self.botnick2 = botnick2
        self.botnick3 = botnick3
        self.botpass = botpass
        self.reader = None
        self.writer = None
        self.readQueue = None
        self.writeQueue = None
        self.connected = await self.connect()

    def initialize_queue(self, messageQueue):
        if self.hostname not in self.msgQ.queue:
            self.msgQ.queue[self.hostname] = {'incomming': deque(),
                                              'outgoing': deque()}

    async def handler(self, state=None, async_loop=None):
        for out_msg in self.msgQ.queue[self.hostname]['outgoing']:
            await self.send(**self.msgQ.queue[self.hostname]['outgoing'].popleft())
        self.msgQ.queue[self.hostname]['incomming'].append(await self.receive())

    async def connect(self):
        ### TEST SEGMENT - SHOULD BE HANDLED THROUGH MSG DEQUEUE
        print(f"connecting to {self.hostname} {self.port}")
        sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='selfsigned.cert')
        reader, writer = await asyncio.open_connection(self.hostname, self.port)
        self.reader = reader
        self.writer = writer
        print(f"connected to {self.hostname}")
        self.authenticate_user()
        return True

    def authenticate_user(self):
        await self.send(message=f"PASS {self.botpass} \n", channel=None, user=None)
        await asyncio.sleep(1)
        await self.send(message=f"USER {self.botnick} \n", channel=None, user=None)
        await asyncio.sleep(1)
        await self.send(message=f"USER {self.botnick} \n", channel=None, user=None)

    def test(self):
        pass

    async def disconnect(self):
        self.reader.close()
        self.writer.close()
        await self.writer.wait.closed()
        await self.reader.wait.closed()
        self.connected = False

    async def send(self, message=None, channel=None, user=None):
        if channel and user and message:
            message = (bytes(f"PRIVMSG {channel} :/msg {user} {message}\n", "UTF-8"))
        elif channel and message:
            message = (bytes(f"PRIVMSG {channel} {message}\n", "UTF-8"))
        elif message:
            message = (bytes(f"{message}\n", "UTF-8"))

        if message:
            self.writer.write(message)
            await self.writer.drain()

    async def receive(self):
        data = await self.reader.read(4096)
        data = data.decode()
        if data.find('PING') != -1:
            print("PONG")
        print(f"received {data}")

    def joinChannel(self, channel):
        print(f"joining {channel}")

    def whisper(self, channel, user, message):
        print(f"PRIVMSG {user}: {message}")
        return (f"PRIVMSG #{channel} :/msg {user} {message}\r\n")

    def joinchannel(self, channel):
        pass
# botconfig.connections{hostname:{channel{funcitons, input, output, users}}}

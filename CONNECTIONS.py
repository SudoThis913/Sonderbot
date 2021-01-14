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
    def __str__(self):
        for msg in self.queue:
            print(msg)


class IRCCON:
    def __init__(self, hostname = None, port = None,
                 botnick = None, botnick2 = None, botnick3=None, botpass=None,
                 async_loop=asyncio.new_event_loop(), messagequeue=messageQueues):
        self.msgQ = messagequeue
        self.connected = False
        self.async_loop = async_loop
        self.reader = None
        self.writer = None

        self.channels = ['#botspam']
        self.hostname = hostname
        self.port = port
        self.botnick = botnick
        self.botnick2 = botnick2
        self.botnick3 = botnick3
        self.botpass = botpass
        self.initialize_queue()

    def initialize_queue(self):
        if self.hostname not in self.msgQ.queue:
            self.msgQ.queue[self.hostname] = {'incomming': deque(),
                                              'outgoing': deque()}

    async def handler(self, state=None, async_loop=None):
        #SEND MESSAGES IN OUTGOING QUEUE TO IRC HOST
        for out_msg in self.msgQ.queue[self.hostname]['outgoing']:
            await self.send(**self.msgQ.queue[self.hostname]['outgoing'].popleft())
        #RECEIVE MESSAGES FROM IRC HOST
        new_msg = await self.receive()
        self.msgQ.queue[self.hostname]['incomming'].append(new_msg)

    async def connect(self):
        ### TEST SEGMENT - SHOULD BE HANDLED THROUGH MSG DEQUEUE
        print(f"connecting to {self.hostname} {self.port}")
        sslctx = ssl.create_default_context()
        #sslctx.check_hostname = False
        #sslctx.load_verify_locations('sba.crt')


        reader, writer = await asyncio.open_connection(self.hostname, self.port, ssl=sslctx)
        self.reader = reader
        self.writer = writer
        print(f"connected to {self.hostname}")
        await self.authenticate_user()
        return True

    async def authenticate_user(self):
        #print(f"PASS {self.botpass}")
        await self.send(message=f"PASS {self.botpass} \n", channel=None, user=None)
        await asyncio.sleep(1)
        await self.receive()

        print(f"USER {self.botnick}")
        await self.send(message=f"USER {self.botnick} {self.botnick2} {self.botnick3} :Sonderbot\n", channel=None, user=None)
        await asyncio.sleep(1)
        await self.receive()
        print(f"NICK {self.botnick}")
        await self.send(message=f"NICK {self.botnick} \n", channel=None, user=None)

    async def disconnect(self):
        self.reader.close()
        self.writer.close()
        await self.writer.wait.closed()
        await self.reader.wait.closed()
        self.connected = False

    async def send(self, message=None, channel=None, user=None):
        if not channel and not user and not message:
            pass
        if channel and user and message:
            message = f"PRIVMSG {channel[1:]} :/msg {user[1:]} {message}\n"
            print(f"CHANNEL {message}")
        elif channel and message:
            message =f"PRIVMSG {channel[1:]} {message}\n"
        elif message:
            print(f"SERV {message}")
            message = f"{message}\n"

        if message:
            self.writer.write(message.encode())
            await self.writer.drain()
            print(f"drain {message}")

    async def receive(self):
        data = await self.reader.read(4096)
        if data:
            data = data.decode()
            print(f"received {data}")
            if data.find('PING') != -1:
                print("PONG")
                print(f"received {data.decode('utf-8')}")
                response = bytes('PONG ' + data.split()[1].encode('UTF-8').decode('UTF-8')+'\r\n', 'UTF-8')
                await self.send(message=response)

    def joinChannel(self, channel):
        print(f"joining {channel}")


    def whisper(self, channel, user, message):
        print(f"PRIVMSG {user}: {message}")
        return (f"PRIVMSG #{channel} :/msg {user} {message}\r\n")

    def joinchannel(self, channel):
        pass

class testBot:
    def __init__(self, queue = messageQueues):
        self.q = queue

    async def print(self, mq, hostname):
        for msg in mq.queue[hostname]["incomming"]:
            (mq.queue[hostname]["incomming"].popleft())

if __name__ == '__main__':

    # RUNS TEST BOT ON CONNECTION, SHOULD CONNECT AND PRINT ANYTHING ON THE CHANNEL
    async_queue = messageQueues
    irc = IRCCON(hostname = "irc.wetfish.net", port =6697,
                 botnick = "sonderbot", botnick2 = "Biggus", botnick3="Henry", botpass="sonderbotpw",
                 async_loop=asyncio.new_event_loop(), messagequeue=messageQueues)
    isrunning = asyncio.run(irc.connect())
    #asyncio.run(irc.authenticate_user())
    if isrunning:
        bot = testBot()
        test = asyncio.gather(bot.print(async_queue,"wetfish.irc.net"), irc.handler(async_queue))

    pass
import asyncio
import ssl
from collections import deque

'''
Asynchronous IRC connection over SSL.
Shares a messageQueues class to transport data between IRC and bot client.
Instantiate w/ IRC credentials before running .connect()

'''

#Used to send data between IRCCON and Sonderbot
#Probably switch to Pandas DF in future update.
class messageQueues:
    queue = {"hostname": {
        'incomming': deque(),
        'outgoing': deque()}
    }

    def __str__(self):
        for msg in self.queue:
            print(msg)

#Asynchronous IRC connection.
class IRCCON:
    def __init__(self, hostname = None, port = None,
                 botnick = None, botnick2 = None, botnick3=None, botpass=None,
                 async_loop=asyncio.new_event_loop(), messagequeue=messageQueues):
        self.msgQ = messagequeue
        self.connected = False
        self.authenticated = False
        self.async_loop = async_loop
        #TODO Update as function params instead of class variable 2 limit scope
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

    async def connect(self):
        sslctx = ssl.create_default_context()
        print(f"connecting to {self.hostname} {self.port}")
        #create ssl default context.
        reader, writer = await asyncio.open_connection(self.hostname, self.port, ssl=sslctx)
        self.reader = reader
        self.writer = writer
        print(f"connected to {self.hostname}")
        self.connected = True

        #Authenticate user, start handling IO calls
        await self.authenticate_user()
        # Loop IO calls and message queue handling
        await asyncio.sleep(.5)
        await self.joinChannel("#botspam")
        while self.connected:
            await self.handler()

    async def handler(self, message=None, channel=None, user=None):
        qlock = asyncio.Lock()
        mq = None
        async with qlock:
            if message:
                self.msgQ.queue[self.hostname]['outgoing'].append({'message':message,'channel':channel,'user':user})

            #Copy message cue for conditional statements
            mq = self.msgQ.queue[self.hostname].copy()
            self.msgQ.queue[self.hostname]['outgoing'].clear()


            #SEND MESSAGES IN OUTGOING QUEUE TO IRC HOST
            try:
                if mq['outgoing']:
                    for out_msg in mq['outgoing']:
                        msgSend = mq['outgoing'].popleft()
                        await self.send(**msgSend)
                #RECEIVE MESSAGES FROM IRC HOST
                new_msg = await self.receive()
                if new_msg:
                    self.msgQ.queue[self.hostname]['incomming'].append(new_msg)
            except Exception as e:
                print(e)

    async def authenticate_user(self):
        #Send password (optional)
        if self.botpass is not None:
            await asyncio.sleep(1)
            await self.handler(message=f"PASS {self.botpass} \n")

        #Send usernames
        await asyncio.sleep(1)
        await self.send(message=f"USER {self.botnick} {self.botnick2} {self.botnick3} :Sonderbot\n", channel=None, user=None)

        #Set nickname
        await asyncio.sleep(1)
        print(f"NICK {self.botnick}")
        await self.send(message=f"NICK {self.botnick} \n", channel=None, user=None)
        self.authenticated = True

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
            print(f"send: MCU {message}")
        elif channel and message:
            message =f"PRIVMSG {channel[1:]} {message}\n"
            print(f"send: CM {message}")
        elif message:
            message = f"{message}\n"
            print(f"send: M {message}")
        if message is not None:
            self.writer.write(message.encode())
            await self.writer.drain()
            print(f"sending: {message}")

    async def receive(self):
        data = await self.reader.read(4096)
        if data:
            data = data.decode()
            print(f"received {data}")
            if data.find('PING') != -1:
                print("PONG")
                print(f"received {data}")
                response = ('PONG '+data.split()[1])
                await self.send(message=response)

    async def joinChannel(self, channel):
        print(f"joining {channel}")
        await self.handler(message=f"JOIN {channel}\n")

    def whisper(self, channel, user, message):
        print(f"PRIVMSG {user}: {message}")
        return (f"PRIVMSG #{channel} :/msg {user} {message}\r\n")

    def commandsList(self):
        pass

class testBot:
    def __init__(self, queue=messageQueues):
        self.mq = queue
        self.qLock = asyncio.Lock()

    async def bot_print(self):
        async with self.qLock:
            newmq = self.mq.queue.copy()
            for hostnames in newmq.keys():
                if self.mq.queue[hostnames]["incomming"]:
                    print(self.mq.queue[hostnames]["incomming"].popleft())
                else:
                    pass

async def main():
    # RUNS TEST BOT ON CONNECTION, SHOULD CONNECT AND PRINT ANYTHING ON THE CHANNEL
    async_queue = messageQueues
    irc = IRCCON(hostname="irc.wetfish.net", port=6697,
                 botnick="sonderbot", botnick2="Biggus", botnick3="Henry", botpass="sonderbotpw",
                 async_loop=asyncio.get_event_loop(), messagequeue=messageQueues)
    bot = testBot(messageQueues)
    await asyncio.gather(bot.bot_print(), irc.connect())

if __name__ == '__main__':
    #Run the test bot, connect to IRC.
    asyncio.run(main())
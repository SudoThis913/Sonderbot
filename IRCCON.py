#!/usr/bin/python3
import asyncio
import ssl
import logging
from Queues import MessageQueues
import traceback

'''
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


class IRC_Connection:
    connected = False
    active = False
    timeout = 10
    RECONNECT_MAX_TIME = 60

    def __init__(self, **bot_params):
        self.connected = False
        self.active = False
        self.authenticated = False
        self.hostname = bot_params['hostname']
        self.timeout = 10
        self.reconnect_attempts = 1
        self.channels = {}

    async def connect(self, msq=MessageQueues, **params):
        wait = min(self.reconnect_attempts * 2, self.RECONNECT_MAX_TIME)  # max wait time on reconnect attempts
        connect_attempts = 0
        if self.reconnect_attempts < 120:
            print("Connection Attempt: " + str(self.reconnect_attempts))
            try:
                ssl_ctx = ssl.create_default_context()
                reader, writer = await asyncio.open_connection(params['hostname'], params['port'], ssl=ssl_ctx)
                self.connected = True
                # Create authenticate task, then continue to run handler.
                au = asyncio.create_task(self.authenticate_user(msq, reader, writer, **params))
                sq = asyncio.create_task(self.send_queue(msq, writer))
                rq = asyncio.create_task(self.receive_queue(msq,reader,writer))
                await asyncio.gather(au, sq, rq)
            except TimeoutError:
                print("Timeout Error")
                self.reconnect_attempts = self.reconnect_attempts + 1
                await self.reset_reconnect_attempts(self.reconnect_attempts)
                self.connected = False
            except Exception as e:
                print("Exception")
                traceback.print_exc()
                print(e)
                self.reconnect_attempts = self.reconnect_attempts + 1  # increment reconnect attempts
                await self.reset_reconnect_attempts(self.reconnect_attempts)
                self.connected = False
        else:
            print(f"Max Retries {params['hostname']}")
            return False

    async def reset_reconnect_attempts(self, recon_num):
        print("reset")
        await asyncio.sleep(500)
        if self.reconnect_attempts < recon_num + 1:
            self.reconnect_attempts = 0

    def create_ssl_ctx(self, **params):
        print("ctx")
        ssl_ctx = ssl.create_default_context()
        if not params['ssl']:
            # TODO handle non-ssl connection
            ssl_ctx = ssl.create_default_context()
        return ssl_ctx


    async def send_queue(self, msq, writer):
        while self.connected:
            #print("S_Q")
            if msq.queue[self.hostname]['outgoing']:
                outgoing = msq.queue[self.hostname]['outgoing'].popleft()
                await self.send(writer, self.irc_msg_format(**outgoing))
            await asyncio.sleep(.2)
        return False

    async def send(self, writer, message=None):
        print("SENDING " + message)
        writer.write(message.encode())
        # print("send_2")
        await writer.drain()
        # print("send_3")
        # TODO return sent confirmation for sql logging
        return True

    async def receive_queue(self, msq, reader, writer):
        while self.connected:
            incomming = await self.receive(reader, writer)
            if incomming != -1:
                #print("r_q_inc " + incomming)
                msq.queue[self.hostname]['incomming'].append(incomming)
                if incomming.startswith('ERROR :Closing link:'):
                    raise TimeoutError
                # print("r_q4")
            await asyncio.sleep(.2)
        return False

    async def receive(self, reader, writer):
        response = await reader.read(4096)
        if response != -1:
            response = response.decode()
            # print("rec3" + response)
            if response.startswith('PING'):
                print("ping: " + response)
                await self.send(writer, message=(str(response).replace('PING','PONG')))
                print(str(response).replace('PING','PONG'))
            print("rec4 ")
            return response
        else:
            print("rec4 ")
            return None

    def irc_msg_format(self, **msg):
        message, user, channel = msg['message'], msg['user'], msg['channel']
        if (message and user and channel): return f"PRIVMSG {channel[1:]} :/msg {user[1:]} {message}\n"
        if (message and user): return f"PRIVMSG :/msg {user[1:]} {message}\n"
        if (message and channel): return f"PRIVMSG {channel[1:]} {message}\n"
        if (message): return f"{message}\n"
        return None

    async def authenticate_user(self, msq, reader, writer, **params):
        # Send password (optional)
        # print("au_1")
        if params['botpass']:
            # print("au_bp")
            await asyncio.sleep(1)
            await self.send(writer, f"PASS {params['botpass']}\n")
            await asyncio.sleep(.5)
        # Send usernames and set nickname
        await asyncio.sleep(.5)
        await self.send(writer, f"USER {params['botnick']} {params['botnick2']} {params['botnick3']} :Sonderbot\n")
        await asyncio.sleep(.5)
        await self.send(writer, f"NICK {params['botnick']}\n")
        await asyncio.sleep(5)
        await self.join_channel(msq, channel='#botspam')

    async def disconnect(self, reader, writer):
        if reader.hasattribute('close'):
            reader.close()
            writer.close()
            await reader.wait.closed()
            await writer.wait.closed()
        self.connected = False

    async def join_channel(self, msq, channel=None, key=''):
        self.channels[channel] = True
        #Copy message template before submitting
        join_msg = MessageQueues.message.copy()
        join_msg['message'] = f"JOIN {channel} {key}\n"
        msq.queue[self.hostname]['outgoing'].append(join_msg)

    async def leave_channel(self, msq, channel=None):
        self.channels[channel] = False
        part_msg = MessageQueues.message.copy()
        part_msg['message'] = f"PART {channel}\n"
        msq.queue[self.hostname]['outgoing'].append(part_msg)


class TestBot:
    # TEST THE IRC CONNECTION W/ SIMPLE BOT. SHOULD PRINT ANYTHING SENT TO IT.
    async def bot_print(self, queue=MessageQueues):
        try:
            while True:
                mq = queue
                for hostname in mq.queue.keys():
                    if mq.queue[hostname]['incomming']:
                        print(mq.queue[hostname]['incomming'].popleft())
                await asyncio.sleep(1)
        except Exception as e:
            print("BOT EXCEPTION")
            traceback.print_exc()


async def main():
    # RUNS TEST BOT ON CONNECTION, SHOULD CONNECT AND PRINT ANYTHING ON THE CHANNEL
    message_queue = MessageQueues
    message_queue.queue['irc.wetfish.net'] = MessageQueues.queue['hostname'].copy()
    irc_parameters = {'hostname': "irc.wetfish.net", 'port': 6697, 'botnick': "sonderbot",
                      'botnick2': "Biggus", 'botnick3': "Henry", 'botpass': 'sonderbotpw'}
    irc = IRC_Connection(**irc_parameters)
    bot = TestBot()
    print("make bot")
    sonderbot = asyncio.create_task(bot.bot_print(message_queue))
    irccon = asyncio.create_task(irc.connect(message_queue, **irc_parameters))
    await asyncio.gather(sonderbot,irccon)

if __name__ == '__main__':
    # Run the test bot, connect to IRC.
    asyncio.run(main())

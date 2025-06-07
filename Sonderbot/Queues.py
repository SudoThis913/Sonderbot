from collections import deque
import queue


class MessageQueues:
    queue = {
        "hostname": None,
        'incomming': deque(),
        'outgoing': deque(),
        'commands': {}

    }
    message = {'hostID': None,
               'hostname': None,
               'channel': None,
               'message': None,
               'user': None,
               'timestamp': None}

    @property
    def __str__(self):
        output = ''
        for msg in self.queue:
            output = output + "\n" + msg
        return output

    @property
    def __getitem__(self):
        return self.queue


class Message:
    def __init__(self, hostID='', hostname='', channel='', message='', user=''):
        self.hostID = hostID
        self.hostname = hostname
        self.channel = channel
        self.message = message,
        self.user = user

    @property
    def __str__(self):
        return str(self.hostID)


class MessagesQueue:
    iMSQ = queue.Queue()
    oMSQ = queue.Queue()

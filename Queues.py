from collections import deque
class MessageQueues:
    queue = {
        "hostname": {
            'incomming': deque(),
            'outgoing': deque(),
            'commands': deque()
        }
    }
    message = {'channel': None, 'message': None, 'user': None}

    @property
    def __str__(self):
        output = ''
        for msg in self.queue:
            output = output + "\n" + msg
        return output
    @property
    def __getitem__(self):
        return self.queue

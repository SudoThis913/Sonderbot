
import os

class SonderbotApp:
    messages = []
    dispatch = {}
    appname = "SonderbotApp"

    def __init__(self, name=None):
        if name:
            self.name = name
    ##### SONDERBOT APP METHODS #####
    def input(self, **in_msg):
        pass

    def output(self, **message):
        msgout = self.messages.copy()
        self.messages.clear()
        return msgout

    def get_dispatch(self):
        return self.dispatch

    def irc_format(self, in_str, **in_msg):
        new_msg = {"channel": in_msg["channel"],
                   "user": in_msg["user"],
                   "message": in_str}
        return new_msg

def main():
    pass
if __name__ == "__main__":
    main()
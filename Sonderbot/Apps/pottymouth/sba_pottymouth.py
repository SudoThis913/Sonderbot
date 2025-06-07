import random
#Uses SonderBotApp as a base class. The Sonderbot looks for apps/*/*.sba.py for auto-installing addon modules.
from sonderbotapp import SonderbotApp


def __getattr__(name):
    return "Pottymouth"
def main1():
    x = Pottymouth()
    return x
# Pottymouth is a sonderbot app which randomly returns dirty phrases on command.
class Pottymouth(SonderbotApp):
    lastDirty = ""
    mainurl = "https://example.com"

    def __init__(self, name=None):
        SonderbotApp.__init__(self, name)
        self.persistant = True
        self.selfDispatch = False
        self.appName = "pottymouth"
        print("POTTYMOUTH STARTED")
        self.dispatch = {
            "dirty": self.dirty,
            "last dirty url": self.last_dirty_url,
            "dirty info": self.dirty_info,
            "dirty url": self.dirty_url,
        }

    def return_dispatch(self):
        return self.dispatch

    def dirty_help(self, **kwargs):
        dinfo = "dirty commands are: "
        for key in self.dispatch.keys():
            dinfo = dinfo + key + ", "
        dinfo = dinfo[:-2]
        self.queue_response(dinfo, **kwargs)

    def dirty(self, **kwargs):
        dirty_comment = self.pottymouth(**kwargs)
        self.queue_response(dirty_comment["comment"], **kwargs)

    def dirty_info(self, **kwargs):
        dinfo = "From the album: " +self.lastDirty["album"] + " at: " + self.mainurl + self.lastDirty["picture"]
        self.queue_response(dinfo, **kwargs)

    def dirty_url(self, **kwargs):
        dirty_comment = self.pottymouth(**kwargs)
        dinfo = self.mainurl + dirty_comment["picture"]
        self.queue_response(dinfo, **kwargs)

    def last_dirty_url(self, **kwargs):
        dinfo = self.mainurl+self.lastDirty["picture"]
        self.queue_response(dinfo, **kwargs)

    def queue_response(self, in_str, **kwargs):
        print("in_str: "+in_str)
        self.messages.append(
            {"channel": kwargs["channel"],
             "user": kwargs["user"],
             "message": str(in_str)}
        )

    def pottymouth(self, **kwargs):
        # Open text file containing dirty phrases scraped from the internet.
        with open("Dirty_Comments.txt", encoding='utf-8') as f:
            lines = f.readlines()
            line = (random.choice(lines))

        # Text file is in dictionary format  {'album':"", 'picture':"", 'url':"", 'comment':""}\n.
        # Eval converts to dict.
        dirty_comment = eval(line)

        # If random comment is 4 or more words long, add dirty_comment to lastDirty and return.
        # Otherwise, add recursion counter to kwargs and self-invoke.
        if len(dirty_comment['comment'].split()) < 4:
            if 'retry' not in kwargs:
                kwargs['retry'] = 1
                dirty_comment = self.pottymouth(**kwargs)
            elif kwargs['retry'] < 11:
                kwargs['retry'] = kwargs['retry'] + 1
                dirty_comment = self.pottymouth(**kwargs)
            elif kwargs['retry'] > 10:
                dirty_comment["comment"] = "ERROR: MICROPENIS DETECTED."
        self.lastDirty = dirty_comment
        return dirty_comment


if __name__ == '__main__':
    pm = Pottymouth()
    kwargsX = {"channel": "C", "user": "U", "message": "M"}

    pm.dirty(**kwargsX)
    pm.last_dirty_url(**kwargsX)
    pm.dirty_info(**kwargsX)
    pm.dirty_url(**kwargsX)
    pm.dirty_help(**kwargsX)
    x = pm.output(**kwargsX)

    for y in x:
        print(y)

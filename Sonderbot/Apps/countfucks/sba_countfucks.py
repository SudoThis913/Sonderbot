import random
#Uses SonderBotApp as a base class. The Sonderbot looks for apps/*/*.sba.py for auto-installing addon modules.
import os
import re
import traceback
from dotenv import load_dotenv
from Apps.sonderbotapp import SonderbotApp

def __getattr__(name):
    return "CountFucks"
def main1():
    x = CountFucks()
    return x
# Pottymouth is a sonderbot app which randomly returns dirty phrases on command.
class CountFucks(SonderbotApp):
    whoGivesAFuck = {}
    fuckingLeaders = []
    hexLog = []
    leaderLog = []
    animeLog = []
    message = {"channel": "", "user": "", "message": ""}
    messages = []


    def __init__(self, name=None):
        SonderbotApp.__init__(self, name)
        self.persistant = False # Does not need to store state specific information.
        self.selfDispatch = True # Will receive every message logged by channel.
        self.appName = "countFucks"
        print("COUNT FUCKS STARTED")
        self.dispatch = {
            "count fucks": "",
            "all fucks": "",
            "my fucks": "",
            "count fuckula": ""
        }

    def dispatchFucks(self, **in_msg):
        trigger = in_msg["trigger"]
        FUCKINGCOMMANDS = \
            {
                "top fucks": self.topFucks,
                "count fucks": self.countFucks,
                "my fucks": self.myFucks,
                "all fucks": self.topFucks,
                "fuck me": self.fuckSelf,
                "count fuckula": self.countFuckula, }
        FUCKINGCOMMANDS = {trigger + key: value for key, value in FUCKINGCOMMANDS.items()}
        # = FC2
        if in_msg["message"] in FUCKINGCOMMANDS.keys():
            FUCKINGCOMMANDS[in_msg["message"]](**in_msg)

    def fuckSelf(self, **message):
        fuckingSelf = open(os.path.join(os.getcwd(), "sba_countfucks.py"), 'r', encoding='utf8')
        fucks = 0
        for line in fuckingSelf:
            line = line.lower()
            fuck = re.findall('fuck', line)
            for f in fuck:
                fucks = fucks + 1
        print("The number of fucks in this file is: " + str(fucks))

    def countFuckula(self, **in_msg):
        # prints 14 lines of count fuckula ASCII art.
        countFuckulaHimself = open(os.path.join(os.getcwd(), "theCount_small"), 'r', encoding='utf8')
        fuckingLines = ""
        # fuck = "CountFuckula"
        for line in countFuckulaHimself:
            fuck = "CountFuckula"
            fuckingLines = fuckingLines + "."
            for letter in line[1:]:
                if letter.isalpha():
                    letter = fuck[0]
                elif letter == "`":
                    letter = '.'
                elif letter == "'":
                    letter = '.'
                fuck = (fuck[1:] + fuck[0])
                fuckingLines = fuckingLines + letter
        self.messages.append(self.irc_format(fuckingLines, **in_msg))

    def topFucks(self, **in_msg):
        self.collectFucks()
        self.fuckingLeaderboard()
        try:
            for line in self.fuckingLeaders[:7]:
                self.messages.append(self.irc_format(line, **in_msg))
        except Exception as e:
            traceback.print_exc()
            pass

    def countFucks(self, **in_msg):
        self.collectFucks()
        allFucks = 0
        for key in self.whoGivesAFuck:
            allFucks = allFucks + self.whoGivesAFuck[key]
        m = "The total number of Fucks given is: " + str(allFucks)
        self.messages.append(self.irc_format(m, **in_msg))

    def myFucks(self, **in_msg):
        self.collectFucks()
        fucker = in_msg["user"]
        whofucks = ""
        if fucker in self.whoGivesAFuck:
            whofucks = "%s has %s fucks to give." % (fucker, str(self.whoGivesAFuck[fucker]))
        else:
            whofucks = "%s has no fucks to give." % (fucker)
        self.messages.append(self.irc_format(whofucks, **in_msg))

    def collectFucks(self):
        try:
            # save filepath in seperate .env with following line:
            # IRC_LOG="FILEPATH"
            load_dotenv()
            LOG = os.getenv("IRC_LOG")
            self.whoGivesAFuck.clear()
            self.fuckingLeaders = []
            self.hexLog = open(LOG, "r", encoding="utf8")
            # Open a log file
            self.leaderLog = open(r"leaderLog.log", "w+", encoding="utf8")
            log = self.hexLog.readlines()
            self.whoGivesAFuck = {}
            for line in log:
                fuckcount = 0
                if len(line) > 17:
                    if line[16] == '*':
                        # print('***')
                        pass
                    else:
                        # print(line)
                        fuck = re.findall('fuck', line)
                        if fuck:
                            for fucks in fuck:
                                fuckcount = fuckcount + 1

                            name = re.search('<.*?>', line)  # names are received as <name>
                            if name:
                                # print(name.group(0)+" Fucks: "+str(fuckcount))
                                name = name.group(0)
                                name = name[1:-1]  # remove < > from name
                                # tally up fucks in a dictionary
                                if name not in self.whoGivesAFuck:
                                    self.whoGivesAFuck[name] = fuckcount
                                else:
                                    self.whoGivesAFuck[name] = fuckcount + self.whoGivesAFuck[name]
        except Exception as e:
            pass

    def fuckingLeaderboard(self):
        championsOfFuck = [(fucks, name) for name, fucks in self.whoGivesAFuck.items()]
        championsOfFuck.sort(reverse=True)
        winner = championsOfFuck[0][1]
        winner = winner[:-1] + "‎" + winner[-1]
        mostfucks = championsOfFuck[0][0]
        forbiddenChars = ['<', '>', ]
        fuckingWinner = "%s gives the most fucks at %s fucks." % (winner, str(mostfucks))
        self.fuckingLeaders.append(fuckingWinner)
        self.fuckingLeaders.append("Fucking Leaderboard:")

        for fucks, name in championsOfFuck:  # Top 5 fuckers
            # ADD INVISIBLE CHARACTERS TO NAMES TO PREVENT PINGING CLIENTS ON IRC
            fuckingContenders = name[:-1] + "‎" + name[-1] + ": " + str(fucks)
            self.fuckingLeaders.append(fuckingContenders)
        # print(name+": "+str(fucks))
        # print(self.leaderboard[:7])

    def returnfucks(self):
        lb = self.fuckingLeaders[:7]  # rETURNS top 5 fuckcount
        self.fuckingLeaders = []
        return lb

    ##### IRC COMPAT #####
    def input(self, **in_msg):
        pass

    def irc_format(self, in_str, **in_msg):
        newMsg = {"channel": in_msg["channel"],
                  "user": in_msg["user"],
                  "message": in_str}
        return newMsg

    def output(self, **message):
        msgout = self.messages.copy()
        self.messages.clear()
        self.fuckingLeaders = []
        return msgout

########### MAIN ######################
if __name__ == '__main__':
    # test cases
    cf = CountFucks()
    m = {"channel": "ch ", "user": "bot ", "message": "msg"}
    cf.myFucks(**m)
    cf.topFucks(**m)
    cf.countFucks(**m)
    cf.fuckSelf(**m)
    cf.countFuckula(**m)
    z = cf.to_channel(**m)
    print("LB" + cf.fuckingLeaders)
    for row in z:
        print(str(row["channel"]) + str(row["user"]) + str(row["message"]))



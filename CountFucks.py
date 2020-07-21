import os
import re


class CountFucks:
    whoGivesAFuck = {"Sonder": 0, "Rachel":69}
    leaderboard = []
    hexLog = []
    leaderLog = []
    animeLog = []
    def __init__(self):
        try:
            self.whoGivesAFuck = {}
            self.leaderboard = []
            self.hexLog = open(r"C:\Users\GNorr\AppData\Roaming\HexChat\logs\Wetfish\#wetfish.log", "r", encoding="utf8")
            #Open a log file
            self.leaderLog = open(r"leaderLog.log", "w+", encoding="utf8")
            #self.animeLog = open(r"#anime.log", "r+", encoding="utf8")
            log = self.hexLog.readlines()
            self.whoGivesAFuck = {}
            for line in log:
                fuckcount = 0
                if len(line) > 17:
                    if line[16] == '*':
                        #print('***')
                        pass
                    else:
                        #print(line)
                        fuck = re.findall('fuck', line)
                        if fuck:
                            for fucks in fuck:
                                fuckcount = fuckcount+1

                            name = re.search('<.*?>', line) #names are received as <name>
                            if name:
                                #print(name.group(0)+" Fucks: "+str(fuckcount))
                                name = name.group(0)
                                name = name[1:-1] # remove < > from name
                                #tally up fucks in a dictionary
                                if name not in self.whoGivesAFuck:
                                    self.whoGivesAFuck[name] = fuckcount
                                else:
                                    self.whoGivesAFuck[name] = fuckcount + self.whoGivesAFuck[name]

            #topFucks = sorted(self.leaderboard, key = self.leaderboard.get())

            championsOfFuck = [(fucks, name) for name,fucks in self.whoGivesAFuck.items()]
            championsOfFuck.sort(reverse=True)
            winner = championsOfFuck[0][1]
            winner = winner[:-1]+"‎"+winner[-1]
            mostfucks = championsOfFuck[0][0]
            forbiddenChars = ['<', '>', ]
            fuckingWinner = "%s gives the most fucks at %s fucks." % (winner, str(mostfucks))
            self.leaderboard.append(fuckingWinner)
            print(fuckingWinner)
            self.leaderboard.append("Fucking Leaderboard:")
            print("Fuck Leaderboard:")
            print_leaderboard = ""
            for fucks, name in championsOfFuck: # Top 5 fuckers
                fuckingContenders = name[:-1]+"‎"+name[-1]+": "+str(fucks)
                print_leaderboard = print_leaderboard+fuckingContenders+"\n"
                self.leaderboard.append(fuckingContenders)
            #print(name+": "+str(fucks))
            print(print_leaderboard)
        except Exception as e:
            print(e)
    def returnfucks(self):
        lb = self.leaderboard[:7]#rETURNS top 5 fuckcount
        self.leaderboard = ""
        return lb

    def countFucks(self, name):
        pass


    ##### IRC COMPAT #####
    def input(self, channel, user, message):
        pass
    def to_user(self):
        return False

    def to_channel(self):
        return self.returnfucks()

########### MAIN ######################
if __name__ == '__main__':
    cf = CountFucks()

    # for fucks,name in championsOfFuck:
    # print("%s: %d" % (name,fucks))
    #
    # for name, fucks in self.leaderboard.items():
    #   #print(name+": "+str(fucks))
    #  pass
    # for name, fucks in sortedFucks:
    #    print(name + ": " + str(fucks))
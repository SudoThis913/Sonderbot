#Give a Fuck (C) Greg Norris 2020
#import os
import re
class Fuck:
    timeOfFuckery = ""
    fucker = ""
    fucked = ""
    fucking = ""
    fuckConversionRate =""# The fuck conversion rate of one Fuck is equal to the US Dollar conversion of (XRP/BTC)/virgins

class CountFucks:
    whoGivesAFuck = {}
    leaderboard = []
    hexLog = []
    leaderLog = []
    def __init__(self):
        try:
            self.hexLog = open(r"*.log", "r", encoding="utf8")
            self.leaderLog = open(r"leaderLog.log", "r+", encoding="utf8")

            log = self.hexLog.readlines()

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

                            fucker = re.search('<.*?>', line) #names are stored as <fucker>
                            if fucker:
                                #print(fucker.group(0)+" Fucks: "+str(fuckcount))
                                fucker = fucker.group(0)
                                fucker = fucker[1:-1]
                                #tally up fucks in a dictionary
                                if fucker not in self.whoGivesAFuck:
                                    self.whoGivesAFuck[fucker] = fuckcount
                                else:
                                    self.whoGivesAFuck[fucker] = fuckcount + self.whoGivesAFuck[fucker]

            #topFucks = sorted(self.leaderboard, key = self.leaderboard.get())

            championsOfFuck = [(fucks, name) for name,fucks in self.whoGivesAFuck.items()]
            championsOfFuck.sort(reverse=True)
            winner = championsOfFuck[0][1]
            mostfucks = championsOfFuck[0][0]
            out_most = "%s gives the most fucks at %s fucks." % (winner, str(mostfucks))
            print(out_most)
            print("Fuck Leaderboard:")
            print_leaderboard = ""
            for fucks, fucker in championsOfFuck[1:]: # Top 5 fuckers
                print_leaderboard = print_leaderboard+fucker+": "+str(fucks)+"\n"
            #print(fucker+": "+str(fucks))
            print(print_leaderboard)
            self.leaderboard = print_leaderboard
            self.leaderLog.write(print_leaderboard)#tally number of fucks given. within leaderlog.

        except Exception as e:
            print(e)

    def returnfucks(self):
        return self.leaderboard

    def countFucks(self, name):
        pass



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
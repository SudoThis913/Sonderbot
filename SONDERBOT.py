#!/bin/env/python3
# SONDERBOT - (C) Greg Norris 2019-2020
# Simple SSL-IRC Chat Bot
# from IRCCON import *
#### BOTCLIENT(server, port,channel,botnick,botnick2,botnick3,botnickpass,botpass)


###### PROGRAM STRUCTURE ######
#   dotenv file required ".env", see "sample.env" file for reference.
#
#   IRCCON - handles the IRC connection to the IRC server.
#       -Contains: connect, joinChannel, send, get_response, get_names, whisper
#
#   BOTCLIENT: Contains bot functions, commands list, apps, main event loop.
#       -Creates IRCCON class.
#       -All command scripts rely on Messages:(Channel, User, Message) input
#       -All command scripts have return functions: to_channel[Messages], and to_user[Messages]
#
#   WORKING FUNCTIONS: (default trigger is: "!")
#       Count Fucks
#           -Counts the number of times each user has said the word "fuck",
#               -returns leader-board of top 5 users with highest score
#
#   FUNCTIONS IN PROGRESS:
#       All addons are initialized in the array appList[] as their own class items.
#       Addons are called sequentially from the array and have input(), to_channel(), to_user invoked().
#
#       SPYFALL: (Addon)
#           Start Spyfall
#               -Social deduction game, all players except the spy know the location, only the spy knows they are the spy.
#               -Input(message), Output: to_channel, to_player
#           Stop Spyfall
#               -Stop the Spyfall game
#       GREEN GLASS DOOR: (Addon)
#           Start Green Glass Door
#               -Word game which asks players to choose an item to pass through the door.
#               -Input(message), Output: to_channel, to_player

#from importlib import reload  # allows dynamic reloading of modules
#import logging
#import importlib
import time, os, traceback
from dotenv import load_dotenv
from IRC_CON import *

#############################################################################
#                                BOTCLIENT                                  #
#############################################################################
class BOTCLIENT:
    #### BOTCLIENT(port,channel,botnick,botnick2,botnick3,botnickpass,botpass) ####
    ##IRC CONFIG###
    botRunning = True
    start_time = 0
    trigger = "!"
    irc = IRCCON()
    accessList = {}
    channel_queue = []
    whisper_queue = []
    channelList = []
    appsList = {}
    active_apps_list = {}
    error_count = 0

    def __init__(self, **botconfig):
        # initiate IRC connection
        self.irc.connect(**botconfig)
        self.irc.joinchannel(botconfig["channel"])
        self.channelList.append(botconfig["channel"])
        self.users = self.irc.get_names(botconfig["channel"], True)

        #############################################################################
        self.bot_running()  # MAIN EVENT LOOP
        #############################################################################

    # *************** MAIN EVENT LOOP ****************************
    def bot_running(self):
        magic_character = "!"
        trigger = magic_character
        #############################################################
        while self.botRunning and self.error_count == 0:
            t = self.irc.get_response()
            # prints chat text to window
            print(t)
            #self.commands(t)
            self.speak()
    # ************** MAIN EVENT LOOP *****************************

    def speak(self):
        floodLimit = 8
        floodCount = 0
        if floodCount <= floodLimit:
            for chan_msg in self.channel_queue:
                self.irc.send(str(chan_msg["channel"]), str(chan_msg["message"]))
            for whisper in self.whisper_queue:
                self.irc.whisper(whisper["channel"], whisper["user"], whisper["message"])
        else:
            time.sleep(3)
        self.channel_queue.clear()
        self.whisper_queue.clear()

    def acl(self, username, permission):
        access = False
        accessControlList = {"Sonder": 69, "rachel": 69}
        if username in accessControlList:
            access = True
        return access

    def get_apps(self):
        pass

def get_config():
    # Loads bot configuration from .env file
    load_dotenv()
    botconfig = {'LOG': os.getenv("SONDERBOT_LOGS"),
                 'BOTNICK': os.getenv("SONDERBOT_BOTNICK"),
                 'BOTNICK2': os.getenv("SONDERBOT_BOTNICK2"),
                 'BOTNICK3': os.getenv("SONDERBOT_BOTNICK3"),
                 'CHANNEL': os.getenv("SONDERBOT_CHANNEL"),
                 'TRIGGER': os.getenv("SONDERBOT_TRIGGER"),
                 'ACL': os.getenv("SONDERBOT_ACL"),
                 'SERVER': os.getenv("SONDERBOT_SERVER"),
                 'PORT': os.getenv("SONDERBOT_PORT"),
                 'BOTNICKPASSWD': os.getenv("SONDERBOT_BOTNICKPASSWD")}
    return botconfig

###########################    MAIN    ############################################
def main():
    try:
        # Pull configuration from get_config(). Allows for multiple bots to be run from the same Sonderbot client.
        botconfig = get_config()
        bot = BOTCLIENT(**botconfig)
    except Exception:
        traceback.print_exc()
        pass

if __name__ == '__main__':
    main()
###########################    MAIN    ############################################

# TODO - LOGGING
# class Logger():
#    logger = logging.getLogger('SONDERBOT')
#    hdlr = logging.FileHandler

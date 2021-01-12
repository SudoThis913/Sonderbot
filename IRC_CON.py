import socket
import ssl
import time
import traceback


##########################################
# IRCCON -> BOTCLIENT -> (MESSAGE{user:, message:}) -> Commands -> (sendout[])
##########################################
class IRCCON:
    irc = socket.socket()
    read_buffer = ""
    server = ""
    port = ""
    botnick = ""
    botnick2 = ""
    botnick3 = ""
    botnickpass = ""
    channel = "#botspam"
    channelList = {}
    users = []
    RPL_NAMESREPLY = '353'
    RPL_ENDOFNAMES = '366'
    botconfig = ""

    def __init__(self):
        # self.context = ssl.create_default_context()
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #   with self.context.wrap_socket(sock server_hostname = hostname) as irc:


        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc = ssl.wrap_socket(self.irc)
        #context.wrap_socket(self.irc)
        self.irc.setblocking(True)

    def connect(self, **botconfig):
        self.botconfig = botconfig
        self.server = str(botconfig['SERVER'])
        self.port = int(botconfig['PORT'])
        self.botnick = str(botconfig['BOTNICK'])
        self.botnick2 = str(botconfig['BOTNICK2'])
        self.botnick3 = str(botconfig['BOTNICK3'])
        self.botpass = str(botconfig['BOTPASS'])

        # connect to server
        print("connecting to: " + str(self.server))
        self.irc.connect((self.server, self.port))

        # Authenticate User
        self.irc.send(bytes("PASS spyfall \n", "UTF-8"))
        # User authentication
        self.irc.send(bytes("USER " + self.botnick + " " + self.botnick2 + " " + self.botnick3 + " :SonderBot\n", "UTF-8"))
        self.irc.send(bytes("NICK " + self.botnick + "\n", "UTF-8"))
        time.sleep(1)
        #self.irc.send(bytes("NICKSERV IDENTIFY " + self.botpass + " " + self.botpass + "\n", "UTF-8"))
        #self.irc.send(bytes("JOIN " + self.channel + "n", "UTF-8"))

    def joinchannel(self, channel):
        time.sleep(2)
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
        print("JOINING CHANNEL!!!" + channel)


    def send(self, channel, msg):
        print(channel)
        print(msg)
        print("SEND:" + str(channel) + " " + str(msg))
        self.irc.send(bytes("PRIVMSG " + channel + " " + str(msg) + "\n", "UTF-8"))

    def whisper(self, channel, user, msg):
        channel = channel[1:]
        user = user[1:]
        print(channel + " " + user)
        # self.irc.send(bytes("PRIVMSG " + channel + ':/msg ' + user + " " + msg + "\n", "UTF-8"))
        print("PRIVMSG #" + channel + ' :/msg ' + user + " " + msg + "\r\n")
        self.irc.send(bytes("PRIVMSG " + user + " :" + msg + "\r\n", "UTF-8"))

    def echo(self, channel, user, msg):
        channel = channel[1:]
        user = user[1:]

    def get_response(self):
        time.sleep(.1)
        response = ""
        try:
            response = self.irc.recv(4096).decode("UTF-8")  # 2040
            if response.find('PING') != -1:
                self.irc.send(bytes('PONG ' + response.split()[1].encode('UTF-8').decode('UTF-8') + '\r\n', "UTF-8"))
                # self.irc.send(bytes("PONG", "UTF-8"))
                print("RESPONSE" + str(response))
        except ValueError:
            traceback.print_exc()
        except Exception:
            traceback.print_exc()
            #timesAttempted=3
            #while timesAttempted > -1:
            #    time.sleep(15)
            #    try:
            #        timesAttempted = timesAttempted -1
            #        print("******** ATTEMPTING TO RECONNECT ***********")
            #        self.connect(**self.botconfig)

             #       continue
            ##    except Exception:
            #        traceback.print_exc()
            #        if timesAttempted == 0:
            #            print("Error - Shutting Down. IRC_CON get_response self.connect()")
            #            return None
            #            #self.botrunning=False
        return response

    def get_names(self, in_channel, firstRun):
        gotNames = False
        if firstRun == False:
            self.irc.send(bytes('NAMES ' + in_channel + '\r\n', "UTF-8"))
        while gotNames == False:
            time.sleep(.3)
            self.read_buffer += self.get_response()
            lines = self.read_buffer.split('\r\n')
            self.read_buffer = lines.pop()
            print(self.read_buffer)
            for line in lines:
                response = line.rstrip().split(' ', 3)
                response_code = response[1]
                if response_code == self.RPL_NAMESREPLY:
                    names_list = response[3].split(':')[1]
                    print(names_list)
                    self.users += names_list.split(' ')
                if response_code == self.RPL_ENDOFNAMES:
                    gotNames = True
        return self.users

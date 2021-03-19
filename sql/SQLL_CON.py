#!/usr/bin/python3
import sqlite3 as sql3
import datetime

"""
Database connection package.
Uses SQLITE.
Will be rewritten as async task

**REQUIRES USER INPUT SANITIZATION BEFORE IMPLEMENTATION**

"""

class DBconn:

    def __init__(self):
        self.conn = sql3.connect("sonderbot.db")
        commands = {}  #Dictionary of expected db commands (add, remove, etc)
        print("connected to sonderbot.db")

        # INITIALIZE TABLES
        self.conn.execute("""""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS IRCCONFIG
                        (
                        HOSTID      INTEGER     PRIMARY KEY AUTOINCREMENT,
                        CONTYPE     CHAR(10)    NOT NULL,
                        HOSTNAME    CHAR(120)   NOT NULL UNIQUE,
                        PORT        INT         NOT NULL,
                        BOTNICK     CHAR(120)   NOT NULL,
                        BOTNICK2    CHAR(120)   NOT NULL,
                        BOTNICK3    CHAR(120)   NOT NULL,
                        BOTPASS     CHAR(120)   NOT NULL    
                        );
                    """)

        print("IRCCONFIG table exists.")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS CHANNELS
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CONTYPE     CHAR(10)    NOT NULL,
                        HOSTID      INTEGER     NULL,
                        HOSTNAME    CHAR(120)   NOT NULL,
                        CHANNEL     CHAR(120)   NOT NULL UNIQUE,
                        STATUS      CHAR(120)   NULL,
                        ACTIVE      BOOLEAN     NULL,
                        AUTOJOIN    BOOLEAN     NULL    
                        );
                    """)
        print("CHANNELS table exists.")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS USERS
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            CONTYPE     CHAR(10)    NOT NULL,
                            HOSTNAME    CHAR(120)   NOT NULL UNIQUE,
                            USER        CHAR(120)   NOT NULL UNIQUE,
                            ACCESS      INTEGER     NULL    
                            );
                        """)
        print("USERSCONFIG table exists.")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS IRCLOG
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TIMESTAMP    TEXT       NOT NULL,
                        HOSTID      CHAR(120)   NOT NULL,    
                        HOSTNAME    CHAR(120)   NOT NULL,
                        CHANNEL     CHAR(120)   NULL,
                        USER        CHAR(120)   NULL,
                        MESSAGE     TEXT        NULL
                        );
                    """)
        print("IRC table exists")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS BOTLOG
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TIMESTAMP    TEXT        NOT NULL,
                        COMMAND     CHAR(120)       NULL,
                        ERROR       TEXT            NULL,
                        DESC        TEXT            NULL
                        );
                    """)
        print("BOTLOG table exists")
        self.conn.close()

    def db_close(self):
        self.conn.close()

    def add_user(self, contype, hostname, user, access):
        try:
            self.conn = sql3.connect("sonderbot.db")
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO USERS
                (CONTYPE,HOSTNAME,USER,
                ACCESS)
                VALUES(?,?,?,?);''',
                (contype,hostname,user,access))
            self.conn.commit()
            print("added "+user)
            self.conn.close()
        except Exception as e:
            print(e)

    def get_users(self):
        userslist = []
        self.conn = sql3.connect("sonderbot.db")
        cur = self.conn.cursor()
        cur.execute("""SELECT HOSTNAME, USER, ACCESS FROM USERS""")
        users = cur.fetchall()

        for row in users:
            userslist.append(self.dictionary_factory(cur,row))
        self.conn.close()
        return userslist

    def remove_user(self,hostname,user):
        try:
            self.conn = sql3.connect("sonderbot.db")
            cursor = self.conn.cursor()
            cursor.execute(
                '''DELETE FROM USERS WHERE HOSTNAME=? AND USER=?;''', (hostname. user))
            self.conn.commit()
            print("removed " + user)
            self.conn.close()
        except Exception as e:
            print(e)

    def edit_user(self, contype, hostname, user, access):
        try:
            self.conn = sql3.connect("sonderbot.db")
            self.remove_user(hostname,user)
            self.add_user(contype,hostname,user,access)
            self.conn.close()
        except Exception as e:
            print(e)

    def add_connection(self,contype, hostname, port, botnick,
                       botnick2, botnick3, botpass):
        try:
            self.conn = sql3.connect("sonderbot.db")
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO IRCCONFIG
                (CONTYPE,HOSTNAME,PORT,BOTNICK,BOTNICK2,BOTNICK3,BOTPASS) \
                VALUES(?,?,?,?,?,?,?);''',
                (contype,hostname,port,botnick,botnick2,botnick3,botpass))
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)

    def remove_connection(self, del_host):
        self.conn = sql3.connect("sonderbot.db")
        cursor = self.conn.cursor()
        cursor.execute(
            '''DELETE FROM IRCCONFIG WHERE HOSTNAME=?;''',del_host)
        self.conn.commit()
        self.conn.close()

    def get_connections(self):
        connectionslist = []
        self.conn = sql3.connect("sonderbot.db")
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM IRCCONFIG""")
        users = cur.fetchall()
        for row in users:
            connectionslist.append(self.dictionary_factory(cur,row))
        self.conn.close()
        return connectionslist

    def add_channel(self,contype,hostname,channel,status,active,autojoin):
        try:
            self.conn = sql3.connect("sonderbot.db")
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO CHANNELS
                (CONTYPE,HOSTNAME,CHANNEL,STATUS,ACTIVE,AUTOJOIN) \
                VALUES(?,?,?,?,?,?);''',
                (contype, hostname, channel, status, active, autojoin))
            self.conn.commit()
            print("added " + hostname)
            self.conn.close()
        except Exception as e:
            print(e)

    def get_channels(self, hostname):
        self.conn = sql3.connect("sonderbot.db")
        cur = self.conn.cursor()
        cur.execute("""SELECT HOSTID, HOSTNAME, CHANNEL FROM CHANNELS WHERE HOSTNAME=?""", (hostname,))
        users = cur.fetchall()
        channels_list = []
        for row in users:
            channels_list.append(self.dictionary_factory(cur, row))
        self.conn.close()
        return channels_list

    def remove_channel(self, del_host, del_channel):
        self.conn = sql3.connect("sonderbot.db")
        cursor = self.conn.cursor()
        cursor.execute(
            '''DELETE FROM CHANNELS WHERE HOSTNAME=?;''',del_host)
        self.conn.commit()
        self.conn.close()

    def add_irc_log(self,hostid, hostname, channel, user, message):
        try:
            self.conn = sql3.connect("sonderbot.db")
            cursor = self.conn.cursor()
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                '''INSERT INTO IRCLOG
                (TIMESTAMP,HOSTID,HOSTNAME,CHANNEL,USER,MESSAGE)
                VALUES(?,?,?,?,?,?);''',
                (timestamp, hostid, hostname, channel, user, message))
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)

    def get_irc_channel_log(self,hostname, channel):
        self.conn = sql3.connect("sonderbot.db")
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM IRCLOG WHERE HOSTNAME=? AND CHANNEL=?""", (hostname,channel))
        users = cur.fetchall()
        loglist = []
        for row in users:
            print(str(row)+" "+str(users))
            loglist.append(self.dictionary_factory(cur,row))
        self.conn.close()
        return loglist

    def dictionary_factory(self,cursor, row):
        # Turns SQL3 queries into dictionaries.
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


if __name__ == '__main__':
    # ALL MAIN METHODS ARE TEST CASES
    db = DBconn()
    db.add_connection('0001','IRC', 'irc.wetfish.net', 6697, 'sonderbot','sonderbot2','sonderbot3','sbpass')
    db.get_connections()
    db.add_user('IRC', 'irc.wetfish.net', 'Sonder',  '5')
    db.get_users()
    db.add_channel('IRC', 'irc.wetfish.net', '#botspam', 'Joined', True, True)
    db.get_channels('irc.wetfish.net')
    db.get_irc_channel_log('irc.wetfish.net', '#botspam')
    db.add_irc_log('0001','irc.wetfish.net','#botspam','Sonder','WEEE I\'M A BOT')
    db.get_irc_channel_log('irc.wetfish.net','#botspam')
    db.conn.close()

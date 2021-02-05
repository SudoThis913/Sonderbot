#!/usr/bin/python3
import sqlite3 as sql3


"""
Database connection package.
Uses SQLITE.
Will be rewritten as async task

**REQUIRES USER INPUT SANITIZATION BEFORE IMPLEMENTATION**

"""

class DBconn:
    conn = sql3.connect("sonderbot.db")
    def __init__(self):
        commands = {}  #Dictionary of expected db commands (add, remove, etc)
        print("connected to sonderbot.db")

        # INITIALIZE TABLES

        self.conn.execute("""CREATE TABLE IF NOT EXISTS IRCCON
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CONTYPE     CHAR(10)    NOT NULL,
                        HOSTNAME    CHAR(120)   NOT NULL UNIQUE,
                        PORT        INT         NOT NULL,
                        BOTNICK     CHAR(120)   NOT NULL,
                        BOTNICK2     CHAR(120)  NOT NULL,
                        BOTNICK3     CHAR(120)  NOT NULL,
                        BOTPASS     CHAR(120)   NOT NULL    
                        );
                    """)

        print("IRCCONFIG table exists.")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS CHANNELS
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CONTYPE     CHAR(10)    NOT NULL,
                        HOSTNAME    CHAR(120)   NOT NULL,
                        CHANNEL     CHAR(120)   NOT NULL UNIQUE,
                        STATUS      CHAR(120)    NULL,
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

    def db_close(self):
        self.conn.close()

    def add_user(self, contype, hostname, user, access):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO USERS
                (CONTYPE,HOSTNAME,USER,
                ACCESS)
                VALUES(?,?,?,?);''',
                (contype,hostname,user,access))
            self.conn.commit()
            print("added "+user)
        except Exception as e:
            print(e)

    def get_users(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT HOSTNAME, USER, ACCESS FROM USERS""")
        users = cur.fetchall()
        for row in users:
            print(row)

    def remove_user(self,hostname,user):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''DELETE FROM USERS WHERE HOSTNAME=? AND USER=?;''', (hostname. user))
            self.conn.commit()
            print("removed " + user)
        except Exception as e:
            print(e)
    def edit_user(self, contype, hostname, user, access):
        try:
            self.remove_user(hostname,user)
            self.add_user(contype,hostname,user,access)
        except Exception as e:
            print(e)
    def add_connection(self, contype, hostname, port, botnick,
                       botnick2, botnick3, botpass):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO IRCCON
                (CONTYPE,HOSTNAME,PORT,BOTNICK,BOTNICK2,BOTNICK3,BOTPASS) \
                VALUES(?,?,?,?,?,?,?);''',
                (contype,hostname,port,botnick,botnick2,botnick3,botpass))
            self.conn.commit()
            print("added "+hostname)
        except Exception as e:
            print(e)

    def remove_connection(self, del_host):
        cursor = self.conn.cursor()
        cursor.execute(
            '''DELETE FROM IRCCON WHERE HOSTNAME=?;''',del_host)
        self.conn.commit()
        print("removed "+del_host)

    def get_connections(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT HOSTNAME, PORT, BOTNICK FROM IRCCON""")
        users = cur.fetchall()
        for row in users:
            print(row)

    def add_channel(self,contype,hostname,channel,status,active,autojoin):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO CHANNELS
                (CONTYPE,HOSTNAME,CHANNEL,STATUS,ACTIVE,AUTOJOIN) \
                VALUES(?,?,?,?,?,?);''',
                (contype, hostname, channel, status, active, autojoin))
            self.conn.commit()
            print("added " + hostname)
        except Exception as e:
            print(e)

    def get_channels(self, hostname):
        cur = self.conn.cursor()
        cur.execute("""SELECT HOSTNAME, CHANNEL FROM CHANNELS WHERE HOSTNAME=?""", (hostname,))
        users = cur.fetchall()
        for row in users:
            print(row)

if __name__ == '__main__':

    db = DBconn()
    db.add_connection('IRC', 'irc.wetfish.net', 6697, 'sonderbot','sonderbot2','sonderbot3','sbpass')
    db.get_connections()
    db.add_user('IRC', 'irc.wetfish.net', 'Sonder',  '5')
    db.get_users()
    db.add_channel('IRC', 'irc.wetfish.net', '#botspam', 'Joined', True, True)
    db.get_channels('irc.wetfish.net')
    db.conn.close()

#!/usr/bin/python3
import sqlite3 as s3


"""
Database connection package.
Uses SQLITE.
Will be rewritten as async task

**REQUIRES USER INPUT SANITIZATION BEFORE IMPLEMENTATION**

"""

class DBconn:
    db_commands = {}  #Dictionary of expected db commands (add, remove, etc)
    conn = s3.connect("sonderbot.db")
    print("connected to sonderbot.db")

    conn.execute("""CREATE TABLE IF NOT EXISTS IRCCONFIG
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

    conn.execute("""CREATE TABLE IF NOT EXISTS CHANNELSCONFIG
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CONTYPE     CHAR(10)    NOT NULL,
                    HOSTNAME    CHAR(120)   NOT NULL UNIQUE,
                    CHANNEL     CHAR(120)   NOT NULL UNIQUE,
                    STATUS      CHAR(60)    NULL,
                    ACTIVE      BOOLEAN     NULL    
                    );
                """)
    print("CHANNELSCONFIG table exists.")

    conn.execute("""CREATE TABLE IF NOT EXISTS USERSCONFIG
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CONTYPE     CHAR(10)    NOT NULL,
                        HOSTNAME    CHAR(120)   NOT NULL UNIQUE,
                        USER        CHAR(120)   NOT NULL UNIQUE,
                        ACCESS INTEGER          NULL    
                        );
                    """)
    print("USERSCONFIG table exists.")

    conn.execute("""CREATE TABLE IF NOT EXISTS IRCLOG
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TIMESTAP    TEXT        NOT NULL,
                    HOSTNAME    CHAR(120)   NOT NULL,
                    CHANNEL     CHAR(120)   NULL,
                    USER        CHAR(120)   NULL,
                    MESSAGE     TEXT        NULL
                    );
                """)
    print("IRC table exists")

    conn.execute("""CREATE TABLE IF NOT EXISTS BOTLOG
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TIMESTAP    TEXT        NOT NULL,
                    COMMAND     CHAR(120)       NULL,
                    ERROR       TEXT            NULL,
                    DESC        TEXT            NULL
                    );
                """)
    print("BOTLOG table exists")

    conn.execute("""INSERT INTO IRCCONFIG (CONTYPE, HOSTNAME, PORT, BOTNICK, BOTNICK2, BOTNICK3, BOTPASS) \
                    VALUES('IRC','irc.wetfish.net',6697,'Sonderbot','Biggus_Dickus','Henry_Fondle','sbPass') ");
                """)


    conn.close()



    def db_insert(self, in_var):
        conn = s3.connect("sonderbot.db")
        conn.close()

    def db_select(self, in_var):
        conn = s3.connect("sonderbot.db")
        cursor = conn.execute(in_var)
        conn.close()

    def add_user(self,in_var):
        pass

    def remove_user(self,in_var):
        pass

    def acl_user(self, in_var):
        pass

    def add_connection(self,in_var):
        pass

    def remove_connection(self, in_var):
        pass

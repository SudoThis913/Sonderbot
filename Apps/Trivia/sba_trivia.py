import csv
import datetime
import time
import threading
import random
import re
import asyncio
#216931 approximate number of trivia questions
"""
Very much under development, consists of random psudocode
and poorly written code.


"""
class Trivia:
    output = []
    input = []
    time = datetime.time()

    def __init__(self, trigger):
        print ("On")
        Q = Questions()
    def input(self, channel, user, message):
        pass

    def output(self):
        return self.output

    def tcommands(self, channel, user, message):
        dispatch = {
            trigger+"next": tNext,
            trigger+"stop": tStop,
            trigger+"answer": tAnswer,
        }
        if message in dispatch:
            dispatch[message]()
    def tNext(self):
        pass

    def tTimer(self):
        duration = 10

    def tAsk(self):
        pass

class Questions:
    categories = {}
    questions = []
    question =  {'Show': "1",
                    'Number': "2",
                    'Air': "3",
                    'Date': "4",
                    'Round': "5",
                    'Category': "6",
                    'Value':"7",
                    'Question':"8",
                    'Answer': "9",
                    'PK' : 0
                 }
    def __init__(self):
        print("Questions")
        with open ('JEOPARDY_CSV.csv', newline = '', encoding = 'UTF=8') as csvfile:
            sr = csv.reader(csvfile, delimiter=",")
            count = 0
            #216931 lines in Trivia file
            for row in sr:
                #assign primary key while parsing file
                count = count + 1
                question = {
                 'PK' : count,
                 'Show Number': row[0],
                 'Air Date': row[1],
                 'Round': row[2],
                 'Category': row[3],
                 'Value': row[4],
                 'Question': row[5],
                 'Answer':row[6],
                 }
                if question['Category'] not in self.categories:
                    #save the top $100/$200 questions for every category
                    if (question['Value'] == "$100") or (question['Value'] == "$200"):
                        if "www." in question['Question']:
                            print ("SKIPPING: "+question['Answer'])
                            pass
                        else:
                            #5867 total $100 questions
                            #18489 total 100+200 questions
                            self.categories[question['Category']] = question
                            #print (question['Air Date'])
            print (len(self.categories))



if __name__ == "main":
    print("START")
    c = Questions()
    print ("END")
else:
    c = Questions()

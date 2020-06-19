#import sqlite3
#from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
#
# sched = BlockingScheduler()
# conn = sqlite3.connect('Test.db')
# curs = conn.cursor()
#
# @sched.scheduled_job('interval', minutes=.5)
# def timed_job():
#     for i in range(2,6):
#         curs.execute('INSERT INTO Name(ID) VALUES(i);')
#         conn.commit()
#         print('{} is inserted into the DB'.format(i))
#
# sched.start()

import schedule
import time

def job():
    for i in range(1,5):
        print("I'm working", i)

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
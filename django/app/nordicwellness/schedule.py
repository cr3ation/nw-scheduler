import schedule
import time

def job():
    print("I'm working...")

schedule.every(1).second(job)
from apscheduler.scheduler import Scheduler
import os 

sched = Scheduler()

@sched.interval_schedule(minutes=60)
def timed_job():
    print 'This job is run every three minutes.'

sched.start()

while True:
	pass
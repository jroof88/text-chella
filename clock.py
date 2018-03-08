from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=10, timezone='US/Pacific')
def text_chella():
    #text_chella()
    
sched.start()
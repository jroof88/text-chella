from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=18, minute=15, timezone='US/Pacific')
def send_text():
    text_chella()
    
sched.start()
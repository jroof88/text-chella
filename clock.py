from text_chella import text_chella
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=19, minute=20, timezone='US/Pacific')
def send_text():
    text_chella()


sched.start()

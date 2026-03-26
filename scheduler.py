"""
Scheduler: Auto-run pipeline twice daily.
Uses Python schedule library instead of crontab.
"""
import schedule
import time
from datetime import datetime
from main import run_pipeline
from config import SCHEDULE_TIME_1, SCHEDULE_TIME_2


def job():
    print(f"\n[SCHEDULER] Job started at {datetime.now()}")
    try:
        run_pipeline()
    except Exception as e:
        print(f"[SCHEDULER ERROR] {e}")


# Register schedule
schedule.every().day.at(SCHEDULE_TIME_1).do(job)
schedule.every().day.at(SCHEDULE_TIME_2).do(job)

print(f"[SCHEDULER] Registered times: {SCHEDULE_TIME_1}, {SCHEDULE_TIME_2}")
print("[SCHEDULER] Waiting for next scheduled run...")

while True:
    schedule.run_pending()
    time.sleep(60)

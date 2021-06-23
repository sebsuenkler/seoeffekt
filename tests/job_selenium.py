#background scheduler for scraping
import sys
import os
import time



#processing libraries
import threading
from subprocess import call
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

def job():
    os.system('python3 google_selenium.py')

if __name__ == '__main__':
    scheduler = BackgroundScheduler(job_defaults=job_defaults)
    scheduler.add_job(job, 'interval', seconds=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

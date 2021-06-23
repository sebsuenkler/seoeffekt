#sub processes to scrape
import sys
import os
import time

#processing libraries
import threading
from subprocess import call
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def scraper():
    call(["python3", "job_selenium.py"])


process1 = threading.Thread(target=scraper)

process1.start()

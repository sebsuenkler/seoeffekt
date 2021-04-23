#sub processes to start all apps
import sys
sys.path.insert(0, '..')
from include import *

def indicators():
    call(["python3", "proc_indicators.py"])

def scraper():
    call(["python3", "proc_scraper.py"])

def speed():
    call(["python3", "proc_speed.py"])

def bing_api():
    call(["python3", "proc_bing.py"])

def google_selenium():
    call(["python3", "proc_google_selenium.py"])



process1 = threading.Thread(target=scraper)
process2 = threading.Thread(target=indicators)
process3 = threading.Thread(target=speed)
process4 = threading.Thread(target=bing_api)
process5 = threading.Thread(target=google_selenium)

process1.start()
process2.start()
process3.start()
process4.start()
process5.start()

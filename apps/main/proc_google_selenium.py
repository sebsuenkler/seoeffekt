#sub processes to scrape
import sys
sys.path.insert(0, '..')
from include import *

def google_selenium():
    call(["python3", "job_google_selenium.py"])

process1 = threading.Thread(target=google_selenium)

process1.start()

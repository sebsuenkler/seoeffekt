#sys libs
import os, sys
import hashlib
from datetime import date
from datetime import datetime
import fnmatch

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class Helpers:
    def __init__(self):
        self.data = []

    def computeMD5hash(string):
        m = hashlib.md5()
        m.update(string.encode('utf-8'))
        return m.hexdigest()

    def changeCoding(source):
        if type(source) == str:
            source = source.encode('utf-8')
        else:
            source = source.decode('utf-8')

        return str(source, 'utf-8', 'ignore')

    def saveLog(file_name, content, show):
        log_now = datetime.now()
        log_now = log_now.strftime('%Y-%m-%d_%H%M%S')
        log_path = os.getcwd() + "//" + file_name
        with open(log_path,'a+') as f:
            log_now = log_now+'\n'
            f.write(log_now)
            if(show == 1):
                print(log_now)
                c = content+'\n'
                f.write(c)
                if(show == 1):
                    print(c)
        f.close()

    def html_escape(text):
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
            "#": "&hash;"
        }
        """Produce entities within text."""
        return "".join(html_escape_table.get(c,c) for c in text)

    def html_unescape(text):
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&quot;", '"')
        text = text.replace("&apos;", "'")
        text = text.replace("&hash;", "#")
        # this has to be last:
        text = text.replace("&amp;", "&")
        return text

    def matchText(text, pattern):
        text = text.lower()
        pattern= pattern.lower()
        check = fnmatch.fnmatch(text, pattern)
        return check

    def remove_duplicates_from_list(a_list):
        b_set = set(tuple(x) for x in a_list)
        b = [ list(x) for x in b_set ]
        b.sort(key = lambda x: a_list.index(x) )
        return b

    def saveResult(url):

        os.environ['MOZ_HEADLESS'] = '0'
        options = Options()
        #options.add_argument('--ignore-certificate-errors-spki-list')
        #options.add_argument('--ignore-ssl-errors')
        #options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--allow-insecure-localhost')
        options.add_argument("user-data-dir=selenium")
        options.log.level = 'error'

        profile = webdriver.FirefoxProfile()

        profile.set_preference("browser.safebrowsing.blockedURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.downloads.enabled", True)
        profile.set_preference("browser.safebrowsing.enabled", True)
        profile.set_preference("browser.safebrowsing.forbiddenURIs.enabled", True)
        profile.set_preference("browser.safebrowsing.malware.enabled", True)
        profile.set_preference("browser.safebrowsing.phishing.enabled", True)
        profile.set_preference("dom.webnotifications.enabled", False);

        driver = webdriver.Firefox(firefox_profile=profile, options=options)

        driver.set_page_load_timeout(60)



        try:
            driver.get(url)
            source = driver.page_source


        except:
            source = "error"

        driver.quit()

        return source

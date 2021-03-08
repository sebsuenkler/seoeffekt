from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import time

import os

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

    #profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

    driver = webdriver.Firefox(firefox_profile=profile, options=options)

    driver.set_page_load_timeout(120)

    try:
        driver.get(url)
        time.sleep(10)
        source = driver.page_source


    except:
        source = "error"

    driver.quit()

    return source

url = "https://www.spiegel.de"

s = saveResult(url)

print(s)

file = "test.html"

with open(file,'w+') as f:
    f.write(s)
f.close()

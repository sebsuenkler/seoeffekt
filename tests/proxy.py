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

    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    PROXY = "185.198.188.55:8080"

    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY
    }

    driver = webdriver.Firefox(firefox_profile=profile, options=options, capabilities=firefox_capabilities)

    driver.set_page_load_timeout(120)

    try:
        driver.get(url)
        #time.sleep(10)
        source = driver.page_source


    except Exception as e:
        print(e)
        source = "error"

    driver.quit()

    return source

#url = "https://www.show-my-ip.de/ipadresse/"

url = "https://www.google.de/search?q=merkel&start=20&lr=lang_de&cr=countryDE"

s = saveResult(url)

print(s)

file = "test.html"

with open(file,'w+') as f:
    f.write(s)
f.close()

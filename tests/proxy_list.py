#sys libs
import os, sys
import os.path
import json

#scraping libs
from urllib.parse import urlsplit
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

from lxml import html
from bs4 import BeautifulSoup, Comment
import lxml.html
import os

from urllib.parse import urlsplit
from urllib.parse import urlparse
import urllib.parse
import socket

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.results import Results as DB_Results

from libs.helpers import Helpers

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

    profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

    driver = webdriver.Firefox(firefox_profile=profile, options=options)

    driver.set_page_load_timeout(60)


    try:
        driver.get(url)
        time.sleep(10)
        source = driver.page_source


    except:
        source = "error"

    driver.quit()

    source = Helpers.changeCoding(source)

    return source

url = "https://hidemy.name/de/proxy-list/?type=s#list"

#url = "https://www.google.de/search?q=merkel&start=20&lr=lang_de&cr=countryDE"

#s = saveResult(url)

ips = "//div[@class='table_block']//tr//td[1]/text()"
ports = "//div[@class='table_block']//tr//td[2]/text()"



file = "proxies.html"

'''
with open(file,'w+') as f:
    f.write(s)
f.close()
'''

f = open(file, "r")

source = f.read()

tree = html.fromstring(source)

ip = tree.xpath(ips)

port = tree.xpath(ports)

y = 0

proxies = []

for i in ip:
    proxy = i+":"+port[y]
    y = y + 1
    proxies.append(proxy)

print(proxies)

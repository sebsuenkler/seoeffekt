 #scraping libs
import os
import random

from lxml import html

from bs4 import BeautifulSoup
import lxml.html
from bs4 import BeautifulSoup, Comment
import bs4, requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import requests
from urllib.request import urlparse, urljoin

from urllib.parse import urlparse

from urllib.parse import urlsplit

def changeCoding(source):
    if type(source) == str:
        source = source.encode('utf-8')
    else:
        source = source.decode('utf-8')

    return str(source, 'utf-8', 'ignore')

def scrape_url(url):
    results = {}
    urls = []
    page = scrape_content(url)
    if page:
        main = page[0]
        soup = page[3]
        urls = extract_random_urls(main, soup)
        r1 = urls[0]
        r2 = urls[1]
        random_page_1 = scrape_content(r1)
        if not random_page_1:
            random_page_1 = [-1,-1,-1,-1,-1,-1]
        random_page_2 = scrape_content(r2)
        if not random_page_2:
            random_page_2 = [-1,-1,-1,-1,-1,-1]
        results = {'page':page, 'r1':random_page_1, 'r2':random_page_2}
        return results
    else:
        return False


def extract_random_urls(main, soup):
    soup_urls = []
    tags = soup.find_all('a')
    urls = []

    if tags:
        for tag in tags:
            link_text = str(tag.string).strip()
            href = str(tag.get('href')).strip()

            if "http" not in href:
                href = href.lstrip('/')
                href = main+href

            if main in href and not '.pdf' in href and not '.jpg' in href and href != main and not '#' in href:
                urls.append(href)


    u_urls = set(urls)
    urls_r = list(u_urls)
    url1 = urls_r[0]
    url2 = urls_r[-1]
    random_urls = [url1, url2]

    return random_urls

def scrape_content(url):

    os.environ['MOZ_HEADLESS'] = '0'
    options = Options()
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

    if source != "error":

        source = changeCoding(source)

        content = []

        main = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
        soup = BeautifulSoup(source, 'lxml')
        html_source = soup.get_text().strip()
        html_source = html_source.split('\n')
        html_source = set(html_source)
        html_source = list(html_source)
        html_comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        html_comments = set(html_comments)
        html_comments = list(html_comments)
        code = source.lower()
        tree = html.fromstring(code)

        content = [main, html_source, html_comments, soup, code, tree]

        return content

    else:
        return False

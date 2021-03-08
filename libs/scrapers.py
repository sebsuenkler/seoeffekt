#sys libs
import os, sys
import os.path
import json
from datetime import date
import random
import time


#scraping libs
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from lxml import html

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.scrapers import Scrapers as DB_Scrapers

from libs.helpers import Helpers

class Scrapers:
    def __init__(self, search_engine, results_range, search_url, start_parameter, xpath, filter, serp_filter, language):
        self.__search_engine = search_engine
        self.__results_range = results_range
        self.__search_url = search_url
        self.__start_parameter = start_parameter
        self.__xpath = xpath
        self.__filter = filter
        self.__serp_filter = serp_filter
        self.__language = language

    def __getResultsRange(self):
        return self.__results_range

    results_range = property(__getResultsRange)

    def __getSearchEngine(self):
        return self.__search_engine

    search_engine = property(__getSearchEngine)

    def __getSearchURL(self):
        return self.__search_url

    search_url = property(__getSearchURL)


    def __getXpath(self):
        return self.__xpath

    xpath = property(__getXpath)

    def __getStartParameter(self):
        return self.__start_parameter

    start = property(__getStartParameter)

    def __getFilterParameter(self):
        return self.__filter

    filter = property(__getFilterParameter)

    def __getSERPFilterParameter(self):
        return self.__serp_filter

    serp_filter = property(__getSERPFilterParameter)

    def __getLanguage(self):
        return self.__language

    language = property(__getLanguage)


    def scrapeQuery(query, search_xpath, start, filter):

        def extractSearchResults(source, xpath):
            tree = html.fromstring(source)
            urls = tree.xpath(xpath)
            return urls

        today = date.today()
        string_today = str(today)
        results = []

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


        #time.sleep(sleeper)

        driver.get(query)

        source = driver.page_source

        source = Helpers.changeCoding(source)

        #print(source)


        xpath = search_xpath

        urls = extractSearchResults(source, xpath)



        driver.quit()



        i = start

        if urls:
            for url in urls:
                i = i + 1
                results.append(url)

        search_results = list(dict.fromkeys(results))

        res = []


        if search_results:
            res = [search_results, source]
            return res
        else:
            if str(source).find(str(filter)) > 0:
                res = ["filtered", source]
                return res
            else:
                print(source)
                return False

    def generateScrapers():
    #noch dynamischer generieren einfach nach anzahl der scraper, nicht mit google_config und bing_config
        with open('../../config/scraper.ini', 'r') as f:
            array = json.load(f)

        scrapers_json = array['scraper']

        scrapers = []

        for scraper in scrapers_json:
            config = scrapers_json[scraper]
            search_engine = config['search_engine']
            results_range = config['results_range']
            search_url = config['search_url']
            start_parameter = config['start_parameter']
            xpath = config['xpath']
            filter = config['filter']
            serp_filter = config['serp_filter']
            language = config['language']
            scrapers.append(Scrapers(search_engine, results_range, search_url, start_parameter, xpath, filter, serp_filter, language))

        return scrapers

    def getScrapingJobsByProgress(progress):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByProgress(db.cursor, progress)
        db.DBDisconnect()
        return rows

    def insertScrapingJobs(query_id, study_id, query_string, search_engine, start, today):
        db = DB()
        rows = DB_Scrapers.insertScrapingJobs(db.cursor, query_id, study_id, query_string, search_engine, start, today)
        db.DBDisconnect()

    def getScrapingJobsByQueryProgress(query_id, progress):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByQueryProgress(db.cursor, query_id, progress)
        db.DBDisconnect()
        return rows


    def getScrapingJobsByQuery(query):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsByQuery(db.cursor, query)
        db.DBDisconnect()
        return rows

    def getScrapingJobsBySE(query_id, search_engine):
        db = DB()
        rows = DB_Scrapers.getScrapingJobsBySE(db.cursor, query_id, search_engine)
        db.DBDisconnect()
        return rows


    def updateScrapingJobQuery(query_id, progress):
        db = DB()
        DB_Scrapers.updateScrapingJobQuery(db.cursor, query_id, progress)
        db.DBDisconnect()

    def updateScrapingJobQuerySearchEngine(query_id, search_engine, progress):
        db = DB()
        DB_Scrapers.updateScrapingJobQuerySearchEngine(db.cursor, query_id, search_engine, progress)
        db.DBDisconnect()

    def updateScrapingJob(job_id, progress):
        db = DB()
        DB_Scrapers.updateScrapingJob(db.cursor, job_id, progress)
        db.DBDisconnect()

    def resetScrapingJobs():
        db = DB()
        DB_Scrapers.resetScrapingJobs(db.cursor)
        db.DBDisconnect()

    def getScrapingJobs(query_id, study_id, search_engine):
        db = DB()
        DB_Scrapers.getScrapingJobs(db.cursor, query_id, study_id, search_engine)
        db.DBDisconnect()

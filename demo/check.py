import csv

import json

import pandas as pd
import numpy as np

import datetime

import random

import json


from app.libs.scraper import scrape_url
from app.libs.classifier import classify
from app.libs.https import check_https
from app.libs.description import check_description
from app.libs.title import check_title
from app.libs.micros import check_micros
from app.libs.nofollow import check_nofollow
from app.libs.robots import check_robots
from app.libs.speed import get_speed
from app.libs.sitemap import check_sitemap
from app.libs.canonicals import check_canonicals
from app.libs.og import check_og
from app.libs.viewport import check_viewport
from app.libs.plugins import check_plugins

def check_url(url):

    scrape = scrape_url(url)

    if scrape:
        content = scrape.get("page")
        r1 = scrape.get("r1")
        r2 = scrape.get("r2")

        content_main = content[0]
        content_source = content[1]
        content_comments = content[2]
        content_code = content[4]

        content_tree = content[5]
        r1_tree = r1[5]
        r2_tree = r2[5]

        robots = check_robots(content_main)

        plugins = check_plugins(content_source, content_comments)

        classes = classify(url)
        https = check_https(url)
        description = check_description(content_tree)

        title_page = check_title(content_tree)

        check_identical_r1 = 0
        check_identical_r2 = 0

        try:
            title_r1 = check_title(r1_tree)
            check_identical_r1 = 1
        except:
             check_identical_r1 = 0

        try:
            title_r2 = check_title(r2_tree)
            check_identical_r2 = 1
        except:
            check_identical_r2 = 0

        identical_tags = 0

        if check_identical_r1 == 1 and check_identical_r2 == 1:
            if(title_page != title_r1 and title_page != title_r2 and title_r1 != title_r2):
                identical_tags = 0
            else:
                identical_tags = 1
        else:
            identical_tags = -1

        micros = check_micros(content_source, content_comments)

        nofollow = check_nofollow(content_tree)

        speed = get_speed(url)

        sitemap = check_sitemap(content_code)

        canonicals = check_canonicals(content_tree)

        og = check_og(content_code)

        viewport = check_viewport(content_code)

        results = {}

        results.update({'plugins': plugins})
        results.update({'classes': classes})
        results.update({'https': https})
        results.update({'description': description})
        results.update({'title': title_page})
        results.update({'identical title': identical_tags})
        results.update({'micros': micros})
        results.update({'nofollow': nofollow})
        results.update({'speed': speed})
        results.update({'robots': robots})
        results.update({'sitemap': sitemap})
        results.update({'canonicals': canonicals})
        results.update({'og': og})
        results.update({'viewport': viewport})

        #assessment
        res_source_not_optimized = results['classes']['source not optimized']
        seo_not_optimized = 0

        #not optimized
        results.update({'Most probably not optimized': 0})
        if res_source_not_optimized == 1:
            seo_not_optimized = 1
            results.update({'Most probably not optimized': seo_not_optimized})

        #most probably optimized
        results.update({'Most probably optimized': 0})
        seo_t_counter = 0
        seo_optimized = 0
        seo_tools = []

        res_source_known = results['classes']['source known']
        res_source_news = results['classes']['source news']
        res_source_ads = results['classes']['source ads']
        res_micros_counter = results['micros']

        seo_tools_key = results['plugins']['plugins']

        for seo_tool in seo_tools_key:
            seo_t_counter = seo_t_counter + 1

        if seo_not_optimized == 0 and (seo_t_counter > 0 or res_source_known or res_source_news or res_source_ads or res_micros_counter > 0):
            seo_optimized = 1
            results.update({'Most probably optimized': seo_optimized})



        #probably optimized
        results.update({'Probably optimized': 0})
        seo_likely_optimized = 0
        a_t_counter = 0
        analytics_tools_key = results['plugins']['analytics']
        for a_tool in analytics_tools_key:
            a_t_counter = a_t_counter + 1

        res_source_shop = results['classes']['source shop']
        res_source_company = results['classes']['source company']
        res_https = results['https']
        res_robots_txt = results['robots']
        res_sitemap = results['sitemap']
        res_nofollow = results['nofollow']
        res_speed = results['speed']
        res_canonical = results['canonicals']
        res_viewport = results['viewport']
        res_og = results['og']

        if seo_optimized == 0 and seo_not_optimized == 0 and (a_t_counter > 0 or res_source_shop or res_source_company):
            seo_likely_optimized = 1

        if seo_optimized == 0 and seo_likely_optimized == 0:
            if (res_https == 1 or res_og == 1 or res_viewport == 1) or (res_robots_txt == 1 or res_sitemap == 1 or res_nofollow > 0 or res_canonical > 0 and res_speed < 3 and res_speed > 0):
                seo_likely_optimized = 1

        results.update({'Probably optimized': seo_likely_optimized})


        #probably not optimized
        results.update({'Probably not optimized': 0})
        seo_likely_not_optimized = 0
        res_check_title = results['title']
        res_check_description = results['description']
        res_og = results['og']
        res_identical = results['identical title']

        if seo_optimized == 0 and seo_not_optimized == 0 and seo_likely_optimized == 0 and ((not res_check_title or not res_check_description and not res_og) or res_identical == 1):
            seo_likely_not_optimized = 1
            results.update({'Probably not optimized': seo_likely_not_optimized})

        #uncertain
        results.update({'Uncertain': 0})
        seo_unsure = 0

        if seo_optimized == 0 and seo_not_optimized == 0 and seo_likely_optimized == 0 and seo_likely_not_optimized == 0:
            seo_unsure = 1
            results.update({'Uncertain': seo_unsure})

        return results
    else:
        return False

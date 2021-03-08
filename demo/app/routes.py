from flask import render_template, flash, redirect, request, url_for, session
from flask import send_file, send_from_directory, safe_join, abort
from app import app
from app.forms import URLForm

from check import check_url

import requests
from urllib.request import urlparse, urljoin

from urllib.parse import urlparse

from urllib.parse import urlsplit

import csv

import json

import pandas as pd
import numpy as np

from datetime import date
from datetime import datetime

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        session['url'] = url
        return redirect(url_for('processing'))
    return render_template('url.html', title='Sign In', form=form)


@app.route('/processing')
def processing():
    url = session.get('url', None)
    title = 'Processing'+url
    return render_template('loader.html', title=title)

@app.route('/analyze')
def analyze():
    url = session.get('url', None)
    results = check_url(url)

    if results:

        seo_optimized = results['Most probably optimized']
        seo_not_optimized = results['Most probably not optimized']
        seo_likely_optimized = results['Probably optimized']
        seo_likely_not = results['Probably not optimized']
        seo_unsure = results['Uncertain']

        source_ads = results['classes']['source ads']
        source_company = results['classes']['source company']
        source_known = results['classes']['source known']
        source_news = results['classes']['source news']
        source_not_optimized = results['classes']['source not optimized']
        source_shop = results['classes']['source shop']

        description = results['description']
        site_title = results['title']
        identical = results['identical title']
        https = results['https']
        speed = results['speed']
        micros = results['micros']
        nofollow = results['nofollow']
        robots = results['robots']
        viewport = results['viewport']
        canonicals = results['canonicals']

        seo_plugins = results['plugins']['plugins']
        analytics_tools = results['plugins']['analytics']
        
            
        save_main = main = '{0.netloc}/'.format(urlsplit(url))
        save_main = save_main.replace("/", "")
        save_main = save_main.replace("'", "")
        save_main = save_main.replace('"', '')
        save_main = save_main.replace("*", "")
        save_main = save_main.replace(".", "")
        save_main = save_main.replace(":", "")
        save_main = save_main.replace("?", "")
        save_main = save_main.replace(",", "")
        save_main = save_main.replace(";", "")
        content = results
        

        content.update({'Description': 'Most probably optimized: The webpage is most probably optimized when an SEO tool either was found in the HTML code, it is on the list of news services, on the list of customers of SEO agencies, or is on the list with websites with ads, or has at least one microdata.\nProbably optimized: The webpage is not most probably optimized and meets one of the following criteria: (1) It is on the list of shops or business websites, (2) it uses Analytics Tools or advertisement, (3) it uses https, (4) it has SEO indicators in its ro-bots.txt, (5) the website has a sitemap, (6) a viewport is de-fined, (7) it has at least one nofollow link or canonical link, (8) its loading time is less than 3 seconds.\nMost probably not optimized: The main domain is on the list of non-optimized websites.\nProbably not optimized: The webpage is probably not optimized when it is not most probably optimized, it is not classified as not optimized, and it meets at least one of the following criteria: (1) the description tag is empty, (2) the ti-tle tag is empty or identical on subpages, (3) it has no Open Graph tags.'})
        
   
    
        results_folder = "app/results/"
        
        dt = datetime.now() # current date and time

        now = dt.strftime("%m_%d_%Y_%H_%M_%S")
         
        
        file = results_folder+now+"_"+save_main
        json_file = file+".json"
        
        json_file_download = now+"_"+save_main+".json"
        
        with open(json_file, 'w+') as outfile:
            json.dump(content, outfile)
            


        return render_template('analyze.html', title='Results', url=url, results=results, optimized=seo_optimized, not_optimized=seo_not_optimized, m_optimized=seo_likely_optimized, m_not_optimized=seo_likely_not, uncertain=seo_unsure, source_ads = source_ads, source_company = source_company, source_known = source_known, source_news = source_news, source_not_optimized = source_not_optimized, source_shop = source_shop, description=description, site_title = site_title, identical_title = identical, speed=speed, https=https, robots=robots, viewport=viewport, micros = micros, nofollow = nofollow, canonicals=canonicals, seo_plugins=seo_plugins, analytics_tools=analytics_tools)

    else:
        return render_template('error.html', title='Error')
    #merkmale hervorheben, die für die einordung sorgen; verkettung von bedingungen z. b. wennn wahrscheinlich nicht optimiert werden die merkmale fett gemacht


@app.route('/report')
def report():

    results = request.args.get('results', default='', type=str)
    url = request.args.get('url', default='', type=str)


    save_main = main = '{0.netloc}/'.format(urlsplit(url))
    save_main = save_main.replace("/", "")
    save_main = save_main.replace("'", "")
    save_main = save_main.replace('"', '')
    save_main = save_main.replace("*", "")
    save_main = save_main.replace(".", "")
    save_main = save_main.replace(":", "")
    save_main = save_main.replace("?", "")
    save_main = save_main.replace(",", "")
    save_main = save_main.replace(";", "")
    results = results.replace("'",'"')
    content = json.loads(results)
    

    content.update({'Description': 'Most probably optimized: The webpage is most probably optimized when an SEO tool either was found in the HTML code, it is on the list of news services, on the list of customers of SEO agencies, or is on the list with websites with ads, or has at least one microdata.\nProbably optimized: The webpage is not most probably optimized and meets one of the following criteria: (1) It is on the list of shops or business websites, (2) it uses Analytics Tools or advertisement, (3) it uses https, (4) it has SEO indicators in its ro-bots.txt, (5) the website has a sitemap, (6) a viewport is de-fined, (7) it has at least one nofollow link or canonical link, (8) its loading time is less than 3 seconds.\nMost probably not optimized: The main domain is on the list of non-optimized websites.\nProbably not optimized: The webpage is probably not optimized when it is not most probably optimized, it is not classified as not optimized, and it meets at least one of the following criteria: (1) the description tag is empty, (2) the ti-tle tag is empty or identical on subpages, (3) it has no Open Graph tags.'})
    
   
    
    results_folder = "app/results/"
    
    dt = datetime.now() # current date and time

    now = dt.strftime("%m_%d_%Y_%H_%M_%S")
     

    
    file = results_folder+now+"_"+save_main
    json_file = file+".json"
    
    json_file_download = now+"_"+save_main+".json"
    
    with open(json_file, 'w+') as outfile:
        json.dump(content, outfile)
        
    csv_file = file+".csv"
        
    df = pd.read_json(json_file, typ='series', convert_dates=False)
    
    df.to_csv(csv_file)
    
  
    csv_file_download = now+"_"+save_main+".csv"
    
    
    return send_from_directory("/home/sebastian/alpha/demo/app/results/", csv_file_download, as_attachment=True)

    

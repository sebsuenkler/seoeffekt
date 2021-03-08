#done!!!
#sys libs
import sys
sys.path.insert(0, '..')
import json
from datetime import date
from datetime import datetime

#tool libs
from libs.scrapers import Scrapers
from libs.queries import Queries
from libs.results import Results
from libs.studies import Studies
from libs.evaluations import Evaluations
from libs.helpers import Helpers

import random

import collections

import pandas as pd
import numpy as np

import sys

import csv



tools = ['tools analytics', 'tools caching', 'tools seo', 'tools content', 'tools social', 'tools ads']

csv_header = 'Study,ID,Hash,Position,Query_ID,Query,URL,Main,Search Engine,Speed,Classification,check canonical,check description,check external links,check h1,check https,check internal links,check kw_count,check kw_density,check kw_in_description-og-name,check kw_in_description-og-property,check kw_in_href,check kw_in_link-text,check kw_in_meta-content,check kw_in_meta-description,check kw_in_meta-og,check kw_in_meta-properties,check kw_in_source,check kw_in_title,check kw_in_title-meta,check kw_in_title-og,check kw_in_url,check nofollow,check og,check sitemap,check title,check title_h1_identical,check title_h1_match,check viewport,check word_count,check wordpress,micros,micros counter,robots_txt,source ads,source company,source known,source news,source not optimized,source search engine,source shop,source top,tools ads,tools ads count,tools analytics,tools analytics count,tools caching,tools caching count,tools content,tools content count,tools seo,tools seo count,tools social,tools social count'

db_modules = ['check canonical','check description','check external links','check h1','check https','check internal links','check kw_count','check kw_density','check kw_in_href','check kw_in_link-text','check kw_in_meta-content','check kw_in_meta-description','check kw_in_meta-og','check kw_in_meta-properties','check kw_in_source','check kw_in_title','check kw_in_title-meta','check kw_in_title-og','check kw_in_description-og-property','check kw_in_description-og-name','check kw_in_url','check nofollow','check og','check sitemap','check title','check title_h1_identical','check title_h1_match','check viewport','check word_count','check wordpress','micros','micros counter','robots_txt', 'source ads','source company','source known','source news','source not optimized','source shop', 'source search engine','source top', 'tools ads','tools ads count','tools analytics','tools analytics count','tools caching','tools caching count','tools content','tools content count','tools seo','tools seo count','tools social','tools social count']


db_modules = sorted(db_modules, key=str.lower)


save_res = ""

csv_file = 'merged_results_03022021.csv'


with open(csv_file,'w+') as f:
    f.write(csv_header)
f.close()



file = 'seo_results.csv'

eval_results = pd.read_csv(file, error_bad_lines=False, skiprows=0, nrows=10000)

#eval_results = pd.read_csv(file, error_bad_lines=False, low_memory=False)

pd.set_option('display.max_columns', None)



'''
results_studies_id                                                    1
results_id                                                       463846
results_position                                                     56
results_queries_id                                                 1608
results_url           https://www.daserste.de/information/wirtschaft...
results_main                                   https://www.daserste.de/
results_se                                                       Google
hash                                   f977e18d968470c14b0661632b8791c4
 speed                                                           21.566
 module               ['check kw_in_description-og-property', 'micro...
 value                ['0', '0', '0', '0', '1', '0', '1', '0', '5', ...
queries_id                                                         1608
 query                                                       Grundrente
'''

'''
['results_studies_id',
'results_id',
'results_position',
'results_queries_id',
'results_url',
'results_main',
'results_se',
'hash',
'speed',
'module',
'value',
'queries_id',
'query']

['results_studies_id', 'results_id', 'results_position', 'results_queries_id', 'results_url', 'results_main', 'results_se', 'hash', 'speed', 'module', 'result', 'queries_id', 'query', 'class']

'''

#print(list(eval_results.columns))


for index, row in eval_results.iterrows():
    build_res = ""
    hash = str(row[7])

    query_id = str(row[3])
    study = str(row[0])
    results_id = str(row[1])
    results_pos = str(row[2])
    queries_query = '"'+row[12]+'"'

    result_class = '"'+row[13]+'"'

    url = row[4]
    url = url.replace('"', '')
    url = url.replace(',', '')
    url = '"'+url+'"'

    main = row[5]
    main = main.replace('"', '')
    main = main.replace(',', '')
    main = '"'+main+'"'

    se = '"'+row[6]+'"'

    speed = str(row[8])


    modules = row[9]

    #print(modules)

    modules = modules.replace('"','')
    modules = modules.replace('[','')
    modules = modules.replace(']','')
    modules = modules.replace(', ',',')



    m_split = list(modules.split(","))

    m = []

    for x in m_split:
        x = x.replace("'",'')
        m.append(x)


    results = row[10]

    results = results.replace('"','')
    results = results.replace('[','')
    results = results.replace(']','')
    results = results.replace(', ',',')

    r_split= list(results.split(","))

    r = []

    for x in r_split:
        x = x.replace("'",'')
        r.append(x)


    elements = []


    for i in range(0, len(m)):

        elements.append((m[i], r[i]))

    #test_el = []

    for db_el in db_modules:
        if not db_el in m:
            #test_el.append(hash)
            m_val = db_el
            r_val = '"-100"'
            if "source" not in m_val:
                elements.append((m_val, r_val))
            else:
                m_val = db_el
                r_val = '0'
                elements.append((m_val, r_val))

    #mylist = list(dict.fromkeys(test_el))

    #for ml in mylist:
    #    if ml:
    #        print(ml)

        #print(elements)




    build_res = study+','+results_id+','+hash+','+results_pos+','+query_id+','+queries_query+','+url+','+main+','+se+','+speed+','+result_class+','

    lh_values = []
    lh_results = ''

    for el in elements:

        mod = el[0]
        val = str(el[1])

        lh_values.append((mod, val))


    lh_values= set(tuple(element) for element in lh_values)

    lh_list=[]
    added_keys = set()

    for row in lh_values:
    # We use tuples because they are hashable
        lookup = tuple(row[:1])
        if lookup not in added_keys:
            lh_list.append(row)
            added_keys.add(lookup)

    lh_list.sort(key=lambda x: x[0])

    #print(lh_list)

    #print(lh_list)
    #print("\n")
    #if len(lh_list) > 42:
        #print(len(lh_list))
        #print(len(db_modules))
        #print(url)
        #print(main)

    '''
    for l in lh_list:
        if l[0] not in db_modules:
        print(l[0])

    exit()
    '''

    mods = ''

    for t in lh_list:
        mods = mods+t[0]+','
        #print(mods)


    for l in lh_list:
        lh_results = lh_results + l[1]+','


    build_res = build_res+lh_results

    #print(build_res)
    #print("\n")



    save_res = '\n'+build_res

    with open(csv_file,'a+') as f:
        f.write(save_res)
    f.close()

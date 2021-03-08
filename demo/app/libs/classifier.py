import os
import csv
from urllib.parse import urlsplit

import config

def classify(url):
    sources_categories = ['source ads', 'source company', 'source known', 'source news', 'source not optimized', 'source search engine', 'source shop', 'source top']

    results = {}

    main = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))

    url = url.replace('www.', '')

    for source_category in sources_categories:

        sources_file = os.environ['CLASSES_FOLDER']+source_category+'.csv'
        sources = []
        sources_loc = []
        results.update({source_category: 0})
        with open(sources_file, 'r') as csvfile:
            urls = csv.reader(csvfile)

            for u in urls:
                sources.append(u)

        for s in sources:
            s[0] = s[0].replace('www.', '')

            if s[0] in url or s[0] in main or s[0] == url or s[0] == main:
                results.update({source_category: 1})

    return results

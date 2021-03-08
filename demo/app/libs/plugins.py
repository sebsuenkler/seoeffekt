import os
import csv
import config
from helpers import Helpers

def check_plugins(html_source, html_comments):
    plugin_files = ['ads', 'analytics', 'plugins']
    results = {'ads':'', 'analytics':'', 'plugins':''}

    for p in plugin_files:
        plugins = []
        plugs = ""
        p_file = os.environ['PLUGINS_FOLDER']+p+'.csv'
        with open(p_file, 'r') as csvfile:
            csv_result = csv.reader(csvfile, delimiter=',', quotechar='"')
            check = list(csv_result)

        for c in check:
            obj = c[0]
            pattern = c[1]
            for comment in html_comments:
                if(len(comment) < 3000):
                    if Helpers.matchText(comment, pattern):
                        plugins.append(obj)

        for c in check:
            obj = c[0]
            pattern = c[1]
            for snip in html_source:
                if(len(snip) < 3000):
                    if Helpers.matchText(snip, pattern):
                        plugins.append(obj)


        save_plugins = set(plugins)
        for s in save_plugins:
            plugs = plugs+s+", "

        plugs = plugs[:-2]

        results.update({p: plugs})

    return results

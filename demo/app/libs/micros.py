import os
import csv
from urllib.parse import urlsplit

import config
from helpers import Helpers

def check_micros(html_source, html_comments):

    number_of_micros = 0
    micro_file = os.environ['MICROS_FOLDER']+'micro.csv'

    micros_list = []
    with open(micro_file, 'r') as csvfile:
        micros = csv.reader(csvfile)
        for m in micros:
            modul = m[0]
            pattern = m[1]
            item = (modul, pattern)
            micros_list.append(item)

    micros_save = []

    for ms in micros_list:
        obj = ms[0]
        pattern = ms[1]

        for comment in html_comments:
            if(len(comment) < 3000):
                if Helpers.matchText(comment, pattern):
                    micros_save.append([obj])
        for s in html_source:
            if(len(s) < 3000):
                if Helpers.matchText(s, pattern):
                    micros_save.append([obj])

    number_of_micros = len(micros_save)
    return number_of_micros

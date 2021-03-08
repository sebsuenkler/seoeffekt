#check description
from bs4 import BeautifulSoup
import lxml.html

def check_canonicals(tree):

    xpath = '//a[@rel="canonical"]'
    module = 'check canonical'
    c_counter = 0

    res1 = tree.xpath(xpath)

    for r in res1:
        c_counter = c_counter + 1
        xpath_2 = '//link[@rel="canonical"]'
        res2 = tree.xpath(xpath_2)

        for r in res2:
            c_counter = c_counter + 1

    c_value = c_counter
    return c_value

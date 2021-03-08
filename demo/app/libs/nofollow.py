#check description
from bs4 import BeautifulSoup
import lxml.html

def check_nofollow(tree):
    nofollow = 0
    xpath = '//a[@rel="nofollow"]'
    res1 = tree.xpath(xpath)
    counter = 0

    for r in res1:
        counter = counter + 1

    xpath_2 = '/meta[@name="robots"]/@content'

    res2 = tree.xpath(xpath_2)

    for r in res2:
        if r == 'nofollow':
            counter = counter + 1

    value = counter

    return nofollow

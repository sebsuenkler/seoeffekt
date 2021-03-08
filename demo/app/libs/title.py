from bs4 import BeautifulSoup
import lxml.html

#check title
def check_title(tree):

    title = ""

    xpath_title = "//title/text()"
    xpath_meta_title = "//meta[@name='title']/@content"
    xpath_og_title = "//meta[@property='og:title']/@content"

    check_title = str(tree.xpath(xpath_title))
    check_meta_title = str(tree.xpath(xpath_meta_title))
    check_og_title = str(tree.xpath(xpath_og_title))

    if len(check_title) > 4 or len(check_meta_title) > 4  or len(check_og_title) > 4:
        value = 1
        if len(check_og_title) > 4:
            title = check_og_title
        elif len(check_meta_title) > 4:
            title = check_meta_title
        else:
            title = check_title

        title = title[2:-2]
        
        title = title.replace("'", "")
        title = title.replace('"', "")
        title = title.replace(':', "")
        title = title.replace(',', "")


    return title

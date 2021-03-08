#check description
from bs4 import BeautifulSoup
import lxml.html

def check_description(tree):
    description = ""
    xpath_meta = "//meta[@name='description']/@content"
    xpath_og_property = "//meta[@property='og:description']/@content"
    xpath_og_name = "//meta[@name='og:description']/@content"

    meta_content = str(tree.xpath(xpath_meta))

    og_property_content = str(tree.xpath(xpath_og_property))
    og_name = str(tree.xpath(xpath_og_name))

    if(len(meta_content) > 5 or len(og_property_content) > 5 or len(og_name) > 5):
        if len(og_name) > 5:
            description = og_name
        elif len(og_property_content) > 5:
            description = og_property_content
        else:
            description = meta_content

        description = description[2:-2]
        
        description = description.replace("'", "")
        description = description.replace('"', "")
        description = description.replace(':', "")
        description = description.replace(',', "")

    return description

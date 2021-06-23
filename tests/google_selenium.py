from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from lxml import html


import time


query = 'karl lauterbach'

options = Options()
#options.add_argument('--ignore-certificate-errors-spki-list')
#options.add_argument('--ignore-ssl-errors')
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--allow-insecure-localhost')
#options.add_argument("user-data-dir=selenium")
#options.log.level = 'error'

profile = webdriver.FirefoxProfile()

profile.set_preference("browser.safebrowsing.blockedURIs.enabled", True)
profile.set_preference("browser.safebrowsing.downloads.enabled", True)
profile.set_preference("browser.safebrowsing.enabled", True)
profile.set_preference("browser.safebrowsing.forbiddenURIs.enabled", True)
profile.set_preference("browser.safebrowsing.malware.enabled", True)
profile.set_preference("browser.safebrowsing.phishing.enabled", True)
profile.set_preference("dom.webnotifications.enabled", False);

profile.add_extension(extension='/home/sebastian/alpha/extensions/i_dont_care_about_cookies-3.2.7-an+fx.xpi')

driver = webdriver.Firefox(firefox_profile=profile, options=options)

driver.get('http://www.google.de')


time.sleep(3)

try:
    element = driver.find_element_by_id("zV9nZe")
    element.click()

except:
    pass

time.sleep(3)

search = driver.find_element_by_name('q')
search.send_keys(query)
search.send_keys(Keys.RETURN)

time.sleep(6)

'''
<a aria-label="Page 3" class="fl" href="/search?q=x-men&amp;ei=1yN4YK6_MZ-I9u8PmsmvMA&amp;start=20&amp;sa=N&amp;ved=2ahUKEwjuhq-Hk4DwAhUfhP0HHZrkCwYQ8tMDegQIARBG"><span class="SJajHc NVbCr" style="background:url(/images/nav_logo299.webp) no-repeat;background-position:-74px 0;width:20px"></span>3</a>
'''

xpath_res = "//div[@class='tF2Cxc']/div[@class='yuRUbf']/a/@href"

pages = []

results = []

x = range(2, 101)

for n in x:
    r = str(n)
    page = 'Page '+r
    pages.append(page)


for p in pages:

    xpath = "//a[@aria-label='{}']".format(p)

    try:

        paging = driver.find_element_by_xpath(xpath)

        paging.click()

        time.sleep(3)

        source = driver.page_source

        tree = html.fromstring(source)
        urls = tree.xpath(xpath_res)

        for url in urls:
            results.append(url)

    except:
        pass

if results:
    print(results)
    #driver.quit()

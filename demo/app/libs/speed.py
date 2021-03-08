from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def get_speed(url):
    try:
        if not '.pdf' in url:

            options = Options()
            options.add_argument('--ignore-certificate-errors-spki-list')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-insecure-localhost')
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('-headless')
            options.log.level = 'error'
            options.headless = True

            driver = webdriver.Firefox(options=options)
            driver.set_page_load_timeout(60)
            driver.get(url)

            speed = driver.execute_script(
                        """
                        var loadTime = ((window.performance.timing.domComplete- window.performance.timing.navigationStart)/1000);
                        return loadTime;
                        """
                        )
            driver.quit()

    except:
        speed = -1

    return speed

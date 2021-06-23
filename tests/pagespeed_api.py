''' Loosely based on the example code in http://www.obeythetestinggoat.com/
how-to-get-selenium-to-wait-for-page-load-after-a-click.html
'''
'''
Import the necessary packages required for execution
'''
from selenium import webdriver


''' Firefox web driver interface
'''
hyperlink = "https://www.fuellmich.com/"
driver = webdriver.Firefox()
driver.get(hyperlink)

''' Use Navigation Timing  API to calculate the timings that matter the most '''

navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
responseStart = driver.execute_script("return window.performance.timing.responseStart")
domComplete = driver.execute_script("return window.performance.timing.domComplete")
loadStart = driver.execute_script("return window.performance.timing.domInteractive")
EventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

''' Calculate the performance'''
loadingTime = EventEnd - navigationStart
speed = loadingTime / 1000

''' Calculate the performance'''
backendPerformance_calc = responseStart - navigationStart
frontendPerformance_calc = domComplete - responseStart

print("Back End: %s" % backendPerformance_calc)
print("Front End: %s" % frontendPerformance_calc)
print(speed)

driver.quit()

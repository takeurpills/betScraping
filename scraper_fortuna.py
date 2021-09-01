from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

SCROLL_PAUSE_TIME = 2  # ajax loading takes forever :(
LOAD_PAUSE_TIME = 1

web = "https://www.ifortuna.sk/stavkovanie/futbal?timeTo=today"
path = "D:/chromedriver/chromedriver"

# open chrome and load the website
driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(web)

# add explicit wait just to be sure
time.sleep(LOAD_PAUSE_TIME)

# initialize the storage variables
teams = []
x12 = []  # 3-way score X 1 2

# scroll until no more new matches are loaded
scroll_context_selector = driver.find_element_by_xpath("//body")
max_scroll_count = -1

while True:
    scroll_context_selector.send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)  # wait for it, booom

    scroll_count = driver.find_elements_by_xpath('//section[@class="competition-box"]')

    if max_scroll_count == len(scroll_count):
        break
    else:
        max_scroll_count = len(scroll_count)

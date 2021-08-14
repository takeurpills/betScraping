from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

SCROLL_PAUSE_TIME = 0.1
LOAD_PAUSE_TIME = 1

web = 'https://www.nike.sk/tipovanie/futbal?zajtra'
path = 'D:/chromedriver/chromedriver'

# open chrome and load the website
driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(web)

# add explicit wait just to be sure
time.sleep(LOAD_PAUSE_TIME)

# initialize the storage variables
teams = []
x12 = [] #3-way score X 1 2
odds_events = []

# turn off live odds
filter_button = driver.find_element_by_xpath('//*[@id="left-column"]/div/div/div/div/ul/li[3]')
filter_button.click()
time.sleep(LOAD_PAUSE_TIME)

live_checkbox = driver.find_element_by_xpath('//*[@id="menuOfferFilterExpanded"]/div/ul[1]/li[2]/label/span[2]')
live_checkbox.click()
time.sleep(LOAD_PAUSE_TIME)
# might not need, there is not close button when in maximized windows on 1080p
#filter_close = driver.find_element_by_xpath('//*[@id="left-column"]/div/div/div/div/ul/li[3]/div/button/span')
#filter_close.click()

scroll_context_selector = driver.find_element_by_xpath('//a[@title="Zápas"][@class="active"]')

# find random text on bottom of page
end_of_page = ""
while (len(end_of_page) < 1):
    scroll_context_selector.send_keys(Keys.END)
    end_of_page = driver.find_elements_by_xpath("//*[contains(text(), 'Prejsť na mobilnú verziu')]")
    time.sleep(SCROLL_PAUSE_TIME)
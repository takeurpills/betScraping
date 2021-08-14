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

#select all standard matches, excluding superchance and other special promotions
leagues = driver.find_elements_by_xpath('//*[contains(@data-atid, "n1-league-box")]')

#loop through all leagues, filter for only classic 1X2 matches and extract data match by match
for league in leagues:
    if league.find_element_by_xpath('.//div[@class="content-box-bets-subtitle no-wrap bet"]').text == "ZÁPAS":
        matches_parent = league.find_element_by_xpath('../../..')
        matches = league.find_elements_by_xpath('.//div[@class="flex bet-view-prematch-row"]')

        for match in matches:
            match_info_raw = match.get_attribute("title")
            match_info_list = match_info_raw.replace("\n"," | ").split(" | ")
            teams.append(match_info_list[3])

            match_odds_parents = match.find_elements_by_xpath('.//a[@data-atid="n1-bet-box"]')
            match_odds_list = []
            odds = ""
            for match_odds in match_odds_parents:                
                odds = match_odds.find_element_by_xpath('.//span[@class="text-extra-bold"]').text
                if len(odds) > 1:
                    match_odds_list.append(odds)
                else:
                    match_odds_list.append("1.00")
            
            x12.append(match_odds_list)

print(x12)
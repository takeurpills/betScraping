from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

SCROLL_PAUSE_TIME = 0.1
LOAD_PAUSE_TIME = 1

web = 'https://www.nike.sk/tipovanie/futbal?dnes'
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
filter_button = driver.find_element_by_xpath('//div[contains(@data-atid, "time-filter")]')
filter_button.click()
time.sleep(LOAD_PAUSE_TIME)

live_checkbox = driver.find_element_by_xpath('//span[contains(@class, "content-filter") and contains(text(), "Live")]')
live_checkbox.click()
time.sleep(LOAD_PAUSE_TIME)

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

            match_odds_parents = match.find_elements_by_xpath('.//*[contains(@class, "bet-box-simple")]')
            match_odds_list = []
            odds = ""
            for match_odds in match_odds_parents:                
                odds = match_odds.find_elements_by_xpath('.//span[@class="text-extra-bold"]')
                if len(odds) > 0:
                    match_odds_list.append(odds[0].text)
                else:
                    match_odds_list.append("1.00")
            
            x12.append(match_odds_list)

driver.quit()

#Store lists in dictionary
dict_betting = {"Teams": teams, "1x2": x12}

#Push data in dataframe
df_betting = pd.DataFrame.from_dict(dict_betting)

#PRINT
df_betting.to_csv("nike.csv")
print(df_betting.head(10))
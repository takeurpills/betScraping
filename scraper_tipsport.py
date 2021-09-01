from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

SCROLL_PAUSE_TIME = 0.1
LOAD_PAUSE_TIME = 1

web = "https://www.tipsport.sk/kurzy/futbal-16?timeFilter=form.period.today&limit=999"
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

# select all standard matches, excluding special events and promotions
matches = driver.find_elements_by_xpath('//div[@class="o-matchRow"]')

# loop through all leagues, filter for only classic 1X2 matches and extract data match by match
for match in matches:
    is_five_way_bet = match.find_elements_by_xpath(
        './/div[contains(@class, "countOpp5")]'
    )  # select only 1x2 type matches
    if len(is_five_way_bet) > 0:

        # extract team names
        match_teams_parent = match.find_element_by_xpath(
            './/span[contains(@class, "o-matchRow__matchName")]'
        )
        match_teams = match_teams_parent.find_element_by_xpath("./span").text

        teams.append(match_teams)

        # extract match odds
        match_odds_parent = match.find_element_by_xpath(
            './/div[contains(@class, "countOpp5")]'
        )
        match_odds = match_odds_parent.find_elements_by_xpath(
            './/div[contains(@class, "btnRate")]'
        )
        match_odds_list = []

        for odds in match_odds:
            if len(odds.text) > 1:
                match_odds_list.append(odds.text)
            else:
                match_odds_list.append("1.00")

        x12.append(match_odds_list)

driver.quit()

# Store lists in dictionary
dict_betting = {"Teams": teams, "1x2": x12}

# Push data in dataframe
df_betting = pd.DataFrame.from_dict(dict_betting)

# PRINT
# df_betting.to_csv("tipsport.csv")
print(df_betting.head(10))

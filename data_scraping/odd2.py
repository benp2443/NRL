import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
pd.set_option("display.max_rows", 160)

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)

dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")


driver = webdriver.PhantomJS(
        executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe',
        desired_capabilities=dcap)

url = 'http://www.oddsportal.com/rugby%2Dleague/australia/nrl%2D2010/results/#/page/3/'

def scrap_page_data(url):
    driver.get(url)
    
    #print(driver.execute_script('return navigator.userAgent'))
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #print(driver.current_url)
    
    date = ''
    
    data = []
    table = soup.find('table', {'id': 'tournamentTable'})
    for row in table.find_all('tr', {'class':['odd deactivate', 'deactivate', 'center nob-border']}):
    
        if row.attrs['class'] == ['center', 'nob-border']:
            date  = row.find('span').text
            continue
        
        else: 
            teams = row.find('td', class_ = 'name table-participant').find('a').text
            split_teams = teams.split(' - ')
            home = split_teams[0]
            away = split_teams[1]
            
            score = row.find('td', class_ = 'center bold table-odds table-score').text
            score_split = score.split(':')
            home_pts = score_split[0]
            if 'OT' in score_split[1]:
                away_pts = score_split[1][0:2]
                overtime = True
            else:
                away_pts = score_split[1]
                overtime = False
        
            odds = row.find_all('td', {'class': 'result-ok odds-nowrp', 'class': 'odds-nowrp'})
            home_odds = odds[0].find('a').text
            away_odds = odds[2].find('a').text    
        print('Home: {}; Away: {}'.format(home, away))        
        data.append([date,home,home_pts,away,away_pts,home_odds,away_odds,overtime])
    
    df = pd.DataFrame(data, columns = ['date','home','home_pts','away','away_pts','home_odds','away_odds', 'overtime'])
        
    return df

df = scrap_page_data(url)

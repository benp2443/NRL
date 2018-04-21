import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
pd.set_option("display.max_rows", 160)

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

url = 'www.oddsportal.com/rugby-league/australia/nrl-2017/results/'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'xml')

table = soup.find('table', class_ = ' table-main')
print(table.prettify())

#for row in table.find_all('tr', {'class':'center nob-border', 'class':'odd deactivate'}):
#        date = row.find('span').text
#        if date != None:
#                print(date)





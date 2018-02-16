import numpy as np
import pandas as pd
import sys 
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

def season_scraper(year):

	year_ = [year]
	url = 'https://www.rugbyleagueproject.org/seasons/nrl-{}/results.html'.format(year)

	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'lxml')

	table = soup.find('table', class_ = 'list')

	year_info = []

	for row in table.find_all('tr'):
		
		row_info = []

		if row.find('th') is not None:
			round_split = row.find('th').text.split('\n')
			round_ = [round_split[1]]
			continue
		elif row.find('td', class_ = "clear noprint"):
			continue

		for column in row.find_all('td'):
			row_info.append(column.text)
		year_info.append(year_ + round_ + row_info)

	return year_info


for year in np.arange(2008, 2018):
	
	year_info = season_scraper(year)

	df = pd.DataFrame(year_info, columns = ['Year', 'Round', 'Day', 'Date', 'Time', 'Home', 'H_PTS', 'Away', 'A_PTS', 'Referee/s', 'Stadium', 'Crowd', 'delete'])

	if year == 2008:
		nrl_df = df
	else:
		nrl_df = pd.concat([nrl_df, df])
		

nrl_df.to_csv('NRL.csv', index = False)

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')


def SOO_scraper(year):
	"""Loads the webpage for the given year. Locates the date data and returns it in a list"""

	url = 'https://www.rugbyleagueproject.org/competitions/state-of-origin-{}/summary.html'.format(year) 
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'lxml')

	table = soup.find('table', class_ = 'list')


	rows = table.find_all('tr')
	desired_rows = []
	for row in rows:
		if row.find('td', class_ = 'clear noprint'):
			continue
		if row.find('td', class_ = 'noprint'):
			desired_rows.append(row)

	dates = []

	for row in desired_rows:
		data = row.find_all('td')
		year = data[0].text
		month_day = data[1].text
		date = year + " " + month_day
		print(date)
		dates.append(date)

	print(dates)

	return dates

# Use SOO_scraper to scrape data for last 10 years then save to csv

soo_dates = []
for year in np.arange(2008,2018):
	dates = SOO_scraper(year)
	soo_dates += dates

print(soo_dates)

df = pd.DataFrame(soo_dates, columns = ['date'])
df.to_csv('SOO_dates.csv', index = False)

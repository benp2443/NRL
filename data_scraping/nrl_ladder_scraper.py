import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
pd.set_option("display.max_rows", 160)

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

def ladder_scraper(year):

	url = 'https://en.wikipedia.org/wiki/{}_NRL_season'.format(year)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'lxml')

	table = soup.find('table', {'class': 'wikitable', 'style': 'text-align:center;'})

	ladder = []

	for row in table.find_all('tr'):

		if row.find('th') != None:
			continue

		row_info = [year]
		i = 0

		for data in row.find_all('td'):

			if i == 9:
				i += 1
				continue
			else:
				row_info.append(data.text)

			i += 1

		ladder.append(row_info)
		df = pd.DataFrame(ladder, columns = ['Year', 'Rank', 'Team', 'Pld', 'W', 'D', 'L', 'B', 'PF', 'PA', 'Pts'])


	return df

df = pd.DataFrame()

for year in np.arange(2008, 2018):
	
	ladder = ladder_scraper(year)

	if year == 2008:
		df = ladder
	
	else:
		df = pd.concat([df, ladder], axis = 0)

df.reset_index(drop = True, inplace = True)


# Cleaning

# Replace '-' with '0' for years where the draw columns uses '-' instead of '0'

df.loc[df['D'] == '-', 'D'] = 0

# remove leading whitespace and training (P) from team names column

df['Team'] = df['Team'].map(lambda x: x.lstrip().rstrip('(P)'))

# remove leading 0 from storm points column in 2010 for when they were stipped off 8 premiership points and unable to compete for points
# for the remainder of the season

df.loc[df['Pts'] == '01', 'Pts'] = '1'

# Remove '*' for bulldogs Points column in 2009 highlighting that they were deducded two points for a interchange breach

df.loc[df['Pts'] == '38*', 'Pts'] = '38'

# Convert strings columns to ints where appropriate

convert_cols = ['Rank', 'Pld', 'W', 'D', 'L', 'B', 'PF', 'PA', 'Pts']

for column in convert_cols:
	df[column] = df[column].astype(float)

# Create Points Differential column

df['PD'] = df['PF'] - df['PA']

# Remove whitespace from start of team names

df['Team'] = df['Team'].str.strip()

print(df['Team'].unique())
print(df.info())

df.to_csv('nrl_ladder.csv', index = False)

## merge this script with cleaning script once complete

import pandas as pd
import numpy as np
import sys
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 50)

df = pd.read_csv('../data/NRL_cleaned.csv')

df['date_time'] = pd.to_datetime(df['date_time'], format = "%Y-%m-%d %H:%M:%S")
df['Date'] = df['Year'].astype(str) + '-' + df['Date']
df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%b-%d") 

print(df.head())

# Create dictionary 

teams = df['Home'].unique().tolist()

team_win_percentage = {}
for team in teams:
	team_win_percentage[team] = {'G': 0, 'W': 0}

win_percentage = team_win_percentage.copy()

# Create rest columns

df['Home_w%'] = 0
df['Away_w%'] = 0

# Create list of opening day idx's

opening_idx = df['Year'].drop_duplicates(keep = 'first').index.values.tolist()
opening_idx = opening_idx[1:] # drop the first idx (0)

# Get index value of certain columns for fast and easy access

home = df.columns.values.tolist().index('Home')
away = df.columns.values.tolist().index('Away')
hw = df.columns.values.tolist().index('HomeWin')
h_w% = df.columns.values.tolist().index('Home_w%')
a_w% = df.columns.values.tolist().index('Away_w%')

i = 0
while i < len(df):

	if i in opening_idx:
		win_percentage = team_win_percentage.copy()	

	h = df.iat[i, home]
	a = df.iat[i, away]
	winner = df.iat[i, hw]
	
	if win_percentage[h]['G'] > 0:
		df.iat[i, h_w%] = win_percentage[h]['W']/win_percentage[h]['G']
	else:
		df.iat[i, h_w%] = 0.5 # set 0.5 is win percentage when team has not played a game in current season

	if win_percentage[a]['G'] > 0:
		df.iat[i, a_w%] = win_percentage[a]['W']/win_percentage[a]['G']
	else:
		df.iat[i, a+w%] = 0.5

	if winner == True:
	



























premiers = ['Manly Warringah', 'Melbourne', 'St George Illawarra', 'Manly Warringah', 'Melbourne', \
	'Sydney', 'South Sydney', 'North Queensland', 'Cronulla'] # excluded 2017 team (Melbourne) as no 2018 data

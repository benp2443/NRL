## merge this script with cleaning script once complete

import pandas as pd
import numpy as np
import sys
import copy
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 50)

df = pd.read_csv('../data/NRL_cleaned.csv')

df['date_time'] = pd.to_datetime(df['date_time'], format = "%Y-%m-%d %H:%M:%S")
df['Date'] = df['Year'].astype(str) + '-' + df['Date']
df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%b-%d") 

# Create dictionary 

teams = df['Home'].unique().tolist()

team_win_percentage = {}
for team in teams:
	team_win_percentage[team] = {'G': 0, 'W': 0}

win_percentage = copy.deepcopy(team_win_percentage)

# Create win percentage columns

df['Home_w_percent'] = -1
df['Away_w_percent'] = -1

# Create list of opening day idx's

opening_idx = df['Year'].drop_duplicates(keep = 'first').index.values.tolist()
opening_idx = opening_idx[1:] # drop the first idx (0)

# Get index value of certain columns for fast and easy access

home = df.columns.values.tolist().index('Home')
away = df.columns.values.tolist().index('Away')
hw = df.columns.values.tolist().index('HomeWin')
h_w_percent = df.columns.values.tolist().index('Home_w_percent')
a_w_percent = df.columns.values.tolist().index('Away_w_percent')

# Loop through df changing Home/Away win percentage columns

i = 0
while i < len(df):
	# reset dictionary if it is the start of a new season
	if i in opening_idx:
		print('Hello')
		win_percentage = copy.deepcopy(team_win_percentage)	

	h = df.iat[i, home]
	a = df.iat[i, away]
	winner = df.iat[i, hw]
	
	# Set win percentage for home and away columns. If team has not played a game in current season, set value to 0.5
	if win_percentage[h]['G'] > 0:
		df.iloc[i, h_w_percent] = win_percentage[h]['W']/win_percentage[h]['G']
	else:
		df.iloc[i, h_w_percent] = 0.5

	if win_percentage[a]['G'] > 0:
		df.iloc[i, a_w_percent] = win_percentage[a]['W']/win_percentage[a]['G']
	else:
		df.iloc[i, a_w_percent] = 0.5

	# Update win values in win_percentage dictionary for home and away teams
	if winner == 1:
		win_percentage[h]['W'] += 1
		print('Home win')
	if winner == 0.5:
		win_percentage[h]['W'] += 0.5
		win_percentage[a]['W'] += 0.5
	if winner == 0:
		win_percentage[a]['W'] += 1
		print('Away win')

	# Update games played value in win_percentage dictionary for both teams
	win_percentage[h]['G'] += 1
	win_percentage[a]['G'] += 1
	
	i += 1

# 

premiers = ['Manly Warringah', 'Melbourne', 'St George Illawarra', 'Manly Warringah', 'Melbourne', \
	'Sydney', 'South Sydney', 'North Queensland', 'Cronulla'] # excluded 2017 team (Melbourne) as no 2018 data

# Import libraries, gameBygame.csv and drop empty column

import pandas as pd
import numpy as np
from datetime import datetime
import copy
pd.set_option("display.max_rows", 150)

df = pd.read_csv('../data/gameBygame.csv')

df.drop(['delete'], axis = 1, inplace = True)

# Covert Crowd to integer and create a datetime variable

df['Crowd'] = df['Crowd'].str.replace(',','').astype(int)

df['Date'] = df['Date'].str.replace('th', '').str.replace('st', '').str.replace('nd', '').str.replace('rd', '').str.replace(' ', '-')
df['date_time'] = df['Year'].astype(str) + '-' + df['Date'] + ' ' + df['Time']
df['date_time'] = pd.to_datetime(df['date_time'], format = "%Y-%b-%d %I:%M%p")

# Clean up the stadiums due to home teams changing stadium names

stadiums = df['Stadium'].unique().tolist()

#for stadium in stadiums:
#	print(stadium, '\n')
#
#	temp = df.loc[df['Stadium'] == stadium, ['Home', 'Away', 'Stadium']]
#	
#	if len(temp) > 10:
#		print("Permanent")
#		print(temp.iloc[0:1, :])
#	else:
#		print(temp)
#	
#	print("")


############ Home Win ############

# 1 for a home team win. 0 for home team lose. 0.5 for draw

def winner(row):
	if row['H_PTS'] > row['A_PTS']:
		return 1
	elif row['H_PTS'] == row['A_PTS']:
		return 0.5
	else:
		return 0

df['HomeWin'] = df.apply(winner, axis = 1)

############# State of Origin Period ############

# load SOO_dates data

soo = pd.read_csv('../data/soo_dates.csv')

# Clean data

soo['date'] = soo['date'].str.replace('th', '').str.replace('st', '').str.replace('nd', '').str.replace('rd', '').str.replace(' ', '-')
soo['date'] = pd.to_datetime(soo['date'], format = "%Y-%b-%d")

# Add SOO period column which is true when the regular season game occurs during the origin period
# period extends from one round prior to game 1 and 1 round post game 3

years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]


df['SOO'] = False # initialise column to False. Will update for True periods.

df_date = df.columns.values.tolist().index('date_time')
SOO = df.columns.values.tolist().index('SOO')

for year_ in years:
	idx_list = df.loc[df['date_time'].dt.year == year_, :].index.values.tolist()
	date_interval = soo.loc[soo['date'].dt.year == year_, :]

	start_soo_period = date_interval.iat[0, 0] - pd.DateOffset(days = 7)
	end_soo_period = date_interval.iat[2, 0] + pd.DateOffset(days = 7)

	i = idx_list[0]

	while i <= idx_list[-1]:

		row_date = df.iat[i, df_date]

		if ((start_soo_period - row_date).days < 0) and ((end_soo_period - row_date).days > 0):
			df.iat[i, SOO] = True

		i += 1

############# Win Percentage Columns #############

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
	if winner == 0.5:
		win_percentage[h]['W'] += 0.5
		win_percentage[a]['W'] += 0.5
	if winner == 0:
		win_percentage[a]['W'] += 1

	# Update games played value in win_percentage dictionary for both teams
	win_percentage[h]['G'] += 1
	win_percentage[a]['G'] += 1
	
	i += 1


# Save dataframe to csv

df.to_csv('../data/NRL_cleaned.csv', index = False)

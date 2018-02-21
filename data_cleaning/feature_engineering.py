import pandas as pd
import numpy as np 
from datetime import datetime
import copy
pd.set_option("display.max_rows", 150)


df = pd.read_csv('../data/gameBygame_cleaned.csv')

df['date_time'] = pd.to_datetime(df['date_time'], format = "%Y-%m-%d %H:%M:%S")

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


# Season will be split on pre origin (start), origin (middle) and post origin (end)

# Create period column and store idx values for each period in lists

df['Period'] = df['SOO']

start_origin = []
end_origin = []
new_season = []
start_finals = []

# Loop through each year finding idx of rows which divide the season between pre, origin, end and finals and store in lists

for year in years:

	temp = df.loc[df['Year'] == year, :]

	# Get idx values

	unique_idx = temp['SOO'].drop_duplicates(keep = 'first').index.values.tolist() # returns idx of first game of year and first game during origin period in a list
	new_season_idx = [unique_idx[0]]
	start_origin_idx = [unique_idx[1]]
	end_origin_idx = [temp['SOO'].drop_duplicates(keep = 'last').index.values.tolist()[0]] 
	qualif_final_idx = [temp.loc[temp['Round'] == 'Qualif Final', :].index.values.tolist()[0]]

	# Add idx values to respective lists for current year

	start_origin += start_origin_idx
	end_origin += end_origin_idx
	new_season += new_season_idx
	start_finals += qualif_final_idx

# Use the idx values found above to update the 'Period' column

i = 0
while i < len(new_season):

	df.loc[new_season[i]: start_origin[i] - 1, 'Period'] = 'Pre'

	if i < len(new_season) - 1:

		df.loc[end_origin[i] + 1: new_season[i + 1], 'Period'] = 'Post'
		df.loc[start_finals[i]: new_season[i + 1], 'Period'] = 'Finals'
	else:
			
		df.loc[end_origin[i] + 1:, 'Period'] = 'Post'
		df.loc[start_finals[i]:, 'Period'] = 'Finals'

	i += 1

df.loc[df['Period'] == True, 'Period'] = 'Origin'

# Save dataframe to csv

df.to_csv('../data/NRL.csv', index = False)

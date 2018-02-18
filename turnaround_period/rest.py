import pandas as pd
import numpy as np
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 50)

df = pd.read_csv('../data/NRL_cleaned.csv')

df['date_time'] = pd.to_datetime(df['date_time'], format = "%Y-%m-%d %H:%M:%S")
df['Date'] = df['Year'].astype(str) + '-' + df['Date']
df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%b-%d") 
print(df.head())

# Create dictionary 

teams = df['Home'].unique().tolist()

team_last_game = {}
for team in teams:
	team_last_game[team] = ''

last_game = team_last_game.copy()

# Create rest columns

df['Home_rest'] = 0
df['Away_rest'] = 0

# Create list of opening day idx's

opening_idx = df['Year'].drop_duplicates(keep = 'first').index.values.tolist()
opening_idx = opening_idx[1:] # drop the first idx (0)

# Loop through df and add days rest for each team

ht = df.columns.values.tolist().index('Home')
hr = df.columns.values.tolist().index('Home_rest')
at = df.columns.values.tolist().index('Away')
ar = df.columns.values.tolist().index('Away_rest')
Date = df.columns.values.tolist().index('Date')

i = 0
while i < len(df): 

	if i in opening_idx:
		last_game = team_last_game.copy()

	home_team = df.iat[i, ht]
	away_team = df.iat[i, at]
	date = df.iat[i, Date]
	home_last_date = last_game[home_team]
	away_last_date = last_game[away_team]

	if home_last_date != '':
		df.iat[i, hr] = (date - home_last_date).days
	else:
		df.iat[i, hr] = -1 #first game of season place holder

	
	if away_last_date != '':
		df.iat[i, ar] = (date - away_last_date).days
	else:
		df.iat[i, ar] = -1

	last_game[home_team] = date
	last_game[away_team] = date

	i += 1


print(df.Home_rest.unique())
print(df.Away_rest.unique())

df.to_csv('../data/rest_temp.csv', index = False)

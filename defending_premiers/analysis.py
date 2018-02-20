import numpy as np
import pandas as pd
import sys

df = pd.read_csv('../data/NRL_cleaned.csv')

# Create list of premiers and corresponding years

gf_games = df.loc[(df['Round'] == 'Grand Final'), ['Home', 'Away', 'HomeWin']].reset_index(drop = True)

premiers = []

i = 0
while i < len(gf_games):

	if gf_games.loc[i, 'HomeWin'] == 1:
		premiers.append(gf_games.loc[i, 'Home'])
	else:
		premiers.append(gf_games.loc[i, 'Away'])

	i += 1

premiers = premiers[0:-1] # 2017 premiers (Melbourne) dropped as analysis requires following years results

years = df['Year'].unique().tolist()

# Reduce dataset to only include the last round of the regular season (Round 26) and the first round of the finals (Qualif Final)
# Round 26 is included as defending premiers may not make the finals the following year and hence w/l percent will be taken from final round

temp = df.loc[(df['Round'] == 'Qualif Final') | (df['Round'] == 'Round 26'), :]

# win loss percentages will be appended to the following lists for the premiers
win_loss_premiers = []
win_loss_defending_premiers = []

i = 0
while i < len(premiers):
	
	champs = premiers[i]
	prem_year = temp.loc[(temp['Year'] == years[i]) & (temp['Round'] == 'Qualif Final'), :]
	defending_year = temp.loc[temp['Year'] == years[i+1], :]

	h = df.columns.values.tolist().index('Home')
	a = df.columns.values.tolist().index('Away')
	h_w_percent = df.columns.values.tolist().index('Home_w_percent')
	a_w_percent = df.columns.values.tolist().index('Away_w_percent')
	
	# Find win percentage for the premiers in the year they win the premiership. Win percentage is taken 
	# in the first round of the finals as that is there win percentage through the regular season (26 rounds).

	j = 0
	while j < len(prem_year):
		
		if prem_year.iat[j, h] == champs:
			win_loss_premiers.append(prem_year.iat[j, h_w_percent])
			break
		elif prem_year.iloc[j, a] == champs:
			win_loss_premiers.append(prem_year.iat[j, a_w_percent])
			break

		j += 1

	# Check if defending premiers made Qualif final. If yes, append win/loss record to win_loss_defending_premiers

	temp2 = defending_year.loc[defending_year['Round'] == 'Qualif Final', :]

	made_semis = False
	j = 0

	while j < len(temp2):
		
		if temp2.iat[j, h] == champs:
			win_loss_defending_premiers.append(temp2.iat[j, h_w_percent])
			made_semis = True
			break
		elif temp2.iat[j, a] == champs:
			win_loss_defending_premiers.append(temp2.iat[j, a_w_percent])
			made_semis = True
			break
					
		j += 1

	# If the defending premiers did not make the semis, find win/lose record at the final round
	# Need to figure out how to update w/l depending on final game result -> Find how many bye games each team has in a season and can deduce from there

	if made_semis == False:

		j = 0

		while j < len(defending_year):
			
			if defending_year.iat[j, h] == champs:
				win_loss_defending_premiers.append(defending_year.iat[j, h_w_percent])
				break
			elif defending_year.iat[j, a] == champs:
				win_loss_defending_premiers.append(defending_year.iat[j, a_w_percent])
				break

			j += 1
	
	i += 1			
	
years_list = years[0:-1]

results_df = pd.DataFrame(np.array([years_list, premiers, win_loss_premiers, win_loss_defending_premiers]).T, columns = ['Year', 'Premiers', 'w_%_prem', 'w_%_def_prem'])

results_df['w_%_prem'] = results_df['w_%_prem'].astype(float)
results_df['w_%_def_prem'] = results_df['w_%_def_prem'].astype(float)
results_df['Change'] = round((results_df['w_%_prem'] - results_df['w_%_def_prem'])*100,2)


########## Analysis of start, middle and end of regular season ##########

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

periods_list = ['Pre', 'Origin', 'Post']

def win_percentage(df, period, team, wins = 0, games = 0):
	
	temp = df.loc[df['Period'] == period, :].reset_index(drop = True)

	j = 0
	while j < len(temp):

		if temp.loc[j, 'Home'] == team:

			games += 1

			if temp.loc[j, 'HomeWin'] == 1:
				wins += 1
			elif temp.loc[j, 'HomeWin'] == 0.5:
				wins += 0.5
		else:
			games += 1

			if temp.loc[j, 'HomeWin'] == 0:
				wins += 1
			elif temp.loc[j, 'HomeWin'] == 0.5:
				wins += 0.5

		j += 1

	return wins, games

results_df['prem_w_pre_%'] = -1
results_df['prem_w_origin_%'] = -1
results_df['prem_w_post_%'] = -1
results_df['def_w_pre_%'] = -1
results_df['def_w_origin_%'] = -1
results_df['def_w_post_%'] = -1

results_df['Year'] = results_df['Year'].astype(int)

i = 0

while i < len(premiers):
	champs = premiers[i]
	prem_year = years[i]
	def_year = years[i + 1]

	prem_df = df.loc[((df['Home'] == champs) | (df['Away'] == champs)) & (df['Year'] == prem_year), ['Home', 'Away', 'HomeWin', 'Period']]
	def_df = df.loc[((df['Home'] == champs) | (df['Away'] == champs)) & (df['Year'] == def_year), ['Home', 'Away', 'HomeWin', 'Period']]

	prem_results = []
	prem_games = []
	def_results = []
	def_games = []

	for period in periods_list:
		p_wins, p_games = win_percentage(prem_df, period, champs)
		d_wins, d_games = win_percentage(def_df, period, champs)
		
		if period == 'Pre':

			results_df.loc[results_df['Year'] == prem_year, 'prem_w_pre_%'] = round(p_wins/p_games,2)
			results_df.loc[results_df['Year'] == prem_year, 'def_w_pre_%'] = round(d_wins/d_games,2)

		elif period == 'Origin':

			results_df.loc[results_df['Year'] == prem_year, 'prem_w_origin_%'] = round(p_wins/p_games,2)
			results_df.loc[results_df['Year'] == prem_year, 'def_w_origin_%'] = round(d_wins/d_games,2)

		else:

			results_df.loc[results_df['Year'] == prem_year, 'prem_w_post_%'] = round(p_wins/p_games,2)
			results_df.loc[results_df['Year'] == prem_year, 'def_w_post_%'] = round(d_wins/d_games,2)
			
	i += 1
	
########## For and Against ##########

results_df['prem_for'] = -1
results_df['prem_against'] = -1
results_df['def_for'] = -1
results_df['def_against'] = -1

def for_against_count(df, team):
	
	for_ = 0
	against = 0

	h = df.columns.values.tolist().index('Home')
	a = df.columns.values.tolist().index('Away')
	h_pts = df.columns.values.tolist().index('H_PTS')
	a_pts = df.columns.values.tolist().index('A_PTS')

	j = 0

	while j < len(df):

		if df.iat[j, h] == team:
		
			for_ += df.iat[j, h_pts]
			against += df.iat[j, a_pts]

		else:

			for_ += df.iat[j, a_pts]
			against += df.iat[j, h_pts]

		j += 1
	
	return for_, against

i = 0

while i < len(premiers):

	champs = premiers[i]
	prem_year = years[i]
	def_year = years[i + 1]

	prem_df = df.loc[((df['Home'] == champs) | (df['Away'] == champs)) & (df['Year'] == prem_year) & (df['Period'] != 'Finals'), ['Home', 'Away', 'H_PTS', 'A_PTS', 'HomeWin', 'Period']]
	def_df = df.loc[((df['Home'] == champs) | (df['Away'] == champs)) & (df['Year'] == def_year) & (df['Period'] != 'Finals'), ['Home', 'Away', 'H_PTS', 'A_PTS', 'HomeWin', 'Period']]

	prem_for, prem_against = for_against_count(prem_df, champs)
	def_for, def_against = for_against_count(def_df, champs)
	
	results_df.loc[results_df['Year'] == prem_year, 'prem_for'] = prem_for
	results_df.loc[results_df['Year'] == prem_year, 'prem_against'] = prem_against
	results_df.loc[results_df['Year'] == prem_year, 'def_for'] = def_for
	results_df.loc[results_df['Year'] == prem_year, 'def_against'] = def_against

	i += 1

print(results_df)

results_df.to_csv('win_percentage.csv', index = False)	

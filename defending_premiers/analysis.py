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




aa
df.to_csv('win_percentage.csv', index = False)	

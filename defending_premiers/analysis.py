import numpy as np
import pandas as pd
import sys

df = pd.read_csv('../data/NRL.csv')

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

# Create list of years

years = df['Year'].unique().tolist()

########## Analysis of Premiers win/lose percentage in premiership year vs defending year ##########

# import ladders csv which contains regular season standings for each year

ladder_df = pd.read_csv('../data/nrl_ladder.csv')

# Calculate win/lose percentage for premiers during prem year and defending year

prem_wins = []
def_wins = []

prem_wl = []
def_prem_wl = []

i = 0

while i < len(premiers): 
	
	champs = premiers[i]
	prem_year = years[i]
	def_year = years[i+1]
	
	prem_results = ladder_df.loc[(ladder_df['Year'] == prem_year) & (ladder_df['Team'] == champs), :].reset_index()
	def_results = ladder_df.loc[(ladder_df['Year'] == def_year) & (ladder_df['Team'] == champs), :].reset_index()

	prem_win = prem_results.loc[0,'W'] 
	prem_wins.append(prem_win)
	prem_games = prem_results.loc[0,'Pld']

	def_win = def_results.loc[0,'W']
	def_wins.append(def_win)
	def_games = def_results.loc[0,'Pld']

	win_percent_prem = ((prem_win/prem_games)*100).round(0)
	win_percent_def = ((def_win/def_games)*100).round(0)

	prem_wl.append(win_percent_prem)
	def_prem_wl.append(win_percent_def)

	i += 1

data = [premiers, years[:-1], prem_wl, def_prem_wl, prem_wins, def_wins]
prems_df = pd.DataFrame(data, ['Premiers', 'Year', 'Prem_W/L', 'Def_W/L', 'Prem_Wins', 'Def_Wins']).T

prems_df['year_prem'] = prems_df['Year'].astype(str) + '-' + prems_df['Premiers']
prems_df.drop(['Year', 'Premiers'], axis = 1, inplace = True)

prems_df['wins_change'] = prems_df['Prem_Wins'] - prems_df['Def_Wins']
prems_df['wins_percent_change'] = prems_df['Prem_W/L'] - prems_df['Def_W/L']
prems_df.to_csv('prems_df.csv', index = False)

prems_df2 = prems_df[['year_prem', 'Prem_W/L', 'Def_W/L']]
prems_df2 = pd.melt(prems_df2, id_vars = ['year_prem'])
prems_df2.columns = ['Year_Premier', 'Prem/Def', 'Win_Percent']

prems_df2['Prem/Def'] = prems_df2['Prem/Def'].apply(lambda x:'Premiers' if x == 'Prem_W/L' else 'Defending')

prems_df2.to_csv('prem_wl.csv', index = False)

########## Analysis of start, middle and end of regular season ##########

periods_list = ['Pre', 'Origin', 'Post']

def win_percentage(df, period, team):
	
	wins = 0
	games = 0

	temp = df.loc[df['Period'] == period, :].reset_index(drop = True)

	j = 0
	while j < len(temp):

		games += 1

		if temp.loc[j, 'Home'] == team:

			if temp.loc[j, 'HomeWin'] == 1:
				wins += 1
			elif temp.loc[j, 'HomeWin'] == 0.5:
				wins += 0.5
		else:

			if temp.loc[j, 'HomeWin'] == 0:
				wins += 1
			elif temp.loc[j, 'HomeWin'] == 0.5:
				wins += 0.5

		j += 1

	return wins, games

prems_df['prem_w_pre_%'] = -1
prems_df['prem_w_origin_%'] = -1
prems_df['prem_w_post_%'] = -1
prems_df['def_w_pre_%'] = -1
prems_df['def_w_origin_%'] = -1
prems_df['def_w_post_%'] = -1

prems_df['Year'] = years[:-1]

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

			prems_df.loc[prems_df['Year'] == prem_year, 'prem_w_pre_%'] = round(p_wins/p_games,2)
			prems_df.loc[prems_df['Year'] == prem_year, 'def_w_pre_%'] = round(d_wins/d_games,2)

		elif period == 'Origin':

			prems_df.loc[prems_df['Year'] == prem_year, 'prem_w_origin_%'] = round(p_wins/p_games,2)
			prems_df.loc[prems_df['Year'] == prem_year, 'def_w_origin_%'] = round(d_wins/d_games,2)

		else:

			prems_df.loc[prems_df['Year'] == prem_year, 'prem_w_post_%'] = round(p_wins/p_games,2)
			prems_df.loc[prems_df['Year'] == prem_year, 'def_w_post_%'] = round(d_wins/d_games,2)
			
	i += 1
	
########## For and Against ##########

prems_df['prem_for'] = -1
prems_df['prem_against'] = -1
prems_df['prem_for_pre'] = -1
prems_df['prem_againsts_pre'] = -1
prems_df['prem_for_origin'] = -1
prems_df['prem_againsts_origin'] = -1
prems_df['prem_for_post'] = -1
prems_df['prem_againsts_post'] = -1

prems_df['def_for'] = -1
prems_df['def_against'] = -1
prems_df['def_for_pre'] = -1
prems_df['def_againsts_pre'] = -1
prems_df['def_for_origin'] = -1
prems_df['def_against_origin'] = -1
prems_df['def_for_post'] = -1
prems_df['def_againsts_post'] = -1

def for_against_count(df, team):
	
	for_ = 0
	against = 0

	for_pre = 0
	against_pre = 0

	for_origin = 0
	against_origin = 0

	for_post = 0
	against_post = 0

	h = df.columns.values.tolist().index('Home')
	a = df.columns.values.tolist().index('Away')
	h_pts = df.columns.values.tolist().index('H_PTS')
	a_pts = df.columns.values.tolist().index('A_PTS')
	p = df.columns.values.tolist().index('Period')

	j = 0

	while j < len(df):
		
		home_points = df.iat[j, h_pts]
		away_points = df.iat[j, a_pts]
		period = df.iat[j, p]

		if df.iat[j, h] == team:
		
			for_ += home_points
			against += away_points

			if period == 'Pre':
				for_pre += home_points
				against_pre += away_points
			elif period == 'Origin':
				for_origin += home_points
				against_origin += away_points
			else:
				for_post += home_points
				against_post += away_points

		else:

			for_ += away_points
			against += home_points

			if period == 'Pre':
				for_pre += away_points
				against_pre += home_points
			elif period == 'Origin':
				for_origin += away_points
				against_origin += home_points
			else:
				for_post += away_points
				against_post += home_points

		j += 1
	
	results = [for_, against, for_pre, against_pre, for_origin, against_origin, for_post, against_post]

	return results


def append_results(df, year, variable, value):
	df.loc[df['Year'] == year, variable] = value


idx = prems_df.columns.values.tolist().index('prem_for')
variables = prems_df.columns.values.tolist()[idx:]

i = 0

while i < len(premiers):

	champs = premiers[i]
	prem_year = years[i]
	def_year = years[i + 1]

	prem_df = df.loc[((df['Home'] == champs) | (df['Away'] == champs)) & (df['Year'] == prem_year) & (df['Period'] != 'Finals'), ['Home', 'Away', 'H_PTS', 'A_PTS', 'HomeWin', 'Period']]
	def_df = df.loc[((df['Home'] == champs) | (df['Away'] == champs)) & (df['Year'] == def_year) & (df['Period'] != 'Finals'), ['Home', 'Away', 'H_PTS', 'A_PTS', 'HomeWin', 'Period']]

	prem_results = for_against_count(prem_df, champs)
	def_results = for_against_count(def_df, champs)

	results = prem_results + def_results

	j = 0

	while j < len(results):

		append_results(prems_df, prem_year, variables[j], results[j])
		
		j += 1

	i += 1

print(prems_df.columns.values)

def win_percent(df, prem_col_name, def_col_name, save_name):
	temp = df.loc[:, ['year_prem', prem_col_name, def_col_name]]
	temp = pd.melt(temp, id_vars = ['year_prem'])
	temp.to_csv(save_name, index = False)

win_percent(prems_df, 'prem_w_pre_%', 'def_w_pre_%', 'pre_win_percent.csv')
win_percent(prems_df, 'prem_w_origin_%', 'def_w_origin_%', 'origin_win_percent.csv')
win_percent(prems_df, 'prem_w_post_%', 'def_w_post_%', 'post_win_percent.csv')

prems_df['pre_change'] = prems_df['prem_w_pre_%'] - prems_df['def_w_pre_%']
prems_df['origin_change'] = prems_df['prem_w_origin_%'] - prems_df['def_w_origin_%']
prems_df['post_change'] = prems_df['prem_w_post_%'] - prems_df['def_w_post_%']

results = [prems_df['pre_change'].mean(), prems_df['origin_change'].mean(), prems_df['post_change'].mean()]
rows = ['Pre', 'Origin', 'Post']

df2 = pd.DataFrame([rows, results]).T
df2.columns = ['Period', 'Change']
df2.to_csv('period_change.csv', index = False)


########## counting games in each period #########

print(df.columns.values)

for period in periods_list:
	print('###', period, '###')
	for year in years:
		print(year)
		temp = df.loc[(df['Year'] == year) & (df['Period'] == period), :]
		temp.drop_duplicates('Round', inplace = True)
		print(len(temp))



prems_df.to_csv('win_percentage.csv', index = False)




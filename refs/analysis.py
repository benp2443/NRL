import pandas as pd
import numpy as np

df = pd.read_csv('../data/NRL.csv')

# 2 refs starting in 2009. Hence subset data from 2009 onwards and create a list of teams

df = df.loc[df['Year'] != 2008, :].reset_index()
teams = df['Home'].unique().tolist()

# Create individual columns for both refs

df['ref1'] = ''
df['ref2'] = ''

i = 0

while i < len(df):
	
	refs = df.loc[i, 'Referee/s'].split(',', 1)
	df.loc[i, 'ref1'] = refs[0].strip()
	df.loc[i, 'ref2'] = refs[1].strip()
	
	i += 1

data = pd.DataFrame()
first_loop = True

for team in teams:

	# Subset df to only include Manly games

	df2 = df.loc[(df['Home'] == team) | (df['Away'] == team), ['Year', 'Home', 'Away', 'HomeWin', 'ref1', 'ref2']].reset_index(drop = True)

	# Create TeamWin column. 1 if team won the game and 0 if they lost

	df2['TeamWin'] = 0

	i = 0

	while i < len(df2):

		hw = df2.loc[i, 'HomeWin']
		home_team = df2.loc[i, 'Home']

		if home_team == team and hw == 1:
			df2.loc[i, 'TeamWin'] = 1
		
		elif home_team != team and hw == 0:
			df2.loc[i, 'TeamWin'] = 1

		i += 1

	# Drop unneccesary columns and melt dataframe for analysis

	df2.drop(['Home', 'Away', 'HomeWin'], axis = 1, inplace = True)
	
	df2['Team'] = team
	df2_melt = pd.melt(df2, id_vars = ['Year', 'Team', 'TeamWin'])
	
	df2_melt.drop(['variable'], axis = 1, inplace = True)
	df2_melt.columns = ['Year', 'Team', 'TeamWin', 'Referee']

	# Return list of refs who have refereed Manly > 15 times

	ref_counts = df2_melt['Referee'].value_counts().reset_index(drop = False)
	ref_counts.columns = ['Referee', 'Count']

	referees = ref_counts.loc[ref_counts['Count'] > 15, 'Referee'].values.tolist()

	# Record Manly's win percentage with each referee and Manly's win percentage without that referee

	win_percent = pd.DataFrame(referees, columns = ['referee'])
	win_percent['team'] = team
	win_percent['with'] = 0.0
	win_percent['without'] = 0.0
	win_percent['difference'] = 0.0

	for ref in referees:

		with_ref = df2_melt.loc[df2_melt['Referee'] == ref, ]

		# Find time period in dataset this ref is present
		start = with_ref['Year'].min()
		end = with_ref['Year'].max()

		# Futher filter with_ref df to only include years which ref was in the dataset
		# and create without_ref df to include games within that period that ref was not involved in
		with_ref = with_ref.loc[(with_ref['Year'] >= start) & (with_ref['Year'] <= end), :]
		without_ref = df2_melt.loc[(df2_melt['Referee'] != ref) & (df2_melt['Year'] >= start) & (df2_melt['Year'] <= end), :]

		win_percent_with = with_ref['TeamWin'].mean()
		win_percent_without = without_ref['TeamWin'].mean()
		diff = (win_percent_with - win_percent_without)*100

		win_percent.loc[win_percent['referee'] == ref, 'with'] = win_percent_with
		win_percent.loc[win_percent['referee'] == ref, 'without'] = win_percent_without
		win_percent.loc[win_percent['referee'] == ref, 'difference'] = diff

	if first_loop == True:
		data = win_percent
		first_loop = False
	else:
		data = pd.concat([data, win_percent], axis = 0)


data.to_csv('teams_refs.csv', index = False)

	











import pandas as pd
import numpy as np
pd.set_option("display.max_rows", 150)

df = pd.read_csv('../data/NRL.csv')

# Annual crowd sizes

print(df.head())

temp = df.groupby('Year')['Crowd'].agg(['count', 'sum'])
print(temp)

temp2 = df.groupby('Period')['Crowd'].agg(['count', 'mean'])

# Create column which is home if team is at a home group and neutral overwise

crowd_df = df.loc[df['Period'] != 'Finals', :]

# if the team has played 12 or more games at a ground, consider it a home ground

crowd_df['Stadium_'] = ""

teams = crowd_df['Home'].unique().tolist()

for team in teams:

	temp = crowd_df.loc[crowd_df['Home'] == team, :]
	grounds = temp['Stadium'].unique().tolist()

	for ground in grounds:
		temp2 = temp.loc[temp['Stadium'] == ground, :]

		if len(temp2) >= 12:
			crowd_df.loc[(crowd_df['Home'] == team) & (crowd_df['Stadium'] == ground), 'Stadium_'] = 'h'

		else:			
			crowd_df.loc[(crowd_df['Home'] == team) & (crowd_df['Stadium'] == ground), 'Stadium_'] = 'n'

melb_stadiums = ['Telstra Dome', 'Etihad']


# UGLY! CLEAN UP

crowd_df.loc[(crowd_df['Home'] == 'Melbourne') & ((crowd_df['Stadium'] == 'Telstra Dome') | (crowd_df['Stadium'] == 'Etihad')), 'Stadium_'] = 'h'
crowd_df.loc[(crowd_df['Home'] == 'Warriors') & (crowd_df['Stadium'] == 'Eden Park'), 'Stadium_'] = 'h'
crowd_df.loc[(crowd_df['Home'] == 'St George Illawarra') & (crowd_df['Stadium'] == 'UOW Jubilee'), 'Stadium_'] = 'h'
crowd_df.loc[(crowd_df['Home'] == 'Penrith') & (crowd_df['Stadium'] == 'Sportingbet'), 'Stadium_'] = 'h'
crowd_df.loc[(crowd_df['Home'] == 'Manly Warringah') & (crowd_df['Stadium'] == 'Lottoland'), 'Stadium_'] = 'h'
crowd_df.loc[(crowd_df['Home'] == 'Cronulla') & (crowd_df['Stadium'] == 'Shark Stadium'), 'Stadium_'] = 'h'
crowd_df.loc[(crowd_df['Home'] == 'Bulldogs') & (crowd_df['Stadium'] == 'Belmore'), 'Stadium_'] = 'h'

drop_idx = crowd_df.loc[crowd_df['Stadium_'] == 'n', :].index.values.tolist()
crowd_df = crowd_df.drop(drop_idx, axis = 0)

crowds = crowd_df.groupby(['Year', 'Home'])['Crowd'].agg(['count', 'mean', 'min', 'max']).reset_index()
crowds['mean'] = crowds['mean'].round(0)
crowds.rename(columns = {'Home': 'Team'}, inplace = True)
crowds['test'] = -1.0

teams = crowds['Team'].unique().tolist()


for team in teams:
	temp = crowds.loc[crowds['Team'] == team, :]
	min_ = temp['min'].min()
	max_ = temp['max'].max()

	idx = temp.index.tolist()

	crowds.loc[crowds.index.isin(idx), 'test'] = (crowds['mean'] - min_) / (max_ - min_)


ladder_df = pd.read_csv('../data/nrl_ladder.csv')

temp = pd.merge(crowds, ladder_df, how = 'inner', left_on = ['Year', 'Team'], right_on = ['Year', 'Team'])

temp = temp[['Year', 'Team', 'test', 'Rank']]

print(crowds.head(32))
print(ladder_df.head(32))
print(temp)


temp.to_csv('test.csv', index = False)

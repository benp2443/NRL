import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 150)

df = pd.read_csv('../data/NRL.csv')

# Annual crowd sizes

temp = df.loc[df['Period'] != 'Finals', :]
temp1 = temp.groupby('Year')['Crowd'].agg(['count', 'sum']).reset_index()

temp1['base_growth'] = 0.0
temp1['yearly_growth'] = 0.0
temp1['yearly_change'] = 0

base_year = temp1.loc[0, 'sum']

i = 0
while i < len(temp1):
	

	if i == 0:
		i += 1
		continue
	
	current = temp1.loc[i, 'sum']
	last = temp1.loc[i-1, 'sum']
	
	temp1.loc[i, 'base_growth'] = round(((current - base_year) / base_year)*100,1)
	temp1.loc[i, 'yearly_growth'] = round(((current - last) / last)*100,1)
	temp1.loc[i, 'yearly_change'] = current - last

	i += 1

temp1.to_csv('data/yearly_crowds.csv', index = False)

temp2 = df.loc[df['Round'] != 'Grand Final', :]
temp2 = df.groupby('Period')['Crowd'].agg(['count', 'mean']).reset_index()
temp2.to_csv('data/period_crowd.csv', index = False)

temp3 = temp.groupby('Home')['Crowd'].mean().round(0).reset_index()
temp3.to_csv('data/teams_average.csv', index = False)

# Broncos analysis

broncs = temp.loc[temp['Home'] == 'Brisbane', :].reset_index()

temp4 = broncs.groupby('Day')['Crowd'].agg(['count', 'mean']).reset_index()
temp4.to_csv('data/broncs_days.csv', index = False)

broncs['fri_other'] = broncs['Day'].apply(lambda x: 'Friday' if x == 'Fri' else 'Other')

temp5 = broncs.groupby('fri_other')['Crowd'].count().reset_index()
temp5.to_csv('data/broncs_fri_other.csv', index = False)

# Day analysis of crowd size

temp6 = temp.loc[temp['Home'] != 'Brisbane', :]
temp6 = temp6.loc[~temp['Day'].isin(['Tue', 'Wed']), :]
temp6 = temp6.groupby('Day')['Crowd'].mean().round(0).reset_index()
temp6.to_csv('data/days_crowds_exl_bris.csv', index = False)

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

temp = temp[['Year', 'Team', 'mean', 'test', 'Rank']]

print(temp)


temp.to_csv('data/test.csv', index = False)

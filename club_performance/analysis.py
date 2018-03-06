# Import Libraries and load data
import pandas as pd
import numpy as np

df = pd.read_csv('../data/NRL_ladder.csv')

######### Binned Positions #########

df['top_5'] = 0
df['bot_5'] = 0
df['mid_6'] = 0

i = 0

while i < len(df):
	
	rank = df.loc[i, 'Rank']

	if rank <=5:
		df.loc[i, 'top_5'] = 1
	elif rank >= 12 and rank <= 16:
		df.loc[i, 'bot_5'] = 1
	else:
		df.loc[i, 'mid_6'] = 1

	i += 1


temp = df.loc[:, ['Team', 'top_5', 'bot_5', 'mid_6']]
temp = temp.groupby('Team').sum().reset_index()
temp = pd.melt(temp, id_vars = ['Team'])

temp.to_csv('top_bot_5.csv', index = False)

########## Average Position ##########

temp = df.groupby('Team')['Rank'].mean().reset_index()
temp.columns = ['Team', 'Average_rank']
temp.to_csv('average_rank.csv', index = False)


########## Win Percentage ##########

df['Played'] = df['W'] + df['D'] + df['L']

temp = df.groupby('Team')['W', 'Played'].sum().reset_index()
temp['Win_Percentage'] = temp['W']/temp['Played']
temp.to_csv('win_percentage.csv', index = False)














# Import libraries, gameBygame.csv and drop empty column

import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('data/gameBygame.csv')

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


# Add home win boolean column

df['HomeWin'] = df['H_PTS'] > df['A_PTS']

# load SOO_dates data

soo = pd.read_csv('data/soo_dates.csv')

# Clean data

soo['date'] = soo['date'].str.replace('th', '').str.replace('st', '').str.replace('nd', '').str.replace('rd', '').str.replace(' ', '-')
soo['date'] = pd.to_datetime(soo['date'], format = "%Y-%b-%d")

years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

df['SOO'] = False

df_date = df.columns.values.tolist().index('date_time')
df_date = df.columns.values.tolist().index('SOO')
soo_date = soo.columns.values.tolist().index('date')

for year_ in years:

	idx_list = df.loc[df['date_time'].dt.year == year_, :].index.values.tolist()
	date_interval = soo.loc[soo['date'].dt.year == year_, :]

	i = idx_list[0]

	while i <= idx_list[-1]:

		row_date = df.iat[i, df_date]

		if ((date_interval.iat[0, soo_date] - row_date).dt.days < 0) and ((date_interval.iat[2, soo_date] - row_date).dt.days > 0):
			df.iat[i, SOO] = True

		i += 1





# Save dataframe to csv

#df.to_csv('data/NRL_cleaned.csv', index = False)

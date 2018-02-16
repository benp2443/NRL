# Import libraries, load data and drop empty column

import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('NRL.csv')

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


df['HomeWin'] = df['H_PTS'] > df['A_PTS']

df.to_csv('NRL_cleaned.csv', index = False)

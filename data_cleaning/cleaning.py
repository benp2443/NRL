# Import libraries, gameBygame.csv and drop empty column

import pandas as pd
import numpy as np
from datetime import datetime
import copy
pd.set_option("display.max_rows", 150)

df = pd.read_csv('../data/gameBygame.csv')

df.drop(['delete'], axis = 1, inplace = True)

# Covert Crowd to integer and create a datetime variable

df['Crowd'] = df['Crowd'].str.replace(',','').astype(int)

df['Date'] = df['Date'].str.replace('th', '').str.replace('st', '').str.replace('nd', '').str.replace('rd', '').str.replace(' ', '-')
df['date_time'] = df['Year'].astype(str) + '-' + df['Date'] + ' ' + df['Time']
df['date_time'] = pd.to_datetime(df['date_time'], format = "%Y-%b-%d %I:%M%p")

# Over different seasons, the bulldogs have different names ('Canterbury', and 'Bulldogs'). Convert to just 'Bulldogs'.

df.loc[(df['Home'] == 'Canterbury'), 'Home'] = 'Bulldogs'
df.loc[(df['Away'] == 'Canterbury'), 'Away'] = 'Bulldogs'

# Clean up the stadiums due to home teams changing stadium names

stadiums = df['Stadium'].unique().tolist()
print(stadiums)
print(len(stadiums))

group = df.groupby(['Home', 'Stadium'])['Crowd'].count()
print(group)

print(len(df['Home'].unique()))
print(df['Home'].unique())

df.to_csv('../data/gameBygame_cleaned.csv', index = False)

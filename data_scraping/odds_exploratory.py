import pandas as pd
import numpy as np

df = pd.read_csv('odds_data.csv', encoding = "ISO-8859-1")
print(len(df))
df['year'] = df['date'].str[-4:] 
# Duplicates
#dups = df.drop_duplicates()
#group_dups = dups.groupby(by = 'year')['home'].count()
#print(group_dups)
#
## Null odds
#odd1_null = df.loc[df['home_odds'] == -1, :]
#print(len(odd1_null))
#
#odd2_null = df.loc[df['away_odds'] == -1, :]
#print(len(odd2_null))
#
#both_null = df.loc[(df['home_odds'] == -1) & (df['away_odds'] == -1), :]
#print(len(both_null))
#
#temp = df.groupby(['date', 'home', 'away'])['home_odds'].count().reset_index()
#print(temp.loc[temp['home_odds'] == 5, :])
##print(temp['date'].unique())
##print(temp['home_odds'].value_counts())
#
#print(df.loc[df['date'] == '01 Oct 2017', :])


df = df.drop_duplicates()

overtime_df = df.loc[df['overtime'] == True, :]
final = overtime_df.groupby('year')['home'].count().reset_index()
final.rename(columns = {'home':'count'}, inplace = True)
print(final)
final.to_csv('overtime_counts.csv', index = False)

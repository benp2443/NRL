import numpy as np
import pandas as pd
import sys

df = pd.read_csv('../data/NRL_cleaned.csv')

# Create list of premiers and years

premiers = ['Manly Warringah', 'Melbourne', 'St George Illawarra', 'Manly Warringah', 'Melbourne', \
	'Sydney', 'South Sydney', 'North Queensland', 'Cronulla'] # excluded 2017 premiers (Melbourne) as no 2018 data

years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]


# Reduce dataset to only include the last round of the regular season (Round 26) and the first round of the finals (Qualif Final)
# Round 26 is included as defending premiers may not make the finals the following year and hence w/l percent will be taken from final round

temp = df.loc[(df['Round'] == 'Qualif Final') | (df['Round'] == 'Round 26'), :]

# win loss percentages will be appended to the following lists for the premiers
win_loss_premiers = []
win_loss_defending_premiers = []

i = 0
while i < 9:

	champs = premiers[i]
	prem_year = temp.loc[(temp['Year'] == years[i]) & (temp['Round'] == 'Qualif Final'), :]
	defending_year = temp.loc[temp['Year'] == years[i+1], :]

	h = df.columns.values.tolist().index('Home')
	a = df.columns.values.tolist().index('Away')
	h_w_percent = df.columns.values.tolist().index('Home_w_percent')
	a_w_percent = df.columns.values.tolist().index('Away_w_percent')

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
	

print(win_loss_premiers)
print(len(win_loss_premiers))

print(win_loss_defending_premiers)
print(len(win_loss_defending_premiers))


		

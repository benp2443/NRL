import numpy as np
import pandas as pd
import sys

df = pd.read_csv('../data/NRL_cleaned.csv')

print(df.Home.unique())
print(df.Year.unique())

premiers = ['Manly Warringah', 'Melbourne', 'St George Illawarra', 'Manly Warringah', 'Melbourne', \
	'Sydney', 'South Sydney', 'North Queensland', 'Cronulla'] # excluded 2017 team (Melbourne) as no 2018 data



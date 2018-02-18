import numpy as np
import pandas as pd
import sys

df = pd.read_csv('../data/NRL_cleaned.csv')

premiers = ['Manly Warringah', 'Melbourne', 'St George Illawarra', 'Manly Warringah', 'Melbourne', \
	'Sydney', 'South Sydney', 'North Queensland', 'Cronulla'] # excluded 2017 team (Melbourne) as no 2018 data

years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]


temp = df.loc[df['Round'] == 'Qualif Final', :]

i = 0
while i < 10:
	prem_year = df.loc[(df['


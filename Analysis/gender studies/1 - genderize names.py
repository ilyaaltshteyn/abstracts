#This script works with the author names dataset. Some stuff it does:
#1. Summary stats
#2. Assigns gender to each name
#------------------------------------------------------------------------------
#Setup: do imports, define printer

import csv, os, numpy, time
import pandas as pd
from pandas import read_csv
import sexmachine.detector as gender

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/gender studies/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

loc = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
data = read_csv(loc + 'names_split.csv')

#--Use sexmachine package to assign genders to each name:

#Create a gender detector:
d = gender.Detector(unknown_value='unknown', case_sensitive=False)
print d.get_gender('Alex')

data['first_auth_gender'] = 'untouched'
data['second_auth_gender'] = 'untouched'
data['third_auth_gender'] = 'untouched'
data['last_auth_gender'] = 'untouched'



start = time.time()
for row in range(len(data)):
	
	try:
		data.loc[row, 'first_auth_gender'] = str(d.get_gender(data.first_auth_name[row]))
	except:
		continue
	print str(float(row)/172000*100) + ' percent done' + ' on row ' + str(row)

	if data.second_auth_name[row] == 'untouched':
		continue
	try:
		data.loc[row, 'second_auth_gender'] = str(d.get_gender(data.second_auth_name[row]))
	except:
		data.loc[row, 'second_auth_gender'] = 'PULL_ERROR'
	
	if data.third_auth_name[row] == 'untouched':
		continue
	try:
		data.loc[row, 'third_auth_gender'] = str(d.get_gender(data.third_auth_name[row]))
	except:
		data.loc[row, 'third_auth_gender'] = 'PULL_ERROR'
	
	if data.last_auth_name[row] == 'untouched':
		continue
	try:
		data.loc[row, 'last_auth_gender'] = str(d.get_gender(data.last_auth_name[row]))
	except:
		data.loc[row, 'last_auth_gender'] = 'PULL_ERROR'


print time.time() - start

printer(data, filename = 'genderized_names_data.csv')





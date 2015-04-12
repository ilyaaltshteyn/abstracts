#This script does 3 things:
#1. Separates author and editor names into 1-info-unit columns. E.g. separate
#columns for first name, middle initial and last name; separate columns for
#separate people.

#2. Regularizes format of all dates

#3. Moves keywords into separate columns
#------------------------------------------------------------------------------


import csv, os, time, numpy
import pandas as pd
from pandas import read_csv

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

loc = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
data = read_csv(loc + 'all_merged_data.csv')

#**--- Separate names into separate columns:

def author_splitter(row):
	"""This separates each cell of authors into x cells of individual authors,
	returning the number of individual authors followed by their names in a list"""
	authors = data.authors[row]
	separate_authors = authors.split(';')
	return len(separate_authors), separate_authors

def name_splitter(auth):
	parts = auth.split(',')
	"""This function returns the surname, name combo as a tuple for what it took
	as input. parts[0] is the lastname, parts[1] is the firstname and middle 
	initials, but sometimes it's just the first initial bc some papers don't have 
	full author name listed."""
	return parts[0], parts[1].split()[0]

#Drop unnecessary columns to make data faster to work with (this leaves only
#the first column with numbers, and the author names column):
data = data[data.columns[[0,6]]]

#Run author_splitter on the entire dataset. Place first and last author
#names, then place second and third author names, then group the rest
#of the author names into one cell.

#Create columns for splitting author names:
data['auth_count'] = 'untouched'
data['first_auth_name'] = 'untouched'
data['first_auth_surname'] = 'untouched'
data['second_auth_name'] = 'unoutched'
data['second_auth_surname'] = 'untouched'
data['third_auth_name'] = 'untouched'
data['third_auth_surname'] = 'untouched'
data['last_auth_name'] = 'untouched'
data['last_auth_surname'] = 'untouched'

start = time.time()
for row in range(len(data)):
	try:
		auths = author_splitter(row)
		data.loc[row, 'auth_count'] = auths[0]
	except:
		continue
	try:
		first_auth = name_splitter(auths[1][0])
		data.loc[row, 'first_auth_surname'] = first_auth[0]
		data.loc[row, 'first_auth_name'] = first_auth[1]
	except:
		continue
	if auths[0] > 1:
		try:
			second_auth = name_splitter(auths[1][1])
			data.loc[row, 'second_auth_surname'] = second_auth[0]
			data.loc[row, 'second_auth_name'] = second_auth[1]
		except:
			continue
		if auths[0] > 2:
			try:
				third_auth = name_splitter(auths[1][2])
				data.loc[row, 'third_auth_surname'] = third_auth[0]
				data.loc[row, 'third_auth_name'] = third_auth[1]
			except:
				continue
			if auths[0] > 3:
				try:
					last_auth = name_splitter(auths[1][len(auths[1])-1])
					data.loc[row, 'last_auth_surname'] = last_auth[0]
					data.loc[row, 'last_auth_name'] = last_auth[1]
				except:
					continue

	print str(float(row)/172810*100) + " percent finished"

print time.time() - start
#Now write output file to 

printer(data, 'names_split.csv')


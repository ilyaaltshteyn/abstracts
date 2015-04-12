#This script investigates the basic sexism question over time.


import csv, os, time, numpy
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
import seaborn

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/gender studies/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

loc = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
data = read_csv(loc + 'all_data_merged_restructured.csv')

#Split data into frames based on year, putting all frames into a dictionary
#called data_by_years
years = range(1950, 2013)

data_by_years = {}
for year in years:
	yr = str(year)
	data_by_years[yr] = data[data['year'] == year]

#-----START BY LOOKING AT DISPARITY BETWEEN FIRST AND SECOND AUTHORSHIP FOR WOMEN OVER TIME
#IN ALL MULTI-AUTHOR PAPERS:
#Pull out rows for multiauthor papers where both the first and second author names 
#have hard genders.
#Put summary stats about those rows into a dataframe that summarizes the sexism
#over time.
hard_genders_list = ['male', 'female']

sexism_over_time = pd.DataFrame(columns = ('year', 'first_auth_percent_female', 'second_auth_percent_female',
	'first_auth_female_count', 'second_auth_female_count', 'total papers', 'sexism'))

for year in years:
	dat = data_by_years[str(year)]
	dat = dat[dat['auth_count']>1]
	dat_hard_genders = dat[dat.first_auth_gender.isin(hard_genders_list)]
	dat_hard_genders = dat_hard_genders[dat_hard_genders.second_auth_gender.isin(hard_genders_list)]
	print total
	d = dat_hard_genders
	#How many total papers are there?
	total = float(len(d))
	#What percent of them have a female first author?
	first_auth_sex = len(d[d.first_auth_gender == 'female'])
	first_percent = first_auth_sex/total
	#What percent of them have a female second author?
	second_auth_sex = len(d[d.second_auth_gender == 'female'])
	second_percent = second_auth_sex/total
	sexism = second_percent - first_percent

	new_data = {'year': year, 'first_auth_percent_female' : first_percent, 'second_auth_percent_female' : second_percent,
	'first_auth_female_count' : first_auth_sex, 'second_auth_female_count' : second_auth_sex, 'total papers' : total,
	'sexism' : sexism}
	sexism_over_time = sexism_over_time.append(new_data, ignore_index = True)

#Plot first authorship vs second authorship for women across time:
first = list(sexism_over_time.first_auth_percent_female)
second = list(sexism_over_time.second_auth_percent_female)
plt.plot(years, first)
plt.plot(years, second)

plt.show()

#Plot the disparity between first and second authorships for women 
#across time, with above-zero numbers representing sexism and below-
#zero numbers representing reverse sexism:
plt.plot(years, sexism_over_time.sexism)
plt.show()

#----------REPEAT ALL THAT FOR 4 + AUTHOR PAPERS, LOOKING @ FIRST VS THIRD AUTHORSHIP
#Pull out rows for 4+ author papers where both the first and third author names 
#have hard genders.
#Put summary stats about those rows into a dataframe that summarizes the sexism
#over time.
hard_genders_list = ['male', 'female']

sexism_over_time_b = pd.DataFrame(columns = ('year', 'first_auth_percent_female', 'third_auth_percent_female',
	'first_auth_female_count', 'third_auth_female_count', 'total papers', 'sexism'))

for year in years:
	dat = data_by_years[str(year)]
	dat = dat[dat['auth_count']>3]
	dat_hard_genders = dat[dat.first_auth_gender.isin(hard_genders_list)]
	dat_hard_genders = dat_hard_genders[dat_hard_genders.third_auth_gender.isin(hard_genders_list)]
	print total
	d = dat_hard_genders
	#How many total papers are there?
	total = float(len(d))
	#What percent of them have a female first author?
	first_auth_sex = len(d[d.first_auth_gender == 'female'])
	first_percent = first_auth_sex/total
	#What percent of them have a female third author?
	third_auth_sex = len(d[d.third_auth_gender == 'female'])
	third_percent = third_auth_sex/total
	sexism = third_percent - first_percent

	new_data = {'year': year, 'first_auth_percent_female' : first_percent, 'third_auth_percent_female' : third_percent,
	'first_auth_female_count' : first_auth_sex, 'third_auth_female_count' : third_auth_sex, 'total papers' : total,
	'sexism' : sexism}
	sexism_over_time_b = sexism_over_time_b.append(new_data, ignore_index = True)

#Plot first authorship vs third authorship for women across time:
first = list(sexism_over_time_b.first_auth_percent_female)[20:]
third = list(sexism_over_time_b.third_auth_percent_female)[20:]
plt.plot(years[20:], first)
plt.plot(years[20:], third)
plt.show()

#Plot the disparity between first and third authorships for women 
#across time, with above-zero numbers representing sexism and below-
#zero numbers representing reverse sexism:
plt.plot(years[20:], sexism_over_time_b.sexism[20:])
plt.show()

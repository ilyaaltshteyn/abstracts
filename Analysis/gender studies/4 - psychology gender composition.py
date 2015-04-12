#This script computes the breakdown of publishing psychologists by gender
#over time, to answer the question "how has the gender composition of
#academic psychology changed over time?"

import csv, os, time, numpy
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
import seaborn as sns

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/gender studies/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

#Read all data, bc you'll need year data, auth genders and auth names:
loc = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
data = read_csv(loc + 'all_data_merged_restructured.csv')

#Remove unnecessary columns:
dels = ['Unnamed: 0.1', 'authors', 'abstract', 'title', 'date', 'journal',
     'publisher', 'journal_vol', 'journal_issue', 'firstpage',
    'doi', 'abstract_html', 'fulltext_html', 'pdf_url', 'keywords', 'language',
    'editor_name', 'editor_surname']

for x in dels:
    del data[x]

#Now you want to make the data vertical and split it up by author, so
#there is ONE ROW PER AUTHOR. Then you can remove doubles and count the
#number of men and women.
firsts_list = ['year', 'auth_count', 'first_auth_name', 'first_auth_surname', 'first_auth_gender']
firsts = data[firsts_list]
firsts.columns = ['year', 'auth_count', 'name', 'surname', 'gender']
seconds_list = ['year', 'auth_count', 'second_auth_name', 'second_auth_surname', 'second_auth_gender']
seconds = data[seconds_list]
seconds.columns = ['year', 'auth_count', 'name', 'surname', 'gender']
thirds_list = ['year', 'auth_count', 'third_auth_name', 'third_auth_surname', 'third_auth_gender']
thirds = data[thirds_list]
thirds.columns = ['year', 'auth_count', 'name', 'surname', 'gender']
lasts_list = ['year', 'auth_count', 'last_auth_name', 'last_auth_surname', 'last_auth_gender']
lasts = data[lasts_list]
lasts.columns = ['year', 'auth_count', 'name', 'surname', 'gender']

vertical = firsts.append(seconds, ignore_index = True)
vertical = vertical.append(thirds, ignore_index = True)
vertical = vertical.append(lasts, ignore_index = True)

#Create full name column, with whitespace stripped using pandas strip:
vertical['full_name'] = pd.Series(vertical.name.str.strip() + ' ' +
    vertical.surname.str.strip(), index = vertical.index)

#Isolate data for a given year, remove non-unique names for that year, count
#total men/women and convert to percentages:
years = range(1970,2012)
yearly_stats = pd.DataFrame(columns = ['men', 'women', 'percent_women'])
for yr in years:
    yr_data = vertical[vertical.year == yr]
    yr_data.drop_duplicates(subset = 'full_name', inplace = True)
    male_count = float(sum(yr_data.gender == 'male'))
    female_count = float(sum(yr_data.gender == 'female'))
    percent_women = float(female_count/(male_count + female_count))
    yearly_stats.loc[yr] = [male_count, female_count, percent_women]

#Print new data into a separate csv file:
printer(yearly_stats, filename = 'gender_breakdown_by_year.csv')

#Import data about bachelors degrees conferred TO WOMEN by year and major:
loc = '/Users/ilya/Documents/Abstracts project/Analysis/gender studies/'
bachelors_degrees = read_csv(loc + 'bachelors degrees by year and major.csv')
bachelors_degrees.Psychology = bachelors_degrees.Psychology/100

#Import data about PSYCHOLOGY phds conferred by year:
phds = read_csv(loc + 'psych phds by year and sex.csv')

#Visualize the gender breakdown of publishing psychologists by year:
sns.set(style = 'white', palette = 'Set2')
#plt.plot(years,list(bachelors_degrees.Psychology))
plt.plot(years, list(phds.percent_women), label = 'Psychology phds')
plt.plot(years, list(yearly_stats.percent_women), label = 'Publishing psychologists')
plt.legend()
plt.axis(xmin = 1970, xmax = 2011)
plt.xlabel('Year')
plt.ylabel('Proportion women')
plt.title('Proportion women among publishing psychologists\n and among psychology PhDs by year')
plt.legend(loc = 2)
sns.despine()
plt.show()

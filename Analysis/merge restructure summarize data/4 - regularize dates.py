#This script regularizes the date formats, putting the year into a separate column
#and tossing month data (for now). Then it merges the names_split.csv file with
#the final data into a master file.

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

#---Split year off of data and into its own column:

data['year'] = 'untouched'

data['year'] = data['date'].map(lambda x: str(x)[-4:])

printer(data, 'restructured.csv')

#---Merge names_split.csv into the data:
genderized_names = read_csv('/Users/ilya/Documents/Abstracts project/Analysis/gender studies/' + 'genderized_names_data.csv')

all_data = pd.concat([data, genderized_names], axis = 1)

printer(all_data, 'all_data_merged_restructured.csv')





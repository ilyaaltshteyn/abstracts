#This script combines the raw datafiles and fixes some missing data and removes 
#the extra ownership info that's at the end of some abstracts.

import csv, os
import pandas as pd
from pandas import read_csv

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

#Make a list of the files that have abstracts with DOIs in them:
abstracts_dir = '/Users/ilya/Documents/Abstracts project/Scraping tools/abstracts with citation counts/'
abstracts_files = os.listdir(abstracts_dir)

total = 0
for f in abstracts_files[1:]:
    #Read the abstracts file into a dataframe called df:
    file = abstracts_dir + f
    df = read_csv(file)
    file_length = len(df.index)
    total += file_length

print 'We have %d rows of abstracts data' % total

all_data = pd.DataFrame()
for f in abstracts_files[1:]:
    print f
    file = abstracts_dir + f
    temp = read_csv(file)
    
    #Replace PULL_ERRORs in journal name column with the journal 
    #name from another row, and delete ownership info from end
    #of abstract.
    for row in range(len(temp.index)):
        if temp['journal'][row] == 'PULL_ERROR':
            try:
                temp['journal'][row] = temp['journal'][row - 2]
            except:
                temp['journal'][row] = temp['journal'][row + 1]

        if temp['abstract'][row][-25:] == 'APA, all rights reserved)':
            temp['abstract'][row] = temp['abstract'][row][:-61]        

    all_data = all_data.append(temp)

printer(all_data, 'all_merged_data.csv')




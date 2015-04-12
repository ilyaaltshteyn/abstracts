#This script does some basic analysis of the abstracts data

import csv, os
import pandas as pd
from pandas import read_csv
import matplotlib as mpl
import matplotlib.pyplot as plt, seaborn as sns, numpy as np
from numpy.random import randn
from scipy import stats
from matplotlib.font_manager import FontProperties

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

loc = '/Users/ilya/Documents/Abstracts project/Analysis/merge restructure summarize data/'
data = read_csv(loc + 'all_merged_data.csv')

#***Step 1-- graph number of papers per journal
abstracts_dir = '/Users/ilya/Documents/Abstracts project/Scraping tools/abstracts with citation counts/'
abstracts_files = os.listdir(abstracts_dir)

total = 0
journals_data = pd.DataFrame()
for f in abstracts_files[1:]:
    print f
    #Read the abstracts file into a dataframe called df:
    name = f[11:14]
    file = abstracts_dir + f
    df = read_csv(file)
    file_length = len(df.index)
    total += file_length
    new_dat = [[name, file_length]]
    journals_data = journals_data.append(new_dat)

print total

journals_data.columns = ['journal', 'abstract_count']
journals_data.index = range(100)

ordered_dat = journals_data['abstract_count'].order(ascending = False)
hist = pd.Series.plot(ordered_dat, kind = 'bar', color = sns.desaturate('indianred', .75), 
	ylim = (0, 13000), xticks = [], alpha = .9)
hist.grid(b = 'off', axis = 'x')
hist.set_xlabel('Each bar represents one journal')
hist.set_ylabel('Number of abstracts in dataset')
hist.set_title('Distribution of 171,810 abstracts across the 100 journals in the dataset')
hist.lines[0].set_visible(False)
plt.show()




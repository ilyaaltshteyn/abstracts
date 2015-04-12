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

dels = list(data.columns)
for x in dels:
    if (x != 'year' and x != 'auth_count'):
        del data[x]

years = range(1950,2014)
yearly_stats = pd.DataFrame(columns = ['year', 'author_count'])
for year in years:
    dat = data[data.year == year]
    count = numpy.mean(dat.auth_count)
    yearly_stats.loc[year] = [year, count]

sns.set(style = 'white', palette = 'Set2')
#plt.plot(years,list(bachelors_degrees.Psychology))
plt.plot(years, list(yearly_stats.author_count))
plt.axis(xmin = 1950, xmax = 2013)
plt.xlabel('Year')
plt.ylabel('Average authors per paper')
plt.title('Number of authors per psychology paper, n = 147,806 papers')
sns.despine()
plt.show()


#Compute the average citations for papers with a male first author vs a female first author:
male_firsts = data[data.first_auth_gender == 'male']
female_firsts = data[data.first_auth_gender == 'female']

#Throw out non-integer and Nan data for male and female first authors:
male_firsts = male_firsts[male_firsts.citation_count.notnull()]
female_firsts = female_firsts[female_firsts.citation_count.notnull()]
ints_male = [isinstance(element, int) for element in male_firsts.citation_count]
ints_female = [isinstance(element, int) for element in female_firsts.citation_count]
male_firsts = male_firsts[ints_male]
female_firsts = female_firsts[ints_female]
print "male first authors get %f citations" % (numpy.mean(male_firsts.citation_count),)
print "female first authors get %f citations" % (numpy.mean(female_firsts.citation_count),)
male_firsts.citation_count.hist(bins = 100)
plt.show()
female_firsts.citation_count.hist(bins = 100)
plt.show()




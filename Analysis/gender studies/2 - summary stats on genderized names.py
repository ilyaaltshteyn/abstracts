#This script does some summary stats on the genderized names.

#------------------------------------------------------------------------------

import csv, os, time, numpy
import pandas as pd
from pandas import read_csv

def printer(df, filename = 'temporary.csv'):
    path = '/Users/ilya/Documents/Abstracts project/Analysis/gender studies/'
    name = path + filename
    df.to_csv(path_or_buf = name, encoding = 'utf-8')

loc = '/Users/ilya/Documents/Abstracts project/Analysis/gender studies/'
data = read_csv(loc + 'genderized_names_data.csv')

#--Separate data into subsets with multiple author/single author papers:
multi_author = data[data['auth_count']>1]
single_author = data[data['auth_count'] == 1]
threeplus_author = data[data['auth_count'] > 2]
fourplus_author = data[data['auth_count'] > 3]
fiveplus_author = data[data['auth_count'] > 4]

#Pull out rows where both the first and second author names have hard genders.
#Hard genders are 'male' or 'female', as opposed to, e.g. 'mostly_male'
#Easiest way to do this is to remove all rows with "unknown" in them, which is 
#the code that I had the genderizer tool assign when it didn't know the answer.
hard_genders_list = ['male', 'female']

single_author_hard_genders = single_author[single_author.first_auth_gender.isin(hard_genders_list)]

multi_auth_hard_genders = multi_author[multi_author.first_auth_gender.isin(hard_genders_list)]
multi_auth_hard_genders = multi_auth_hard_genders[multi_auth_hard_genders.second_auth_gender.isin(hard_genders_list)]

#Separate first author + third author hard gender papers with three or more authors
threeplus_author_hard_genders = threeplus_author[threeplus_author.first_auth_gender.isin(hard_genders_list)]
threeplus_author_hard_genders = threeplus_author_hard_genders[threeplus_author_hard_genders.third_auth_gender.isin(hard_genders_list)]

#---
#OBSCURE AUTHORSHIP:
#Third authors in 4+ author papers:
fourplus_author_hard_genders = fourplus_author[fourplus_author.first_auth_gender.isin(hard_genders_list)]
fourplus_author_hard_genders = fourplus_author_hard_genders[fourplus_author_hard_genders.third_auth_gender.isin(hard_genders_list)]

#Third authors in 5+ author papers:
fiveplus_author_hard_genders = fiveplus_author[fiveplus_author.first_auth_gender.isin(hard_genders_list)]
fiveplus_author_hard_genders = fiveplus_author_hard_genders[fiveplus_author_hard_genders.third_auth_gender.isin(hard_genders_list)]

#So now we have a dataframe called multi_auth_hard_genders that contains 69,590 
#rows of data. The data is for papers that have multiple authors AND for which
#there is a hard gender for both the first AND second authors. Now we look at
#the percentage of first authors who are women compared to second authors who
#are women.


m = multi_auth_hard_genders
print len(m)
#The answer is 69,590
print len(m[m.first_auth_gender == 'female'])
#The answer is 22,581, which is 32.4%
print len(m[m.second_auth_gender == 'female'])
#The answer is 23,116, which is 33.2%

t = threeplus_author_hard_genders
print len(t)
#The answer is 36,441
print len(t[t.first_auth_gender == 'female'])
#The answer is 12,887, which is 35.4%
print len(t[t.third_auth_gender == 'female'])
#The answer is 13,737, which is 37.7%

#---
#OBSCURE AUTHORSHIP:
#Third authors in 4+ author papers:
f = fourplus_author_hard_genders
print len(f)
#The answer is 18,201
print len(f[f.first_auth_gender == 'female'])
#The answer is 7,008, which is 38.5%
print len(f[f.third_auth_gender == 'female'])
#The answer is 7,835, which is 43.0%

#Third authors in 5+ author papers:
fi = fiveplus_author_hard_genders
print len(fi)
#The answer is 9,005
print len(fi[fi.first_auth_gender == 'female'])
#The answer is 3,625, which is 40.3%
print len(fi[fi.third_auth_gender == 'female'])
#The answer is 4,088, which is 45.4%

#---
#NUMBER OF AUTHORS X FIRST AUTHOR GENDER:
#Does number of authors predict gender of first author?
papers_with_hard_gender_first_author = data[data.first_auth_gender.isin(hard_genders_list)]
print len(papers_with_hard_gender_first_author)
#Answer is 130,236
#% of woman first authors on single-author papers:
s = papers_with_hard_gender_first_author[papers_with_hard_gender_first_author.auth_count == 1]
print len(s)
#Answer is 49,869
print len(s[s.first_auth_gender == 'female'])
#Answer is 10,127, which is 20.3%

#% of woman first authors on 2-author papers:
s = papers_with_hard_gender_first_author[papers_with_hard_gender_first_author.auth_count == 2]
print len(s)
#Answer is 37,688
print len(s[s.first_auth_gender == 'female'])
#The answer is 11,041, which is 29.3%

#% of woman first authors on 3-author papers:
s = papers_with_hard_gender_first_author[papers_with_hard_gender_first_author.auth_count == 3]
print len(s)
#Answer is 21,239
print len(s[s.first_auth_gender == 'female'])
#The answer is 6,867, which is 32.3%

#% of woman first authors on 4-author papers:
s = papers_with_hard_gender_first_author[papers_with_hard_gender_first_author.auth_count == 4]
print len(s)
#Answer is 10,772
print len(s[s.first_auth_gender == 'female'])
#The answer is 3,983, which is 37.0%

#% of woman first authors on 5-author papers:
s = papers_with_hard_gender_first_author[papers_with_hard_gender_first_author.auth_count == 5]
print len(s)
#Answer is 5,182
print len(s[s.first_auth_gender == 'female'])
#The answer is 2,022, which is 39.0%

#% of woman first authors on 6+ author papers:
s = papers_with_hard_gender_first_author[papers_with_hard_gender_first_author.auth_count > 5]
print len(s)
#Answer is 5,486
print len(s[s.first_auth_gender == 'female'])
#The answer is 2,303, which is 42.0%






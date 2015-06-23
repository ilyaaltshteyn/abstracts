# This script separates out the columns of data that have the author genders
# and names, as well as the columns for years and author counts.  
# It then runs a chi squared test on the proportions of male and female 
# authors who are first auth vs second vs third vs last.

# Here's a link to an explanation of how to do chi-squared test in Python:
# http://connor-johnson.com/2014/12/31/the-pearson-chi-squared-test-with-python-and-r/

#                      ****PREPARE EVERYTHING!****

import pandas as pd
import scipy.stats
from matplotlib import pyplot as plt

# Read in just the columns from the csv file that you'll need:
path_name = "/Users/ilya/Projects/abstracts_project/data files/"
file_name = "all_data_merged_restructured.csv"

dat = pd.read_csv(path_name+file_name, usecols = ['first_auth_gender', 'second_auth_gender', 'third_auth_gender', 'last_auth_gender', 'year', 'auth_count'])

print dat.head()

# Define function to calculate chi square results given data in the format that
# will be produced below.
def chi_sq(year, df, gender_info = 'female'):
    """Takes a year and a dataframe that has two columns representing male
    authorships followed by 2 columns representing female authorships, and
    returns a tuple that's the chisquare value followed by the p value. """
    a = df.loc[year]
    print a
    male = a[[1,2]]
    female = a[[3,4]]
    print female
    if gender_info == 'male':
        return scipy.stats.chisquare( male )
    elif gender_info == 'female':
        return scipy.stats.chisquare( female )


#         *****************************************************
#                  ***Get started on the real goals!***

# Plot the number of papers with male and female first and third authors. Run a
# chi squared test on the within-sex difference and include results in plot.

# Get just the data for papers with at least 3 authors:
four_plus_auth = dat[dat.auth_count > 3][['year','first_auth_gender',
                                     'third_auth_gender']]

# Drop rows that have a male/female id in both columns:
drop_rows_with = ['unknown', 'mostly_female', 'mostly_male']
for x in drop_rows_with:
    four_plus_auth = four_plus_auth[four_plus_auth.first_auth_gender != x]
    four_plus_auth = four_plus_auth[four_plus_auth.third_auth_gender != x]

# Get counts of male/female first/third for each year:
years = range(1970,2015)
counts_four_plus = pd.DataFrame(columns = ['year', 'male_first', 'male_third', 'female_first', 'female_third'])
for y in years:
    temp = four_plus_auth[four_plus_auth.year == y]
    male_first = (temp.first_auth_gender == 'male').sum()
    male_third = (temp.third_auth_gender == 'male').sum()
    female_first = (temp.first_auth_gender == 'female').sum()
    female_third = (temp.third_auth_gender == 'female').sum()
    counts_four_plus.loc[y] = [y, male_first, male_third, female_first, female_third]

plt.style.use('ggplot')

to_plot = counts_four_plus.iloc[:-1,1:]
to_plot.plot(kind = 'line')
plt.title('Counts of four plus author papers with female first authors and with \nfemale third authors. Significance of chi square test under x axis.')
plt.axis([1970, 2014, -50,800])
for y in years[:-1]:
    if chi_sq(y, counts_four_plus)[1] < .05:
        plt.annotate('**', xy = (y, -20), rotation = 45, color = 'green')
    elif chi_sq(y, counts_four_plus)[1] < .1:
        plt.annotate('*', xy = (y, -20), rotation = 45, color = 'green')
    # else:
    #     plt.annotate('o', xy = (y, -20))
    if chi_sq(y, counts_four_plus, gender_info = 'male')[1] < .05:
        plt.annotate('**', xy = (y, -40), rotation = 45, color = 'red')
    elif chi_sq(y, counts_four_plus, gender_info = 'male')[1] < .1:
        plt.annotate('*', xy = (y, -40), rotation = 45, color = 'red')
    # else:
    #     plt.annotate('o', xy = (y, -40))

plt.show()




#      ***Repeat the above analysis, but for 2-author papers only***

# Get just the data for papers with 2 authors:
two_auth = dat[dat.auth_count == 2][['year','first_auth_gender',
                                     'second_auth_gender']]

# Drop rows that have a male/female id in both columns:
drop_rows_with = ['unknown', 'mostly_female', 'mostly_male']
for x in drop_rows_with:
    two_auth = two_auth[two_auth.first_auth_gender != x]
    two_auth = two_auth[two_auth.second_auth_gender != x]

# Get counts of male/female first/second for each year:
years = range(1950,2015)
counts = pd.DataFrame(columns = ['year', 'male_first', 'male_second', 'female_first', 'female_second'])
for y in years:
    temp = two_auth[two_auth.year == y]
    male_first = (temp.first_auth_gender == 'male').sum()
    male_second = (temp.second_auth_gender == 'male').sum()
    female_first = (temp.first_auth_gender == 'female').sum()
    female_second = (temp.second_auth_gender == 'female').sum()
    counts.loc[y] = [y, male_first, male_second, female_first, female_second]

to_plot = counts.iloc[:-1,3:]
to_plot.plot(kind = 'line')
plt.title('Counts of two author papers with female first \nauthors and with female second authors')
for y in years:
    if chi_sq(y, counts)[1] < .05:
        plt.annotate('x', xy = (y, 100))
    else:
        plt.annotate('o', xy = (y, 100))

plt.show()



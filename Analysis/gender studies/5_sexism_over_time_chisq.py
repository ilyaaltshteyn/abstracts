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
        print scipy.stats.chisquare( male )
        return scipy.stats.chisquare( male )
    elif gender_info == 'female':
        print scipy.stats.chisquare( female )
        return scipy.stats.chisquare( female )


#         *****************************************************
#                  ***Get started on the real goals!***

# Plot the number of papers with male and female first and third authors. Run a
# chi squared test on the within-sex difference and include results in plot.

# Get just the data for papers with at least 4 authors:
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
plt.title('Counts of papers that have at least 4 authors, with first and third author\ngender. Significance of chi square test under x axis.')
plt.axis([1970, 2013, -50,800])
for y in years[:-1]:
    print y
    if chi_sq(y, counts_four_plus)[1] < .01:
        plt.annotate('**', xy = (y, -20), rotation = 45, color = 'green')
    elif chi_sq(y, counts_four_plus)[1] < .05:
        plt.annotate('*', xy = (y, -20), rotation = 45, color = 'green')
    # else:
    #     plt.annotate('o', xy = (y, -20))
    if chi_sq(y, counts_four_plus, gender_info = 'male')[1] < .01:
        plt.annotate('**', xy = (y, -40), rotation = 45, color = 'red')
    elif chi_sq(y, counts_four_plus, gender_info = 'male')[1] < .05:
        plt.annotate('*', xy = (y, -40), rotation = 45, color = 'red')
    # else:
    #     plt.annotate('o', xy = (y, -40))

plt.show()

#       Plot the percent of papers with female first and third authors:

counts_four_plus['total'] = counts_four_plus.male_first + counts_four_plus.male_third \
    + counts_four_plus.female_first + counts_four_plus.female_third

counts_four_plus['Percent_female_first'] = counts_four_plus.female_first/counts_four_plus.total
counts_four_plus['Percent_female_third'] = counts_four_plus.female_third/counts_four_plus.total

to_plot = counts_four_plus.iloc[:-1, 1:]
to_plot.plot(kind = 'line')
plt.title('Percent of papers with at least 4 authors that have a\n female first author or a female third author.')
plt.show()

#   Now plot just the difference between the percent of papers with female first
# and third authors, across time:

to_plot['percent_difference'] = to_plot.Percent_female_third - to_plot.Percent_female_first
to_plot['year'] = to_plot.index
to_plot.plot(kind = 'scatter', x = 'year', y = 'percent_difference')
plt.title('Difference between the % of papers with a female first author \n\
and the percent of papers with a female third author, by year.')
plt.show()

#  Now do a similar thing: plot the ratio of the count of papers with a female
# first author and a female third author, by year.
to_plot = counts_four_plus.iloc[:-1, 3:-3]
to_plot['year'] = to_plot.index
to_plot['ratio'] = to_plot.female_first / to_plot.female_third
to_plot.plot(kind = 'scatter', x = 'year', y = 'ratio')
plt.title('Ratio of the number of papers with female first authors to\nnumber of papers with female first authors, by year.')
plt.ylabel('Number of first author women/number of third author women')
plt.axis([1968, 2015,0,1.3])
plt.show()

#  Now run a linear regression on the data to find out whether or not the ratio
# has changed over time.



#           THE MOST SENSICAL ANALYSIS HERE:

# This analysis looks at counts of first and second authors who are men and who
# are women, for papers with at least 3 authors. I call this "obscure authorship"
# because the first authorship is a coveted spot, the last authorship is often
# taken by the overseeing professor on the project, and the second authorship
# is more obscure than the first.

# Get just the data for papers with at least 3 authors:
three_plus_auth = dat[dat.auth_count > 2][['year','first_auth_gender',
                                     'second_auth_gender']]

# Drop rows that have a male/female id in both columns:
drop_rows_with = ['unknown', 'mostly_female', 'mostly_male']
for x in drop_rows_with:
    three_plus_auth = three_plus_auth[three_plus_auth.first_auth_gender != x]
    three_plus_auth = three_plus_auth[three_plus_auth.second_auth_gender != x]

# Get counts of male/female first/third for each year:
years = range(1970,2015)
counts_three_plus = pd.DataFrame(columns = ['year', 'male_first', 'male_second', 'female_first', 'female_second'])
for y in years:
    temp = three_plus_auth[three_plus_auth.year == y]
    male_first = (temp.first_auth_gender == 'male').sum()
    male_second = (temp.second_auth_gender == 'male').sum()
    female_first = (temp.first_auth_gender == 'female').sum()
    female_second = (temp.second_auth_gender == 'female').sum()
    counts_three_plus.loc[y] = [y, male_first, male_second, female_first, female_second]

plt.style.use('ggplot')

to_plot = counts_three_plus.iloc[:-1,1:]
to_plot.plot(kind = 'line')
plt.title('Counts of papers that have at least 3 authors, with first and second author\ngender. Significance of chi square test under x axis.')
plt.axis([1970, 2013, -50,1200])
for y in years[:-1]:
    print y
    if chi_sq(y, counts_three_plus)[1] < .01:
        plt.annotate('**', xy = (y, -20), rotation = 45, color = 'green')
    elif chi_sq(y, counts_three_plus)[1] < .05:
        plt.annotate('*', xy = (y, -20), rotation = 45, color = 'green')
    # else:
    #     plt.annotate('o', xy = (y, -20))
    if chi_sq(y, counts_three_plus, gender_info = 'male')[1] < .01:
        plt.annotate('**', xy = (y, -40), rotation = 45, color = 'red')
    elif chi_sq(y, counts_three_plus, gender_info = 'male')[1] < .05:
        plt.annotate('*', xy = (y, -40), rotation = 45, color = 'red')
    # else:
    #     plt.annotate('o', xy = (y, -40))

plt.show()








# Everything below is just extra, more fine-grained stuff.













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



#             ***Now do it for 3-person papers only***
# So you're looking at papers with exactly 3 authors to see whether or not women
# are more likely to be in the first authorship spot than in the second one.

# Get just the data for papers with 3 authors:
three_auth = dat[dat.auth_count == 3][['year','first_auth_gender',
                                     'second_auth_gender']]

# Drop rows that have a male/female id in both columns:
drop_rows_with = ['unknown', 'mostly_female', 'mostly_male']
for x in drop_rows_with:
    three_auth = three_auth[three_auth.first_auth_gender != x]
    three_auth = three_auth[three_auth.second_auth_gender != x]

# Get counts of male/female first/second for each year:
years = range(1950,2015)
counts = pd.DataFrame(columns = ['year', 'male_first', 'male_second', 'female_first', 'female_second'])
for y in years:
    temp = three_auth[three_auth.year == y]
    male_first = (temp.first_auth_gender == 'male').sum()
    male_second = (temp.second_auth_gender == 'male').sum()
    female_first = (temp.first_auth_gender == 'female').sum()
    female_second = (temp.second_auth_gender == 'female').sum()
    counts.loc[y] = [y, male_first, male_second, female_first, female_second]

to_plot = counts.iloc[:-1,3:]
to_plot.plot(kind = 'line')
plt.title('Counts of three author papers with female first \nauthors and with female second authors')
for y in years:
    if chi_sq(y, counts)[1] < .05:
        plt.annotate('x', xy = (y, 100))
    else:
        plt.annotate('o', xy = (y, 100))

plt.show()


#This script pulls citation count info from the CrossRef API

import urllib2, BeautifulSoup, os, csv, errno, signal
from BeautifulSoup import BeautifulSoup
import pandas as pd
from pandas import read_csv
#I think the wraps import is for the timeout function below.
from functools import wraps

#Create a function that times out whatever function it's applied to:
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

#Apply timeout function to the doi_to_info function defined below,
#because it accesses the API and could get stuck.
@timeout()
def doi_to_info(doi):
    """This function accepts a doi as input and uses the Crossref
    OpenURL API to retrieve XML info about the article. It parses
    the XML and spits out an editor's name if there is one (or
    "No_editor_info" if there isn't one listed), and also spits
    out the citation count for the paper."""

    url = 'http://www.crossref.org/openurl/?pid=' + pid + '&id=doi:' + doi + '&noredirect=true'
    response = urllib2.urlopen(url)
    xml = response.read()
    soup = BeautifulSoup(xml)

    #From the 'query' tag, retrieve the citation count:
    try:
        citation_count = soup.query['fl_count']
    except:
        citation_count = 'not_found'
    #From the contributor tag, retrieve the editor's name if it's listed:
    try:
        editor_name = soup('contributor', attrs = {'contributor_role' : 'editor'})[0].given_name.string
    except:
        editor_name = 'not_found'
    try:
        editor_surname = soup('contributor', attrs = {'contributor_role' : 'editor'})[0].surname.string
    except:
        editor_surname = 'not_found'

    return str(citation_count), str(editor_name), str(editor_surname)


#Define the pid so that doi_to_info has what it needs:
pid = 'ilyaaltshteyn@gmail.com'

#Make a list of the files that have abstracts with DOIs in them:
abstracts_dir = '/Users/ilya/Documents/Abstracts project/Scraping tools/PsycNet abstracts/'
abstracts_files = os.listdir(abstracts_dir)

for f in abstracts_files[30:]:
    #Read the abstracts file into a dataframe called df:
    file = abstracts_dir + f
    df = read_csv(file)
    file_length = len(df.index)

    #Add new columns and fill with the word 'untouched', to be replaced
    #when the script touches that row and uses the API for its DOI:
    df['citation_count'] = pd.Series('untouched', index = df.index)
    df['editor_name'] = pd.Series('untouched', index = df.index)
    df['editor_surname'] = pd.Series('untouched', index = df.index)

    #Pull info using doi_to_info for each abstract in the file:
    for row in df.index:
        doi = df['doi'].loc[row]
        try:
            info = doi_to_info(doi)
            df['citation_count'].loc[row] = info[0]
            df['editor_name'].loc[row] = info[1]
            df['editor_surname'].loc[row] = info[2]
            print 'Just finished row ' + str(row) + ' out of ' + str(file_length) + ' rows in file ' + f
        except:
            df['citation_count'].loc[row] = 'PULL_ERROR'
            df['editor_name'].loc[row] = 'PULL_ERROR'
            df['editor_surname'].loc[row] = 'PULL_ERROR'          
            continue
    #Print the file into a new csv file, in another directory:
    output_loc = '/Users/ilya/Documents/Abstracts project/Scraping tools/abstracts with citation counts/'
    df.to_csv(path_or_buf = (output_loc + 'with cites ' + f), encoding = "utf-8")


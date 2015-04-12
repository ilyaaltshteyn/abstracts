#This script pulls the urls from the files in the "PsycNET article urls"
#folder and pulls abstract info from each url. 
import os, csv, urllib2, cookielib, random, time
import pandas as pd
from urllib2 import Request
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup, SoupStrainer

#List files in the folder:
urls_dir = "/Users/ilya/Documents/Abstracts project/Scraping tools/PsycNet article urls/"
files = os.listdir(urls_dir)


#Create custom tag stripper to avoid problems caused by italics formatting tags:
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#Create a function that ends the current loop when it's taking too long. 
#This is useful for if the server returns something unusual that makes a 
#loop infinite for some reason, or if the server goes into some weird
#extended lag, or if the internet cuts out and then cuts back in again
#(which could cause unexpected script behavior).
from functools import wraps
import errno, os, signal
class TimeoutError(Exception):
    pass

def timeout(seconds = 10, error_message = os.strerror(errno.ETIME)):
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

#Create cookie sender, which will prevent the PsycNET site from returning
#an infinite loop instead of html.
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#Create function that pulls html into a pack of html called soup:
@timeout()
def soup_puller(url):
	"""This code pulls the contents of the html page with the abstract on it.
	Uses cookie sender (created above) to send cookies to the page, so that 
	it won't return an infinite loop."""
	request = urllib2.Request(url)
	response = opener.open(request)
	html = response.read()
	soup = BeautifulSoup(html)

	return soup

#Calculate total rows in file, to have a total % done display:
total_urls = 0
for f in files[28:]:
	loc = urls_dir + f
	u = open(loc, 'r')
	openu = csv.reader(u)
	articles = list()
	for row in openu:
		articles.append(row)
	total_urls += len(articles[0])

#Iterate over the files in the folder, putting their urls into a list called
#articles and then pulling info for each article in articles.
urls_finished = 0
for f in files[28:]:
	#Create library for the file being worked on:
	abstracts_lib = pd.DataFrame(columns = ['abstract', 'journal', 'publisher', 
		'authors', 'title', 'date', 'journal_vol', 'journal_issue', 'firstpage', 'doi', 
		'abstract_html', 'fulltext_html', 'pdf_url', 'language', 'keywords'])
	#Pull urls from file into a list called articles:
	loc = urls_dir + f
	u = open(loc, 'r')
	openu = csv.reader(u)
	articles = list()
	for row in openu:
		articles.append(row)

#	print 'The number of articles in this list is: ' + str(len(articles[0]))
	
	count = 0
	for article in articles[0]:
		count += 1
		url = article

		try:
			soup = soup_puller(url)
		except:
			continue

		#This outputs a BeautifulSoup tag, converts it to string, strips 
		#tags using custom stripper defined at the beginning:
		try:
			abstract = soup.find('li', attrs = {'class' : "rdAbstract"})
			abstract = strip_tags(str(abstract))
			#This removes the useless metainfo about PsycINFO database record:
			if abstract[-61:] == ' (PsycINFO Database Record (c) 2012 APA, all rights reserved)':
				abstract = abstract[:-61]
		except:
			abstract = "PULL_ERROR"

		#This grabs metainfo from within the metainfo tags:
		try:
			journal = soup.find('meta', attrs = {'name' : "citation_journal_title"}).get('content')
		except:
			journal = "PULL_ERROR"
		try:
			publisher = soup.find('meta', attrs = {'name' : "citation_publisher"}).get('content')
		except:
			publisher = "PULL_ERROR"
		try:
			authors = soup.find('meta', attrs = {'name' : "citation_authors"}).get('content')
		except:
			authors = "PULL_ERROR"
		try:
			title = soup.find('meta', attrs = {'name' : "citation_title"}).get('content')
		except:
			title = "PULL_ERROR"
		try:
			date = soup.find('meta', attrs = {'name' : "citation_date"}).get('content')
		except:
			date = "PULL_ERROR"
		try:
			journal_vol = soup.find('meta', attrs = {'name' : "citation_volume"}).get('content')
		except:
			journal_vol = "PULL_ERROR"
		try:
			journal_issue = soup.find('meta', attrs = {'name' : "citation_issue"}).get('content')
		except:
			journal_issue = "PULL_ERROR"
		try:
			firstpage = soup.find('meta', attrs = {'name' : "citation_firstpage"}).get('content')
		except:
			firstpage = "PULL_ERROR"
		try:
			doi = soup.find('meta', attrs = {'name' : "citation_doi"}).get('content')
		except:
			doi = "PULL_ERROR"
		try:
			abstract_html = soup.find('meta', attrs = {'name' : "citation_abstract_html_url"}).get('content')
		except:
			abstract_html = "PULL_ERROR"
		try:
			fulltext_html = soup.find('meta', attrs = {'name' : "citation_fulltext_html_url"}).get('content')
		except:
			fulltext_html = "PULL_ERROR"
		try:
			pdf_url = soup.find('meta', attrs = {'name' : "citation_pdf_url"}).get('content')
		except:
			pdf_url = "PULL_ERROR"
		try:
			language = soup.find('meta', attrs = {'name' : "citation_language"}).get('content')
		except:
			language = "PULL_ERROR"
		try:
			keywords = soup.find('meta', attrs = {'name' : "citation_keywords"}).get('content')
		except:
			keywords = "PULL_ERROR"

		#Creates dictionary containing all info:
		all_info = {'abstract' : abstract, 'journal' : journal, 'publisher' : publisher, 'authors' : authors, 
			'title' : title, 'date' : date, 'journal_vol' : journal_vol, 
			'journal_issue' : journal_issue, 'firstpage' : firstpage, 'doi' : doi, 'abstract_html' : abstract_html, 
			'fulltext_html' : fulltext_html, 'pdf_url' : pdf_url,
			'language' : language, 'keywords' : keywords}

		#Adds a random pause, between .05 and 3 seconds (with a mode of .5 seconds)
		#to the loop, to not overload the PsycNet server. So the pause happens
		#after each abstract pull.
		sleeptime = random.triangular(.05,3,.75)
		time.sleep(sleeptime)

		urls_finished += 1

		print ('Working on url ' + str(count) + ' out of ' + str(len(articles[0])) + 
			' in file "' + f + '" | Slept for ' + str(round(sleeptime,2)) + ' secs | ' +  
			str(round((float(urls_finished)/float(total_urls))*100, 2)) + '% of a total ' + 
			str(total_urls) + ' urls done')

		abstracts_lib = abstracts_lib.append(all_info, ignore_index = True)

	#Write the urls to a journal-specific csv file:
	fileloc = '/Users/ilya/Documents/Abstracts project/Scraping tools/PsycNet abstracts/'
	filename = f[0:3] + ' ' + str(len(articles[0])) + '.csv'

	abstracts_lib.to_csv(path_or_buf = (fileloc + filename), encoding = "utf-8")


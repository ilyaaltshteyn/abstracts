#This code pulls the url for all abstracts from a given journal/volume/issue.
#Then it goes to each url and pulls the abstract and other info from it.

#Create some stuff that will be useful throughout the script:
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re, urllib2, cookielib, bleach, time, random
from urllib2 import Request

#Cookie sender:
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#Abstracts library:
abstracts_lib = dict()

#--------	Pull list of article urls

#Define which journal, volume, issue you're looking through:
journal = 'amp'
volume = '1'
issue = '1'

#Compile url where the abstract urls will be pulled from:
url = 'http://psycnet.apa.org/journals/' + journal + '/' + volume + '/' + issue + '/'

#Pull sourcecode from the url:
#Also send cookies to the page using the cookie sender created at the beginning, 
#so that it won't return an infinite loop.
#Returning an infinite loop is probably psycnet's protection against scraping?
request = urllib2.Request(url)
response = opener.open(request)
html = response.read()
soup = BeautifulSoup(html)

#This outputs a BeautifulSoup ResultSet object (iterable) with urls for the
#given journal/volume/issue:
urls = soup.fetch('div', attrs = {'class' : "bwaazTitle"})

#This pulls the article urls from the ResultSet object above and put into list 'articles':
articles = list()

for x in urls:
	suffix = x.a['href']
	article_url = 'http://psycnet.apa.org' + suffix
	articles.append(article_url)


#--------	Now pull the abstracts from the urls.

#Iterate through the list of articles and pull the abstract for each one.
#Add a random-length pause to not overload their system when scaling up.

for article in articles:
	#This code pulls the contents of the html page with the abstract on it.
	#Again, uses cookie sender created at the beginning to send cookies to the 
	#page, so that it won't return an infinite loop.
	url = article
	request = urllib2.Request(url)
	response = opener.open(request)
	html = response.read()
	soup = BeautifulSoup(html)

	#This outputs a BeautifulSoup ResultSet object
	abstract = soup.fetch('li', attrs = {'class' : "rdAbstract"})

	#This turns the ResultSet object into a string
	abstract = unicode.join(u'\n',map(unicode,abstract))

	#This uses the bleach module to strip html tags from the string
	final_abstract = bleach.clean(abstract, tags=[], strip=True)

	#This removes the useless metainfo about PsycINFO database record:
	if final_abstract[-61:] == ' (PsycINFO Database Record (c) 2012 APA, all rights reserved)':
		final_abstract = final_abstract[:-61]

	sleeptime = random.triangular(1,10,1)
	time.sleep(sleeptime)
	
	 final_abstract





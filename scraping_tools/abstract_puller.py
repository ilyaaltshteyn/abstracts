#This code pulls abstract out of this url: http://psycnet.apa.org/journals/amp/1/1/3/

from BeautifulSoup import BeautifulSoup
import re, urllib2, cookielib, bleach
from urllib2 import Request

#This code pulls the contents of the html page with the abstract on it.
#It also sends cookies to the page, so that it won't return an infinite loop.
#Returning an infinite loop is probably psycnet's protection against scraping?
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
url = "http://psycnet.apa.org/journals/amp/1/1/3/"
request = urllib2.Request(url)
response = opener.open(request)
html = response.read()
soup = BeautifulSoup(html)

#***PULL ABSTRACT:
#This outputs a BeautifulSoup ResultSet object
abstract = soup.find('li', attrs = {'class' : "rdAbstract"})
final_abstract = abstract.next

#***PULL OTHER ARTICLE INFO:
journal = soup.find('meta', attrs = {'name' : "citation_journal_title"})
journal = journal.get('content')
publisher = soup.find('meta', attrs = {'name' : "citation_publisher"})
publisher = publisher.get('content')
authors = soup.find('meta', attrs = {'name' : "citation_authors"})
authors = authors.get('content')
title = soup.find('meta', attrs = {'name' : "citation_title"})
title = title.get('content')
date = soup.find('meta', attrs = {'name' : "citation_date"})
date = date.get('content')
journal_vol = soup.find('meta', attrs = {'name' : "citation_volume"})
journal_vol = journal_vol.get('content')
journal_issue = soup.find('meta', attrs = {'name' : "citation_issue"})
journal_issue = journal_issue.get('content')
firstpage = soup.find('meta', attrs = {'name' : "citation_firstpage"})
firstpage = firstpage.get('content')
doi = soup.find('meta', attrs = {'name' : "citation_doi"})
doi = doi.get('content')
abstract_html = soup.find('meta', attrs = {'name' : "citation_abstract_html_url"})
abstract_html = abstract_html.get('content')
fulltext_html = soup.find('meta', attrs = {'name' : "citation_fulltext_html_url"})
fulltext_html = fulltext_html.get('content')
pdf_url = soup.find('meta', attrs = {'name' : "citation_pdf_url"})
pdf_url = pdf_url.get('content')
language = soup.find('meta', attrs = {'name' : "citation_language"})
language = language.get('content')
keywords = soup.find('meta', attrs = {'name' : "citation_keywords"})
keywords = keywords.get('content')



#This code pulls the url for all abstracts from a given journal/volume/issue.
#Then it goes to each url and pulls the abstract and other info from it.

#Create some stuff that will be useful throughout the script:
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re, urllib2, cookielib, bleach, time, random, csv
from urllib2 import Request

#Cookie sender:
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#Abstracts library:
abstracts_lib = list()

#--------	Pull list of article urls
#Count number of volumes for a given journal, then cycle through the issues
#in each volume and collect the urls for that issue. Put the urls into a
#list called article_urls

#Make function that counts volumes:
def volume_counter(journal_name):
	"""This function counts how many volumes a given journal has
	on PsycNet and returns the number of volumes. It also returns
	the smallest volume number, which is not always one."""

	url = 'http://psycnet.apa.org/journals/' + journal_name + '/'
	request = urllib2.Request(url)
	response = opener.open(request)
	html = response.read()
	soup = BeautifulSoup(html)

	vols = soup.findAll('ol', attrs = {'class' : "bwaVolumes"})
	volume_count = len(vols)

	#Get the biggest volume number:
	biggest_volume = vols[1]('a')
	biggest_volume = bleach.clean(biggest_volume, strip = True)
	#Strip everything but the volume number from that tag:
	tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
	bv = tag_re.sub('', biggest_volume)
	bv = re.sub(r'[\n\t+"Volume"+" "+\[+\]]','',bv)
	bv = int(bv)

	#Get the smallest volume number (add 2 bc you're not counting 2014 volume):
	smallest_volume = bv - volume_count + 2

	return volume_count, smallest_volume


#Make function that pulls urls:
def article_urls(journal, volume, issue):
	"""This function compiles a list of article urls for a given
	volume and issue of a given journal. The volume and issue
	should be supplied to the function as strings, not numbers.
	The journal should be supplied as the PsycNet 3-letter code.
	The function will return none if there are no urls (e.g. when
	there is no such issue number."""

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

	#This makes the function return None if there are no urls.
	if urls == []:
		return None

	else:
		#This pulls the article urls from the ResultSet object above and 
		#puts them into the list 'articles':
		articles = list()

		for x in urls:
			suffix = x.a['href']
			article_url = 'http://psycnet.apa.org' + suffix
			articles.append(str(article_url))

		return articles

#Get the volume count and the starting volume number for a given journal:
already_run = ['ort', 'amp', 'aap', 'apf', 'bdb', 'bne', 'cbs', 'cep', 'cpp', 'cpb', 'cfp', 'cri', 'cdp']

#Problem journals: ['cap']

journals_list = ['dec', 'dev', 'drm', 'emo', 'jpa', 'epp',
	'ebs', 'pha', 'zea', 'fsh', 'gro', 'gdn', 'hea', 'hop', 'bct', 'pla', 'str',
	'ipp', 'abn', 'jab', 'apl', 'bah', 'aic', 'bhm', 'com', 'ccp', 'cou', 'dhe']

journals_list2 = ['eib', 'edu', 'xan', 'xap', 'xge', 'xhp', 'xlm', 'fam', 'jid', 'lat', 'jmp',
	'npe', 'ocp', 'psp', 'prs', 'jop', 'int', 'rmh', 'teo', 'tam', 'lhb', 'med',
	'mil', 'mot', 'neu', 'nop', 'pac', 'per', 'pre', 'pro', 'prj', 'pap', 'psb',
	'pas', 'bul', 'met', 'mon', 'rev', 'ser', 'tra', 'pag', 'adb', 'aca']

journals_list3 = ['cns', 'men', 'ppm', 'rel', 'sgd', 'vio', 'law', 'pmu', 'pst',
	'qua', 'rep', 'gpr', 'ror', 'szb', 'stl', 'spq', 'zsp', 'scp', 'spy', 'sjp', 
	'bov', 'slp', 'mgr', 'tep', 'tps', 'trm', 'zfp']

for j in journals_list:
	journal = j
	try:
		volumes = volume_counter(journal)

		#Make list that all urls for this journal will be in:
		all_urls = list()

		#Apply article_urls function up to issue 12 of each volume.
		#This returns a list of urls of articles in UP TO issue 12 of whatever journal is inputted:
		for x in range(volumes[0]):
			for issue in range(1,13):
				print "Looking @ journal " + journal + ", vol " + str(x) + ", issue " + str(issue) + ". Total vols in this journal: " + str(volumes[0])
				#Adjust volume number to correct for the smallest volume number the journal has:
				vol_number = x + volumes[1] - 1
				urls_pulled = article_urls(journal, str(vol_number), str(issue))
				if urls_pulled == None:
					break
				else:
					all_urls.append(urls_pulled)
					sleeptime = random.triangular(1,6,1.1)
					time.sleep(sleeptime)

		unlisted_urls = [item for sublist in all_urls for item in sublist]

		#Write the urls to a journal-specific csv file:
		fileloc = '/Users/ilya/Documents/Abstracts project/Scraping tools/PsycNet article urls/'
		filename = journal + '.csv'
		with open(fileloc + filename, 'wb') as f:
			wr = csv.writer(f, dialect = 'excel')
			wr.writerow(unlisted_urls)
	except:
		pass

for j in journals_list2:
	journal = j
	try:
		volumes = volume_counter(journal)

		#Make list that all urls for this journal will be in:
		all_urls = list()

		#Apply article_urls function up to issue 12 of each volume.
		#This returns a list of urls of articles in UP TO issue 12 of whatever journal is inputted:
		for x in range(volumes[0]):
			for issue in range(1,13):
				print "Looking @ journal " + journal + ", vol " + str(x) + ", issue " + str(issue) + ". Total vols in this journal: " + str(volumes[0])
				#Adjust volume number to correct for the smallest volume number the journal has:
				vol_number = x + volumes[1] - 1
				urls_pulled = article_urls(journal, str(vol_number), str(issue))
				if urls_pulled == None:
					break
				else:
					all_urls.append(urls_pulled)
					sleeptime = random.triangular(1,5,1.1)
					time.sleep(sleeptime)

		unlisted_urls = [item for sublist in all_urls for item in sublist]

		#Write the urls to a journal-specific csv file:
		fileloc = '/Users/ilya/Documents/Abstracts project/Scraping tools/PsycNet article urls/'
		filename = journal + '.csv'
		with open(fileloc + filename, 'wb') as f:
			wr = csv.writer(f, dialect = 'excel')
			wr.writerow(unlisted_urls)
	except:
		pass

for j in journals_list3:
	journal = j
	try:
		volumes = volume_counter(journal)

		#Make list that all urls for this journal will be in:
		all_urls = list()

		#Apply article_urls function up to issue 12 of each volume.
		#This returns a list of urls of articles in UP TO issue 12 of whatever journal is inputted:
		for x in range(volumes[0]):
			for issue in range(1,13):
				print "Looking @ journal " + journal + ", vol " + str(x) + ", issue " + str(issue) + ". Total vols in this journal: " + str(volumes[0])
				#Adjust volume number to correct for the smallest volume number the journal has:
				vol_number = x + volumes[1] - 1
				urls_pulled = article_urls(journal, str(vol_number), str(issue))
				if urls_pulled == None:
					break
				else:
					all_urls.append(urls_pulled)
					sleeptime = random.triangular(1,4,1.1)
					time.sleep(sleeptime)

		unlisted_urls = [item for sublist in all_urls for item in sublist]

		#Write the urls to a journal-specific csv file:
		fileloc = '/Users/ilya/Documents/Abstracts project/Scraping tools/PsycNet article urls/'
		filename = journal + '.csv'
		with open(fileloc + filename, 'wb') as f:
			wr = csv.writer(f, dialect = 'excel')
			wr.writerow(unlisted_urls)
	except:
		pass






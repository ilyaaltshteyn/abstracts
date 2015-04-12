#This script flips through all of the volumes and issues of the amp journal.
#URL for the journal on PsycNet: http://psycnet.apa.org/journals/amp/

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



#coding:utf-8
import sys
import BeautifulSoup
import urllib2
import re
from datetime import datetime

BASE_URL = "http://plaza.rakuten.co.jp/"
IMAGE_URL = "http://image.space.rakuten.co.jp"

argvs = sys.argv
if len(argvs) == 2:
	st_link_filename = argvs[1]
else:
	sys.exit()

target_url = []
fh_link = open(st_link_filename,'r')
for line in fh_link:
	target_url.append(line.rstrip().split('\t')[1])
fh_link.close()
print str(target_url)
	
# title
def get_title(soup):
	return str(soup.find("h2").find("a").string)

# datetime
def get_datetime(soup):
	st_date = str(soup.find("div",align="right")).rsplit("\n")[2].strip()
	dt_date = datetime.strptime(st_date, "%B %d, %Y %I:%M:%S %p")
	return dt_date.strftime("%Y-%m-%d %H:%m:%S")

# content & strip html tags
def get_content(soup):
	for st_contents in soup.findAll(attrs={"class":"dText break-word"}):
		st_contents = str(st_contents)
		st_contents = re.sub(r'<div class=\"dText break-word\">',"",st_contents)
		st_contents = re.sub(r'</div>',"",st_contents)
		st_contents = re.sub(r'\r\n','\n',st_contents)
		return re.sub(r'<br />',"",st_contents)

# link to past content
def get_past_link(soup):
	return str(soup.find("li",{"class":"sideNext"}).find("a",href=True)['href'])

# link to images
def get_link_image(soup):
	image_links=[]
	for st_link_image in soup.find(attrs={"class":"dText break-word"}).findAll("img",src=True):
		if IMAGE_URL in st_link_image['src']:
			image_links.append(st_link_image['src'])
#		print st_link_image['src']
	return image_links

opener = urllib2.build_opener()
while True:
	try:
		soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(target_url.pop(0)).read())

		print "----------"
		print "title\t:" + get_title(soup)
		print "datetime\t:" + get_datetime(soup)
		print "content\t:\n" + get_content(soup)
		for i in get_link_image(soup):
			print "link to images\t:" + i
		st_link = get_past_link(soup)

#		print "link to past content\t:" + st_link
	except:
		print "except..."
		sys.exit()

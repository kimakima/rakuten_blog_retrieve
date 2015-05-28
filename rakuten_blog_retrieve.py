#coding:utf-8
import sys
import BeautifulSoup
import urllib2
import re

url_base = "http://plaza.rakuten.co.jp/"

ini_file = open('rakuten_blog_retrieve.ini','r')
for line in ini_file:
	url_blog = line
ini_file.close()

argvs = sys.argv
if len(argvs) == 2:
	url_origin = url_base + argvs[1]
else:
	url_origin = url_base + url_blog
	
print url_origin

opener = urllib2.build_opener()
soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url_origin).read())

# title
print str(soup.find("h2").find("a").string)

# datetime
print str(soup.find("div",align="right")).rsplit("\n")[2].strip()
	
# content & strip html tags
for st_contents in soup.findAll(attrs={"class":"dText break-word"}):
	print re.sub(r'<br />',"",str(st_contents))

for st_link_image in soup.find(attrs={"class":"dText break-word"}).findAll("img",src=True):
	print "link to image\t:" + st_link_image['src']

# link to past content
def get_past_link(soup):
	for st_past_link in soup.findAll(attrs={"class":"main_title"}):
		if "過去" in str(st_past_link):
			st_past_link = url_base + st_past_link.find("a",href=True)['href']
	return str(st_past_link)

print "link to past content\t:" + get_past_link(soup)



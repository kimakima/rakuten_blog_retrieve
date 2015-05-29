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
def get_title(soup):
	return str(soup.find("h2").find("a").string)

# datetime
def get_datetime(soup):
	return str(soup.find("div",align="right")).rsplit("\n")[2].strip()

# content & strip html tags
def get_content(soup):
	for st_contents in soup.findAll(attrs={"class":"dText break-word"}):
		return re.sub(r'<br />',"",str(st_contents))

# link to past content
def get_past_link(soup):
	return = str(soup.find("li",{"class":"sideNext"}).find("a",href=True)['href'])

# link to images
def get_link_image(soup):
	image_links=[]
	for st_link_image in soup.find(attrs={"class":"dText break-word"}).findAll("img",src=True):
		image_links.append(st_link_image['src'])
		print st_link_image['src']
	return image_links

print "title\t:" + get_title(soup)
print "datetime\t:" + get_datetime(soup)
print "content\t:\n" + get_content(soup)
for i in get_link_image(soup):
	print "link to images\t:" + i
print "link to past content\t:" + get_past_link(soup)

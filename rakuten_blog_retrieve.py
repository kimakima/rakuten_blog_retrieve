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

class BlogBody:
	def __init__(self):
		self.target_url = []
		opener = urllib2.build_opener()

	def read_link_file(self, st_link_filename):
		fh_link = open(st_link_filename,'r')
		for line in fh_link:
			self.target_url.append(line.rstrip().split('\t')[1])
		fh_link.close()
		print str(self.target_url)

	def retrieve_content_body(self):
		st_link_url = self.target_url.pop(0)
		self.soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(st_link_url).read())
	
	# title
	def get_title(self):
		return str(self.soup.find("h2").find("a").string)

	# datetime
	def get_datetime(self):
		st_date = str(self.soup.find("div",align="right")).rsplit("\n")[2].strip()
		dt_date = datetime.strptime(st_date, "%B %d, %Y %I:%M:%S %p")
		return dt_date.strftime("%Y-%m-%d %H:%m:%S")

	# content & strip html tags
	def get_content(self):
		for st_contents in self.soup.findAll(attrs={"class":"dText break-word"}):
			st_contents = str(st_contents)
			st_contents = re.sub(r'<div class=\"dText break-word\">',"",st_contents)
			st_contents = re.sub(r'</div>',"",st_contents)
			st_contents = re.sub(r'\r\n','\n',st_contents)
			return re.sub(r'<br />',"",st_contents)

	# link to past content
	def get_past_link(self):
		return str(self.soup.find("li",{"class":"sideNext"}).find("a",href=True)['href'])

	# link to images
	def get_link_image(self):
		image_links=[]
		for st_link_image in self.soup.find(attrs={"class":"dText break-word"}).findAll("img",src=True):
			if IMAGE_URL in st_link_image['src']:
				image_links.append(st_link_image['src'])
#		print st_link_image['src']
		return image_links

	def get_image_file(self, st_image_url):
		image_url = urllib2.urlopen(st_image_url)
		st_image_filename = st_image_url.split("/")[-1]
		image_file = open(st_image_filename,'wb')
		image_file.write(image_url.read())
		image_url.close()
		image_file.close()

blog_body = BlogBody()
blog_body.read_link_file(st_link_filename)

while True:
	try:
		print "----------"
		blog_body.retrieve_content_body()
		print "title\t:" + blog_body.get_title()
		print "datetime\t:" + blog_body.get_datetime()
		print "content\t:\n" + blog_body.get_content()
		for i in blog_body.get_link_image():
			print "link to images\t:" + i
			blog_body.get_image_file(i)
		st_link = blog_body.get_past_link()

#		print "link to past content\t:" + st_link
	except:
		print "except..."
		sys.exit()

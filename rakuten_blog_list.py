#coding:utf-8
import sys
from bs4 import BeautifulSoup
import urllib2
import re

#BASE_URL = "http://plaza.rakuten.co.jp/"
#IMAGE_URL = "http://image.space.rakuten.co.jp"

RAKUTEN_BLOG_NAME = "kimakimach"
DAIRYALL_URL = "http://plaza.rakuten.co.jp/" + RAKUTEN_BLOG_NAME + "/diaryall/"

st_link = DAIRYALL_URL

soup = BeautifulSoup(urllib2.urlopen(st_link).read())

for st_block in soup.find_all('li',class_="loListItem"):
	for st_title in st_block.find_all('h2',class_="diary_title"):
		print st_title.string
	for st_link in st_block.find_all('a'):
		print st_link.get('href')

li_pagers = []
for st_pager_area in soup.find_all('p',class_="pagerArea"):
	for st_pager in st_pager_area.find_all('a'):
		li_pagers.append(str(st_pager.get('href')))
print list(set(li_pagers))

#	st_title = st_link.find_all('h2',lass_="diary_title")

#for st_title in soup.find_all('h2',class_="loListTtl diary_title"):
#	print st_title

#coding:utf-8
import sys
from bs4 import BeautifulSoup
import urllib2
import re

#BASE_URL = "http://plaza.rakuten.co.jp/"
#IMAGE_URL = "http://image.space.rakuten.co.jp"

RAKUTEN_BLOG_NAME = "kimakimach"

class BlogList:
	def __init__(self,RAKUTEN_BLOG_NAME):
		self.st_link = "http://plaza.rakuten.co.jp/" + RAKUTEN_BLOG_NAME + "/diaryall/"
		
	def get_pager_link(self):
		soup = BeautifulSoup(urllib2.urlopen(self.st_link).read())

		li_pagers = []
		for st_pager_area in soup.find_all('p',class_="pagerArea"):
			for st_pager in st_pager_area.find_all('a'):
				li_pagers.append(str(st_pager.get('href')))
		li_pagers = list(set(li_pagers))
		# ベースのURLからPagerのListを取得してから、Listの先頭にベースのURLを追加することで、完全なPagerのListになる。
		li_pagers.insert(0, self.st_link)
		return li_pagers

	def get_titles(self,st_poped_link):
		soup = BeautifulSoup(urllib2.urlopen(st_poped_link).read())

		li_contents = []
		for st_block in soup.find_all('li',class_="loListItem"):
			li_data = []
			for st_title in st_block.find_all('h2',class_="diary_title"):
				li_data.append(st_title.string)
			for st_link in st_block.find_all('a'):
				li_data.append(st_link.get('href'))
			li_contents.append(li_data)
		return li_contents

blog_list = BlogList(RAKUTEN_BLOG_NAME)
li_pager_link = blog_list.get_pager_link()

while len(li_pager_link):
	li_contents = blog_list.get_titles(li_pager_link.pop(0))

	for i in li_contents:
		print i[0].encode('utf-8') + "\t" + i[1].encode('utf-8')

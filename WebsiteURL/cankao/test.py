# -*- coding:utf-8 -*-

# from urllib2 import urlopen   # python2.7
# from bs4 import BeautifulSoup #用于解析网页
#
#
# html = urlopen("https://www.douban.com/")
#
# bsObj = BeautifulSoup(html, 'html.parser')
# print bsObj
#
# t1 = bsObj.find_all('a')
# for t2 in t1:
#     t3 = t2.get('href')
#     print t3

# list1 = [1,2,3,4]
# print list1.pop()

from urllib import quote
url = "http://www.hikvisioneurope.com/portal/?dir=portal/Product Firmware 2018"
url = quote(url, 'utf-8')
print url
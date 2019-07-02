# -*- coding:utf-8 -*-

##输入链接文件URL.txt，输出链接特征文件url_features.csv

# with open("testurl.txt") as file:
#     for line in file:
#         print line

# ------------
# import csv
#
# feature = [["a", {"111":"1111","333":"3333"}],["b",{"444":"4444","666":"6666"}], ["c",{"777":"7777","999":"9999"}]]
#
# # 111,333
# # 1111,3333
# # 6666,4444
# # 7777,9999
#
# def resultwriter(feature):
#     flag=True
#     with open("output.csv",'wb') as file:
#         for item in feature:
#             w = csv.DictWriter(file, item[1].keys())
#             print w
#             if flag:
#                 w.writeheader()
#                 flag=False
#             w.writerow(item[1])
#         file.close()
#
# resultwriter(feature)

### ----------
# from urlparse import urlparse
# import re
# url = "https://www.baidu.com/zhhhah/zhsg.html"
# # obj=urlparse(url)
# # host=obj.netloc
# # path=obj.path
# # print url
# # print host
# # print path
#
# token_word=re.split('\W+',url)
# print token_word

# ------------
# import urllib2
#
# def getRemoteFileSize(url, proxy=None):
#     '''
#     通过content-length头获取远程文件大小
#     '''
#     opener = urllib2.build_opener()
#     if proxy:
#         if url.lower().startswith('https://'):
#             opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))
#         elif url.lower().startswith('http://'):
#             opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))
#         else:
#             opener.add_handler(urllib2.ProxyHandler({'ftp': proxy}))
#     try:
#         request = urllib2.Request(url)
#         request.get_method = lambda: 'HEAD'
#         response = opener.open(request)
#         response.read()
#     except Exception, e:
#         # 远程文件不存在
#         return 0
#     else:
#         getfileSize = dict(response.headers).get('content-length', 0)
#         filesize = round(float (getfileSize)/1048576, 2)
#
#         getContentType = dict(response.headers).get('content-type', 0)
#
#         return filesize, getContentType
#
# url = "http://www.draytek.com.cn/upFiles/vigor2120/firmware/Vigor2120_v3.8.1.1_CN.zip"
# url2 = "http://www.jcgcn.com/plus/download.php?open=2&id=455&uhash=abae06685ae1bc12e5342755"
# url3 = "http://www.jcgcn.com/plus/download.php?open=2&id=456&uhash=b15762e585cf8be4f480fbd2"
# url4 = "http://www.jcgcn.com/plus/download.php?open=2&id=457&uhash=801ab30bdce7e7f0ed21d7c8"
# url5 = "http://www.baidu.com"
# url6 = "http://support.netgear.cn/Upfilepath/WG302_V3_0_4.zip"
# url7 = "https://www.baidu.com/index.php?tn=monline_3_dg"
# filesize, getContentType =  getRemoteFileSize(url7)
# print filesize, getContentType

#---------
# import re
# ###是否含有版本号等
# def haveVersion(url):
#     url = url.lower()
#     print url
#     # split_word = re.split('\W+', url)
#     version_type1 = re.findall(r"v\d{1,8}\.", url)
#     version_type2 = re.findall(r"\d{1,8}v", url)
#     version_type3 = re.findall(r"\d{1,8}\.\d{1,8}", url)
#
#     v = version_type1 + version_type2 + version_type3
#     print v
#
#     # have_version = version_type1  or version_type3 or version_type2
#     # if have_version:
#     #     print have_version.group(0)
#     # if have_version:
#     #     print have_version.groups()
#
# url = "ftp://FTP2.DLINK.COM/PRODUCTS/DNS-340L/REVA/DNS-340L_REVA_FIRMWARE_v1.06b02.zip"
# url2 = "ftp://FTP2.DLINK.COM/PRODUCTS/DNS-340L/REVA/DNS-340L_REVA_FIRMWARE_1.22v.06b02.zip"
# haveVersion(url2)

#

#-------
import urllib
import urllib2
import requests
import os

url = "http://www.jcgcn.com/plus/download.php?open=2&id=453&uhash=7a4cabc938cd41e02c5387e7"

# # file_url = requests.get(url)
# fo = urllib.urlopen(url)
# blob = fo.read()
# file_size = len(blob)
# if fo.info().has_key('Content-Disposition'):
# 	file_name = fo.info()['Content-Disposition'].split('filename=')[1]
# 	file_name = file_name.replace('"', '').replace("'", "")
# 	print file_name
# else:
# 	file_name = os.path.basename(url)

# file_ext = get_file_ext(file_name.lower())
# remark = request.form.get("remark", '')
# # 存储到hdfs

def get_real_url(url,try_count = 1):
	if try_count > 3:
		return url
	try:
		rs = requests.get(url,headers=http_headers,timeout=10)
		if rs.status_code > 400:
			return get_real_url(url,try_count+1)
		return rs.url
	except:
		return get_real_url(url, try_count + 1)

url1 = get_real_url(url)
print url1













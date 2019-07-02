 # coding=utf-8

__author__ = "zgd"
__time__ = "2018.11.10"
#https://blog.csdn.net/HW140701/article/details/56009019?utm_source=blogxgwz5


from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random
import io
import os
import sys
from urllib import request 
import urllib

pages = set()
random.seed(datetime.datetime.now())


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


# 获取页面所有内链的列表
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    # 找出所有以“/”开头的链接
    for link in bsObj.findAll("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if (link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks


# 获取页面所有外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 找出所有以“http”或者“www”开头且不包含当前URL的链接
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def getRandomExternalLink(startingPage):
    req = request.Request(startingPage, headers=headers)
    html = urlopen(req)
    bsObj = BeautifulSoup(html.read(), "html.parser")
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("没有外部链接，准备遍历整个网站")
        domain = urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("随机外链是: " + externalLink)
    followExternalOnly(externalLink)


# 收集网站上发现的所有外链列表
allExtLinks = set()
allIntLinks = set()


def getAllExternalLinks(siteUrl):
    # 设置代理IP访问
    proxy_handler = urllib.request.ProxyHandler({'http': '183.77.250.45:3128'})
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    # proxy_auth_handler.add_password('realm', '123.123.2123.123', 'user', 'password')
    opener = urllib.request.build_opener(urllib.request.HTTPHandler, proxy_handler)
    urllib.request.install_opener(opener)

    req = request.Request(siteUrl, headers=headers)
    html = urlopen(req)
    bsObj = BeautifulSoup(html.read(), "html.parser")
    domain = urlparse(siteUrl).scheme + "://" + urlparse(siteUrl).netloc
    internalLinks = getInternalLinks(bsObj, domain)
    externalLinks = getExternalLinks(bsObj, domain)

    # 收集外链
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            # print(link)
            print("即将获取的外部链接的URL是：" + link)

    # 收集内链
    for link in internalLinks:
        if link not in allIntLinks:
            print("即将获取内部链接的URL是：" + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)



# followExternalOnly("http://bbs.3s001.com/forum-36-1.html")
# allIntLinks.add("http://bbs.3s001.com/forum-36-1.html")
getAllExternalLinks("http://wangyou.pcgames.com.cn/zhuanti/lol/")

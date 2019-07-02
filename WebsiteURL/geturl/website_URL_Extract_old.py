# -*- coding:utf-8 -*-

'''
author: zgd
date: 2018.11.03
python version: 2.7
function: Crawl a website all urls, and save urls to a urls.txt.
'''

import re
import timeit
import random
import requests
import urlparse
from user_agents import agents
from proxy_ips import proxy_ip
# from urllib.request import urlopen#用于获取网页 python3
import urllib2   # python2.7
from bs4 import BeautifulSoup


# 使用代理ip
def random_proxy_ip():
    proxy_ip_index = random.randint(0, len(proxy_ip))
    user_ip= proxy_ip[proxy_ip_index]
    return  user_ip


# 使用firefox浏览器作为代理
def random_agent():
    agent_index = random.randint(0, len(agents)-1)
    user_agent = agents[agent_index]
    return user_agent


# 检验输入要爬取的网址是否可用
def inputurl_check(url):
    try:
        user_agent = random_agent()
        # kv = {'user_agent': 'Mozilla/5.0'}
        kv = {'user_agent': user_agent}
        requests.get(url, headers=kv)
        print "Your url is right!"
        return url
    except:
        print "Your website url is incorrect! Please try again."
        # return inputurl_check()
        return


# url中特殊字符处理
def str_replace(url):
    str_url = url.replace(" ", "%20")
    strURL = str_url.replace("#", "%23")
    return strURL


https://www.baidu.com

# 获取使用的协议和域名
def getdns(url):
    # 获取链接的协议，判断是https还是http
    urlprotocol = re.findall(r'.*(?=://)', url)[0]
    # urlprotocol = url.split("://")[0]

    # 获取链接的域名
    dns = ""
    if len(re.findall(r'/', url)) > 2:
        if urlprotocol == 'https':
            dns = re.findall(r'(?<=https://).*?(?=/)', url)[0]
        elif urlprotocol == 'http':
            dns = re.findall(r'(?<=http://).*?(?=/)', url)[0]
        else:
            print "please check your input again!"
    else:
        url = url + '/'
        if urlprotocol == 'https':
            dns = re.findall(r'(?<=https://).*?(?=/)', url)[0]
        elif urlprotocol == 'http':
            dns = re.findall(r'(?<=http://).*?(?=/)', url)[0]
        else:
            print "please check your input again!"
    return urlprotocol, dns


###新方法获取协议和dns
def get_dns(url):
    url_change = urlparse.urlparse(url)
    # print url_change
    urlprotocol = url_change.scheme
    dns = url_change.netloc
    return urlprotocol, dns


# 爬取一个url页面中的源码      ###暂时不使用
def spiderpage(url):
    user_agent = random_agent()
    # kv = {'user_agent': 'Mozilla/5.0'}
    kv = {'user_agent': user_agent}
    r = requests.get(url, headers=kv)
    r.encoding = r.apparent_encoding
    pagetext = r.text
    return pagetext


# 获取每个页面的所有a标签的href中的链接内容   ###暂时不用
def gethref(pagetext):
    # page_href = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')', pagetext)
    pagelinks = re.findall(r'(?<=<a href=\").*?(?=\")|(?<=href=\').*?(?=\')', pagetext)
    return page_href


# 直接获取每个页面的a标签的href内容
def get_href(urlprotocol, dns, url):
    pagelinks = []
    try:
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        tag_a = soup.find_all('a')
        for a in tag_a:
            href = a.get('href')
            if href:
                # print href
                link = href_selected(urlprotocol, dns, href)
                # abslink = href_check(link)    ###为了页面链接提升效率，这条链接检查暂时最好不使用
                # if abslink:
                #     pagelinks.append(abslink)
                if link:
                    pagelinks.append(link)
    except Exception,e:
        print e.message

    return pagelinks



# 对href信息进行整合，确保获取的链接为有用的链接
def href_selected(urlprotocol, dns, href):
    link = ""
    if href.startswith("https://") or href.startswith("http://") or href.startswith("ftp://"):
        link = href
    elif href.startswith("www"):
        link = urlprotocol + "://" + href

    # elif href.startswith("//www."):
    #     link = urlprotocol + href

    elif href.startswith("/") or href.startswith("//"):
        link = urlprotocol + "://" + dns + href

    elif not href.startswith("#"):
        link = urlprotocol + "://" + dns + "/" + href
    else:
        pass
    return link


# 检查获取a标签中的href的信息是否能用，因为拼接后的链接信息可能无法使用
def href_check(link):
    try:
        user_agent = random_agent()
        # kv = {'user_agent': 'Mozilla/5.0'}
        kv = {'user_agent': user_agent}
        requests.get(link, headers=kv)
        return link
    except:
        print "The link obtained is not available!"



# 去除不是该站点的url，并且去除重复的链接信息
def url_filtrate(dns, pagelinks):
    website_url = []
    for link in pagelinks:
        if re.findall(dns, link):
            website_url.append(link)
    unrepeat_url = url_unrepeat(website_url)
    return unrepeat_url


# 去除单个页面内的重复的url
def url_unrepeat(website_url):
    unrepeat_url = []
    for link in website_url:
        if link not in unrepeat_url:
            unrepeat_url.append(link)
    return unrepeat_url


# 将已经访问的列表写入文件
def writetofile(all_url_list):
    try:
        with open('urls.txt', 'w') as f:
            for url in all_url_list:
                f.write(url)
                f.write('\n')
        f.close()
    except Exception,e:
        print e.message



# url集合进行处理，分为已访问集合和未访问集合
class linkQuence:

    def __init__(self):
        # 已访问的url集合
        self.visited = []
        # 待访问的url集合
        self.unvisited = []

    # 获取访问过的url队列
    def getvisitedurl(self):
        return self.visited

    # 获取未访问的url队列
    def getunvisitedurl(self):
        return self.unvisited

    # 添加url到访问过的队列中
    def addvisitedurl(self, url):
        return self.visited.append(url)

    # 移除访问过得url
    def removevisitedurl(self, url):
        return self.visited.remove(url)

    # 从未访问队列中取一个url
    def unvisitedurldequence(self):
        try:
            a_url = self.unvisited.pop()   ###默认取出队列中最后一个值，并返回最后一个值
            return a_url
        except:
            return None

    # 添加url到未访问的队列中
    def addunvisitedurl(self, url):
        # if url != "" and url not in self.visited and url not in self.unvisited:
        if not url == "" and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0, url)  #插入到第一个位置

    # 获得已访问的url数目
    def getvisitedurlount(self):
        return len(self.visited)

    # 获得未访问的url数目
    def getunvistedurlcount(self):
        return len(self.unvisited)

    # 判断未访问的url队列是否为空
    def unvisitedurlsempty(self):
        return len(self.unvisited) == 0



###URL爬取开始
class URLSpider():
    def __init__(self, urlprotocol, dns, url):
        self.urlprotocol = urlprotocol
        self.dns = dns
        self.linkQuence = linkQuence()   # 引入linkQuence类
        self.linkQuence.addunvisitedurl(url)   # 并将需要爬取的url添加进linkQuence队列中

    ###页面的循环爬取
    def pageCrawler(self):
        while not self.linkQuence.unvisitedurlsempty():   # 若未访问队列非空
            visitedurl = self.linkQuence.unvisitedurldequence()   # 取一个url
            if visitedurl is None or visitedurl == "":
                continue
            pagelinks = get_href(self.urlprotocol, self.dns, visitedurl)   # 获取一个页面内的所有href链接
            right_links = url_filtrate(self.dns, pagelinks)   # 筛选出合格的链接
            if right_links:
                right_url = right_links
                print right_url
                for link in right_links:  # 将筛选出的链接放到未访问队列中
                    self.linkQuence.addunvisitedurl(link)
            else:
                pass

            self.linkQuence.addvisitedurl(visitedurl)    # 将已经处理过的该url放到已访问过的url队列中

        print("Congratulations, all the links have been crawled!")
        return self.linkQuence.visited


###程序开始
def begin():
    website_url = raw_input("Please input a website url:")

    website_url= str_replace(website_url)
    # ----检查输入的url是否可用----
    website_url = str(website_url)
    url = inputurl_check(website_url)


    # ----输出输入网址的协议和域名----
    urlprotocol, dns = getdns(url)
    print 'The protocol used by the station is：' + urlprotocol
    print 'DNS：' + dns
    print "----------start----------"

    # # ----获取页面的所有链接，返回页面url的列表----
    # pagelinks = get_href(url, urlprotocol, dns)
    #
    # # ---去除不是本站点的url和重复的url，返回页面url的列表
    # unrepeat_url = url_filtrate(dns, pagelinks)
    # print unrepeat_url

    spider = URLSpider(urlprotocol, dns, url)
    all_url_list = spider.pageCrawler()
    writetofile(all_url_list)


if __name__ == '__main__':
    start = timeit.default_timer()
    begin()
    end = timeit.default_timer()
    print str(end - start)

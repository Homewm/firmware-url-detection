#!/usr/local/bin/python
#-*- coding: UTF-8 -*-

from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)

#######################################################
import urllib
import urllister
import socket
import Queue,threading
import time
from threading import Thread
socket.setdefaulttimeout(5)
import list
#消息队列
openurl = Queue.Queue(0)
class Class_url_www(threading.Thread):  #  采集URL
    def __init__(self,LS):
        threading.Thread.__init__(self)
        self.LS=LS
        self.urlname="taobao.com" #域名关键字
        #self.data("http://www.youku.com")
        openurl.put("http://taobao.com",0.5)   #插入队列

    def run(self):
        try:
            print u"消息队列:",openurl.qsize()
            print u"已经扫描过:",len(self.LS.list)
            if openurl.empty():   #判断队列是否为空
                print u"消息队列为空"
                time.sleep(20)
                self.run()
            self.Chost = openurl.get(0.5)  #get()方法从队头删除并返回一个项目
            if self.Chost=="":
                time.sleep(20)
                self.run()
                #self.Chost="127.0.0.1"
            self.data(self.Chost) #遍历页里的地址
            self.run()
        except:
            self.run()


    def data(self,url):
        try:
            if self.LS.liet_CX(url):  #查询这个地址是否爬过
                print "这个URL地址已经爬过了:",url
                return 0
            self.LS.liet_add(url)
            self.TXT_file(url)  #写入文本
            print u"开始采集:",url

            list_2=[]
            list=self.getURL(url)
            for i in list:  #去重重复数据
                if i not in list_2:
                    if self.urlname in i:
                        list_2.append(i)
            if len(list_2) > 0:
                for url in list_2:
                    #print url.strip().lstrip().rstrip('\n')
                    if "http://" in url:
                        #if not openurl.qsize()>=30000:
                        openurl.put(url.strip().lstrip().rstrip('\n'),0.5)   #插入队列
        except Exception,e:
            print "data11111111111111111111111111",e
            self.run()
            return 0

    def getURL(self,url):  #getURL(url)用来将HTML中的url放入urls列表中
        try:
            try:
                usock = urllib.urlopen(url)
            except:
                print 'get url excepton'
                return []
            parser = urllister.URLLister()
            parser.feed(usock.read())
            usock.close()
            parser.close()
            urls = parser.urls
            return urls
        except Exception,e:
            print u"getURL",e
            return 0

    def TXT_file(self,data):  #写入文本
        try:
            #file_nem=time.strftime('%Y.%m.%d')   #file_nem+".txt"
            file_object = open("url.txt",'a')
            #file_object.write(list_passwed[E])
            file_object.writelines(data)
            file_object.writelines("\n")
            file_object.close()
        except Exception,e:
            print u"写入TXT失败",e
            return 0


if __name__ == '__main__':
    LS = list.Clist()  #初始化类
    threads = []  #线程
    for i in range(10):  #nthreads=10  创建10个线程
        threads.append(Class_url_www(LS))

    for t in threads:   #不理解这是什么意思    是结束线程吗
        t.start()  #start就是开始线程

# -*- coding:utf-8 -*-

import urlparse
import requests
import urllib2
###根据url链接提取下载文件的大小特征和下载文件类型

###根据url链接提取下载文件的大小特征和下载文件类型
def getRemoteFileSize(url, proxy=None):
    '''
    通过content-length头获取远程文件大小
    '''
    opener = urllib2.build_opener()
    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))
        elif url.lower().startswith('http://'):
            opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))
        else:
            opener.add_handler(urllib2.ProxyHandler({'ftp': proxy}))
    try:
        request = urllib2.Request(url)
        request.get_method = lambda: 'HEAD'
        response = opener.open(request, timeout=60)
        response.read()
    except Exception, e:
        # 远程文件不存在
        return 0, 0
    else:
        getfileSize = dict(response.headers).get('content-length', 0)
        filesize = round(float(getfileSize) / 1048576, 2)
        getContentType = dict(response.headers).get('content-type', 0)
        return filesize, getContentType


###请求内容：文件大小，文件类型
url = "http://tomato.groov.pl/download/MariuszNM/STD/tomato_1.27PL.46H.trx"

filesize, getContentType = getRemoteFileSize(url)
print getContentType
print filesize
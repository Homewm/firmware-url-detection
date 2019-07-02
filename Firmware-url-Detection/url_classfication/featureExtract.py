# -*- coding:utf-8 -*-

import urlparse
import requests
import urllib2
import re
import urllib
import os
import time


###链接是否具有关键词
def haveKeywords(url):
    key_words = ["firmware", "固件", "软件升级", "升级软件", "gujian"]
    for word in key_words:
        if word in url.lower():
            return 1
        else:
            return 0


###扩展名是否为常见的固件扩展名
def extensionName(url):
    extension_firmware = ['bin', 'rar', 'zip', 'tar', '7z', 'bix', 'trx', 'dlf', 'tfp', 'ipk', 'bz2',
                           'gz', 'img', 'lzma', 'tgz', 'exe', 'ubi', 'uimage', 'ram', 'elf', 'ipa', 'chm',
                           'arg', 'z', 'bak', 'dsw', 'dsp', 'clw', 'mav', 'dav', 'upg', 'iso', 'bfp', 'hex',
                           'npk', 'mdf', 'map', 'com', 'vhdx', 'vmdk', 'vdi', 'ova', 'lzb', 'ipsw', 'xz',
                           'had', 'all', 'pkg', 'rtf', 'pat', 'online', 'apk', 'ssu', 'cssu', 'pk2', 'ov',
                           'stk', 'chk', 'dmg', 'mib', 'rmt', 'opr', 'rom', 'os', 'sh', 'conf', 'sha256',
                           'w', 'fu', '8xu', 'tno', 'tco', 'tnc', '8eu', '73u', 'hqx', '89u', 'v2u', 'tcc']

    ends_firmware = ['download', '=yes', '=false', '=ipdbm', '=local']  ###结尾的是特别的字符串

    ends_other = ['/']

    extension_other = ['txt', 'pdf', 'apk', 'doc', 'gdb', 'rm', 'avi', 'xls', 'mid', 'rtf', 'hlp', 'pic',
                        'png', 'tif', 'bmp', 'gif', 'jpg', 'mpg', 'swf', 'c', 'asm', 'for', 'lib', 'lst',
                        'msg', 'obj', 'pas', 'wki', 'bas', 'dot']


    url_extension = url.split(".")[-1]
    if url_extension in extension_firmware:
        return 1
    elif url_extension in extension_other:
        return 0
    # elif url.endswith() in ends_firmware:
    #     return 1
    else:
        return 0


###除协议和域名之外的链接层次长度问题
def pathLength(url):
    obj = urlparse.urlparse(url)
    host = obj.netloc  ###域名
    path = obj.path   ###出域名之外所有的路径
    if path:
        len_path = len(path.split("/"))
        return len_path
    else:
        return 0


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


##是否含有年份等日期特征
def haveDate(url):
    start_year = 1995
    end_year = 2018
    for year in range(start_year, end_year + 1):
        if str(year) in url:
            return 1
        else:
            continue
    return 0


###是否含有版本号等
def haveVersion(url):
    url_last = url.split("/")[-1]
    try:
        url_last = url_last.lower()
        version_type1 = re.findall(r"v\d{1,8}\.", url_last)
        version_type2 = re.findall(r"\d{1,8}v", url_last)
        version_type3 = re.findall(r"\d{1,8}\.\d{1,8}", url_last)
        version_type4 = re.findall(r"_\d{1,8}\.\d{1,8}", url_last)
        have_version = version_type1 + version_type2 + version_type3 + version_type4
        if have_version:
            return 1
        else:
            return 0
    except Exception,e:
        return 0


###获取真实的url和文件名，并返回
def getRealFile(url, passName=None):
    if passName:
        fileName = passName
        urllib.urlretrieve(attachURL, fileName)
    else:
        try:
            r = urllib2.urlopen(url, timeout=60)
            if r.info().has_key('Content-Disposition'):
                fileName = ""
                file_Name = r.info()['Content-Disposition'].split('filename=')
                if len(file_Name) >= 2:
                    fileName = file_Name[1]
                    fileName = fileName.replace('"', '').replace("'", "")
                elif url:
                    fileName = os.path.basename(url)
            elif r.url != url:
                # if we were redirected, the real file name we take from the final URL
                from os.path import basename
                from urlparse import urlsplit
                fileName = basename(urlsplit(r.url)[2])
            else:
                fileName = os.path.basename(url)
            return r.url, fileName
        except Exception,e:
            try:
                r = urllib2.urlopen(url, timeout=60)
                fileName = ""
                return r.url, fileName
            except Exception,e:
                fileName = ""
                return url, fileName


###文件名的长度和文件名占据实际链接的长度
def fileLength(url):
    url_last = url.split("/")[-1]      ###未必是文件名
    url, fileName = getRealFile(url)
    try:
        filename_len = len(fileName)
        url_len = len(url)
        filename_percentage = ('%.5f' % (float(filename_len)/url_len))
        return filename_len, filename_percentage
    except Exception,e:
        return 0, 0


###点的数量
def pointCount(url):
    point_count = url.count('.')
    return point_count


def feature_extract(url):
    ##是否含有关键字
    have_keywords = haveKeywords(url)

    ##判断是否为上述扩展名
    url_extension = extensionName(url)

    ###路径分层长度
    apth_len = pathLength(url)

    ###请求内容：文件大小，文件类型
    filesize, getContentType = getRemoteFileSize(url)
    print "getContentType:",getContentType
    print "filesize:",filesize

    ###是否含有年月日
    have_date = haveDate(url)

    ###是否具有版本号
    have_version = haveVersion(url)

    ###文件名长度，文件名长度占据链接的长度
    filename_len, filename_percentage = fileLength(url)
    print "filename_len:", filename_len
    print "filename_percentage:", filename_percentage

    ###点的数量
    point_count = pointCount(url)
    # print point_count

    Feature = {}
    Feature['url'] = url
    Feature['have_keywords'] = have_keywords
    Feature['url_extension'] = url_extension
    Feature['apth_len'] = apth_len
    Feature['filesize'] = filesize
    Feature['getContentType'] = getContentType
    Feature['have_date'] = have_date
    Feature['have_version'] = have_version
    Feature['filename_len'] = filename_len
    Feature['filename_percentage'] = filename_percentage
    Feature['point_count'] = point_count
    return Feature


# if __name__ == '__main__':
#     with open("firmwareurls.txt", "r") as file:
#         lines = file.readlines()
#         file.close()
#         for line in lines:
#             url = line.strip()
#             filename_len, filename_percentage =  fileLength(url)
#             # print filename_percentage


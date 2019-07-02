#-*- coding:utf-8 -*-


import urllib2
import os

def getFile(url, passName=None):
    if passName:
        fileName = passName
        urllib.urlretrieve(attachURL, fileName)
        print  fileName
    else:
        r = urllib2.urlopen(url, timeout=60)
        if r.info().has_key('Content-Disposition'):
            fileName = ""
            file_Name = r.info()['Content-Disposition'].split('filename=')
            if len(file_Name) >=2:
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

        print fileName
        print r.url

getFile("http://tomato.groov.pl/download/K26ARM/Netgear%20R-series%20initial%20files/tomato-R6400-initial.chk")
# getFile("http://ota.quanwifi.com/firmware/FYX-AP01J_4.2.0_r1505.bin")
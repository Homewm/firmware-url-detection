# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-

import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


###将从数据库里面提取的固件链接url，添加标签

with open('firmwareurl_hikvision.txt', 'r') as f1:
    lines1 = f1.readlines()
    f1.close()


with open('firmwareurl_hikvision_label.txt','w') as f2:
    for line in lines1:
        url_info = line.strip()
        if url_info:
            extension_list = ["txt", "pdf", "apk", "doc", "gdb", "rm", "avi", "xls", "MID", "rtf", "hlp", "pic", "png", "tif", "bmp", "gif", "jpg", "avi", "mpg", "swf", "c", "asm", "for", "lib", "lst", "msg", "obj", "pas", "wki", "bas", "dot"]

            if url_info[-3:] not in extension_list:
                f2.write(url_info)
                f2.write(',1\n')
    f2.close()
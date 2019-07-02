# -*- coding: utf-8 -*-

###处理mongoDB中下载后的数据，同时过滤掉一些误下载的url
###也可以同时添加标签

import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


with open("firmwareurl_hikvision.json", 'r') as file1:    ##修改
    lines = file1.readlines()
    for line in lines:
        params = json.loads(line)
        url_info = params ["url"]
        url_info = str(url_info)
        if url_info:
            extension_list = ["txt", "pdf", "apk", "doc", "gdb", "rm", "avi", "xls", "MID", "rtf", "hlp", "pic", "png", "tif", "bmp", "gif", "jpg", "avi", "mpg", "swf", "c", "asm", "for", "lib", "lst", "msg", "obj", "pas", "wki", "bas", "dot"]

            if url_info[-3:] not in extension_list:

                with open("firmwareurl_hikvision.txt", "a") as file2:   ##修改
                    file2.write(url_info)
                    file2.write("\n")
                    # file2.write(",1\n")
                    file2.close()
                print "处理成功一个"
    file1.close()




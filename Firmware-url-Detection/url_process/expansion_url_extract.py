# -*- coding: utf-8 -*-

###处理mongoDB中下载后的数据

import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')



with open("crawl_urls.json", 'r') as file1:
    lines = file1.readlines()
    for line in lines:
        params = json.loads(line)
        url_info = params ["url"]
        url_info = str(url_info)
        # expansion =
                with open("firmwareurls.txt", "a") as file2:
                    file2.write(url_info)
                    file2.write("\n")
                    # file2.write(",1\n")
                    file2.close()
                print "处理成功一个"
    file1.close()
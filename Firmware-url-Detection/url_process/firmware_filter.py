# -*- coding:utf-8 -*-

###从爬取的文件中过滤掉数据库中的固件链接
###同时过滤掉换行符和重复的内容

with open('url_spider_hikvision.txt', 'r') as f1:
    lines1 = f1.readlines()
    f1.close()
with open('firmwareurl_hikvision.txt', 'r') as f2:
    lines2 = f2.readlines()
    f2.close()
    line_strip = []
    for l in lines2:
        l = l.strip()
        line_strip.append(l)
    lines3 = []

    for line in lines1:
        line = line.strip()
        if line not in line_strip:
            if line not in lines3:
                lines3.append(line.strip())

with open('not_firmwareurl_hikvision_label.txt','w') as f3:
    for line in lines3:
        f3.write(line)
        f3.write(',0\n')
    f3.close()
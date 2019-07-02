# -*- coding:utf-8 -*-


with open('urls_tomato.txt','r') as f1:
    lines1 = f1.readlines()
    no_strip_list = []
    for line in lines1:
        if line not in no_strip_list:
            no_strip_list.append(line.strip())
    f1.close()
    print no_strip_list

with open('url_spider_tomato.txt','r') as f2:
    lines2 = f2.readlines()
    f2.close()
    line3 = []
    for line in lines2:
        line = line.strip()
        if line not in no_strip_list:
            if line not in line3:
                line3.append(line)

with open('firmwareurl_tomato.txt', 'a') as f3:
    for line in no_strip_list:
        f3.write(line)
        f3.write('\n')
    f3.close()


with open('not_firmwareurl_tomato.txt', 'r') as f4:
    lines4 = f4.readlines()
    no_strip_list2 = []
    for line in lines4:
        no_strip_list2.append(line.strip())
    f4.close()


with open('url_clear.txt', 'a') as f5:
    extract = ['.gz', '.zip', '.tgz']

    fiter = []

    for line in no_strip_list2:
        for e in extract:
            if line.endswith(e) == True:
                if not line in fiter:
                    fiter.append(line)
    for line in fiter:
        f5.write(line)
        f5.write('\n')
    f5.close()

# -*- coding:utf-8 -*-
##是否含有年份等日期特征
def haveDate(url):
    start_year = 1995
    end_year = 2018
    for year in range(start_year, end_year + 1):
        if str(year) in url:
            print year
            return 1
        else:
            continue
    return 0

with open("testurl.txt") as file:
    for line in file:
        ##对每一行内容进行划分为链接和标签
        content_list = line.split(",")
        ##url链接
        url = content_list[0].strip()
        ##标签
        try:
            if content_list[1]:
                firm_bool = content_list[1].strip()
            else:
                firm_bool = "0"
        except Exception,e:
            print e.message
            firm_bool = "0"

        print url

        print haveDate(url)
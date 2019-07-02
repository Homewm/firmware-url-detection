# -*- coding:utf-8 -*-
#author:zgd
import pandas
import csv

# with open("url_features_3_zgd.csv", 'r') as f:
#     train_csv = csv.DictReader(f)   ###读取和加载查询的特征集
#     print train_csv.fieldnames
#     f.close()

    # firm_type = []
    # not_firm_type = []
    # for row in train_csv:
    #     if row["firmware_bool"] == "1":
    #         if row["getContentType"] not in firm_type:
    #             firm_type.append(row["getContentType"])
    #     elif row["firmware_bool"] == "0":
    #         if row["getContentType"] not in not_firm_type:
    #             not_firm_type.append(row["getContentType"])
    #     else:
    #         print "----------"
    # print firm_type
    # print not_firm_type


firm_type = ['application/octet-stream', 'application/zip', 'application/x-gzip',
             'application/x-sh', 'text/plain', 'application/x-rar-compressed',
             'application/x-7z-compressed', 'application/rar', 'application/x-msdos-program',
             'chemical/x-chemdraw']
not_firm_type = ['text/html;charset=utf-8', 'text/x-sh', 'text/x-diff', 'text/html; charset=UTF-8',
                 'text/html;charset=ISO-8859-1', 'text/html']


with open("url_features_3_zgd.csv", 'r') as f1:
    train_csv = csv.DictReader(f1)  ###读取和加载查询的特征集
    print train_csv.fieldnames



    feature = []
    for row in train_csv:
        Feature = {}
        if row["getContentType"] in firm_type:
            row["getContentType"] = "1"
        elif row["getContentType"] in not_firm_type:
            row["getContentType"] = -1
        elif row["getContentType"] == "0":
            row["getContentType"] = 0
        else:
            row["getContentType"] = 0


        Feature["getContentType"] = row["getContentType"]
        Feature['point_count'] = row['point_count']
        Feature['apth_len'] = row['apth_len']
        Feature['url'] = row['url']
        Feature['filename_percentage'] = row['filename_percentage']
        Feature['have_version'] = row['have_version']
        Feature['have_date'] = row['have_date']
        Feature['have_keywords'] = row['have_keywords']
        Feature['url_extension'] = row['url_extension']
        Feature['filesize'] = row['filesize']
        Feature['firmware_bool'] = row['firmware_bool']
        Feature['filename_len'] = row['filename_len']
        feature.append(Feature)
    f1.close()

with open('url_features_4_zgd.csv','wb') as file:
    flag = True
    for item in feature:
        w = csv.DictWriter(file, item.keys())
        if flag:
            w.writeheader()   ###第一行是特征名，只在第一行显示。学习这一行的使用方法。
            flag=False
        w.writerow(item)
    file.close()


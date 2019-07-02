# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import csv
import featureExtract as urlfeature  ##提取url特征
# import train as tr   ##链接训练
import numpy


###将特征写入文本文件
##输入特征列表和输出的目标文件，其中特征列表形式为：[url,多个特征的字典]

##目标是获取输出特征csv格式
def resultwriter(feature, output_dest):
    flag=True
    with open(output_dest,'wb') as file:
        for item in feature:
            w = csv.DictWriter(file, item[1].keys())
            if flag:
                w.writeheader()   ###第一行是特征名，只在第一行显示。学习这一行的使用方法。
                flag=False
            w.writerow(item[1])
        file.close()


##输入为链接文件URL.txt和链接的特征文件url_features.csv
##将特征[url, 预测值]和结果输出文件作为参数
def process_URL_list(file_dest, output_dest):
    feature = []
    with open(file_dest) as file:
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

            if url:
                print 'working on train url: ' + url
                ##url特征提取
                ret_dict = urlfeature.feature_extract(url)
                ###输出是否是固件下载链接
                ret_dict['firmware_bool'] = firm_bool
                feature.append([url, ret_dict])
                # print feature
        file.close()
    resultwriter(feature, output_dest)


##预测的url输入
def process_test_list(file_dest,output_dest):
    feature=[]
    with open(file_dest) as file:
        for line in file:
            url=line.strip()
            if url:
                print 'working on test url: ' + url
                ret_dict=urlfeature.feature_extract(url)
                feature.append([url,ret_dict])
        file.close()
    resultwriter(feature, output_dest)


def begin():
        process_URL_list('urls_label_1.txt','url_features_8.csv')       ##标记为0和标记为1的所有的链接均进行处理
        # process_test_list("query.txt",'query_features.csv')   ##待查询和预测的url
        # tr.train('url_features.csv','url_features.csv')    #arguments:(input_training feature,test/query traning features)
        # tr.train('url_features.csv','query_features.csv')   #testing with urls in query.txt    ###url特征

if __name__ == '__main__':
    begin()






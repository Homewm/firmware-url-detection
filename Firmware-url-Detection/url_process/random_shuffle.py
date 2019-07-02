#coding:utf-8
#author:zgd

import pandas as pd
import numpy as np
import random

urls = 't1.csv'	#path to our all urls file
urlscsv = pd.read_csv(urls)	#reading file
print urlscsv
urlsdata = pd.DataFrame(urlscsv)	#converting to a dataframe   ###数据格式化
urlsdata = np.array(urlsdata)	#converting it into an array
numpy.random.shuffle(urlsdata)	#shuffling    ####随机序列化
print urlsdata



# import numpy
# import random
# n = [[1,2,3],[4,5,6]]
# m = numpy.array([[1,2,3],[4,5,6]])
# random.shuffle(n)
# random.shuffle(m)
# t = numpy.array([[1,2,3],[4,5,6]])
# t[0],t[1] = t[1],t[0]
#
# print "n:",n
# print "m:",m
# print "t:",t
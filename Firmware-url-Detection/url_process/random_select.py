# -*- coding:utf-8 -*-

##随机挑选部分内容
# encoding:utf-8
import random
from random import randint

oldf = open('select_amigo.txt', 'r')
newf = open('select_amigo222.txt', 'w')
n = 0
resultList = random.sample(range(0, 1000), 400)  # sample(x,y)函数的作用是从序列x中，随机选择y个不重复的元素。

lines = oldf.readlines()
for i in resultList:
    newf.write(lines[i])
oldf.close()
newf.close()





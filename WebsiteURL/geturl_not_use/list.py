#!/usr/local/bin/python
#-*- coding: utf-8 -*-
class Clist:
    def __init__(self):    #初始化类
        #self.list
        self.list=[]
        #self.list_2
        self.list_2=[]

    def list_del(self):  #清空list列表
        try:
            del self.list
            del self.list_2
        #########################################
        except:
            print u"清空数组失败"
            return 0

    def liet_lsqc(self): #列表去重复
        try:
                    #passlist = list(set(passlist))   #python 列表去重
            for i in self.list:
                if i not in self.list_2:
                    self.list_2.append(i)
        except:
            print u"列表去重复错误"
            return 0

    def liet_add(self,data):
        try:
#            if len(self.list)>=20000:  #300X300=9000 次密码组合
#                print u"导入数量过大于4100"
#                return 0

            self.list.append(data)  #添加数据
#            print u"数组数量",len(self.list)
#            if len(self.list)>=2000:  #如果数据量过大  就清空数组
#                self.list_del()  #清空list列表
        except:
            print u"liet添加异常"
            return 0
    def liet_CX(self,data):  #查询数据是否存在
        try:
            E = 0 #得到list的第一个元素
            while E < len(self.list):
                #print self.list_2[E]
                if self.list[E]==data:
                    return 1
                E = E + 1
            return 0
        except:
            print u"liet查询异常"
            return 0

#if __name__=='__main__':
#    LS = Clist()  #初始化类
#    LS.liet_add("AAAAA")
#    LS.liet_add("BBBBB")
#    if LS.liet_CX("AAAAA"):  #查询数据是否存在
#        print u"有"
#    else:
#        print u"无"
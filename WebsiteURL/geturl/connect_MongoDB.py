#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pymongo import MongoClient

#建立MongoDB数据库连接
client = MongoClient('IP', 27017)

#用户验证
db = client.库名
db.authenticate("账号", "密码")

#连接所用集合，也就是我们通常所说的表
collection=db.表名

#接下里就可以用collection来完成对数据库表的一些操作
with open ('文件名.txt', 'wb') as f:

#接下来可实现提取想要的字段内的数据
    for item in collection.find({}, {"Summary":1,"Manual":1,"Claim":1,"_id":0}):
        if item.has_key('Summary') and item['Summary']:
            f.write(item['Summary'])
        if item.has_key('Manual') and item['Manual']:
            f.write(item['Manual'])
        if item.has_key('Claim') and item['Claim']:
            f.write(item['Claim'])
        f.write('\n')
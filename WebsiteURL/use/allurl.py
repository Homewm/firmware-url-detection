# coding:utf-8

#https://blog.csdn.net/wxfghy/article/details/80308825?utm_source=blogxgwz8

# 待研究


#验证输入的url是否可正常连接,无法连接提示用户再次输入,正常连接则返回url本身
def url_get():
    url = input("请输入要爬取的首页url:")
    try:
        # 做一个user-agent模拟浏览器发送请求,也可以加入其它字段
        kv = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
        requests.get(url, headers=kv)
        return url
    except:
        print("url无法连接")
    return url_get()



#根据传入的URL参数进行爬取,以列表形式返回
def spiderpage(url):
    kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
    r = requests.get(url, headers=kv)
    r.encoding = r.apparent_encoding
    pagetext = r.text
    # 正则表达式表示要爬取的是<a href="和"中的内容,"或'都可以,即当前页面下所有的链接url,返回列表
    pagelinks = re.findall(r'(?<=<a href=\").*?(?=\")|(?<=href=\').*?(?=\')', pagetext)
    return pagelinks


#根据需要对爬取的所有Url进行筛选和去重,传入的参数为列表形式的Url集合,返回的是符合条件的URL集合
def url_filtrate(pagelinks):
    # 去除不是以要爬取网站开头的url,如跳转的广告等
    same_target_url = []
    for l in pagelinks:
        if re.findall(r'blog.csdn.net/\w+/article/details/\d+', l):
            # 根据对网页的分析添加筛选条件,过滤掉系统推荐的博文链接
            if re.findall(r'blockchain_lemon', l):
                pass
            # 过滤掉广告链接
            elif re.findall(r'passport', l):
                pass
            else:
                same_target_url.append(l)
    # 去除重复url
    unrepect_url = []
    for l in same_target_url:
        if l not in unrepect_url:
            unrepect_url.append(l)

    return unrepect_url



#队列,实现将url集合分为未访问和已访问两类,当前未访问为空时结束循环等功能
class linkQuence:
    def __init__(self):
        # 已访问的url集合
        self.visited = []
        # 待访问的url集合
        self.unvisited = []

    # 获取访问过的url队列
    def getvisitedurl(self):
        return self.visited

    # 获取未访问的url队列
    def getunvisitedurl(self):
        return self.unvisited

    # 添加url到访问过得队列中
    def addvisitedurl(self, url):
        return self.visited.append(url)

    # 移除访问过得url
    def removevisitedurl(self, url):
        return self.visited.remove(url)

    # 从未访问队列中取一个url
    def unvisitedurldequence(self):
        try:
            return self.unvisited.pop()
        except:
            return None

    # 添加url到未访问的队列中
    def addunvisitedurl(self, url):
        if url != "" and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0, url)

    # 获得已访问的url数目
    def getvisitedurlount(self):
        return len(self.visited)

    # 获得未访问的url数目
    def getunvistedurlcount(self):
        return len(self.unvisited)

    # 判断未访问的url队列是否为空
    def unvisitedurlsempty(self):
        return len(self.unvisited) == 0


#爬虫代码,通过调用上边的函数和队列,爬取输入页面下的所有链接,循环输入子页面就可以爬取所有子链接,以列表形式返回url集合
class Spider():
    def __init__(self, url):
        self.linkQuence = linkQuence() # 将队列引入本类
        self.linkQuence.addunvisitedurl(url) # 传入待爬取的url,即爬虫入口

    def crawler(self,urlcount):
    # 子页面过多,为测试方便加入循环控制子页面数量
        x = 1
        while x <= urlcount:
            # 若子页面不是很多,可以直接使用队列中的未访问列表非空作为循环条件
            # while not self.linkQuence.unvisitedurlsempty():
            if x > 1:
                print(f"第{x-1}个url,开始爬")
            visitedurl = self.linkQuence.unvisitedurldequence() # 从未访问列表中pop出一个url
            if visitedurl is None or visitedurl == '':
                continue
            initial_links = spiderpage(visitedurl) # 爬出该url页面中所有的链接
            right_links = url_filtrate(initial_links) # 筛选出合格的链接
            self.linkQuence.addvisitedurl(visitedurl) # 将该url放到访问过的url队列中
            for link in right_links: # 将筛选出的链接放到未访问队列中
                self.linkQuence.addunvisitedurl(link)
            x += 1
        print(f"终于爬完了,一共是{x-2}个url")
        return self.linkQuence.visited


#将爬取到的子链接全部写入本地文件
def writetofile(list):
    # 因为第一个爬取的页面为爬虫入口,非需要的博文网址,因此从[1]开始写入
    x=1
    for url in list[1:]:
        # urls.txt用于保存博文标题和博文链接,文件夹demo创建好,或者加入os也行,反正很简单
        file = open('F://demo/urls.txt', 'a', encoding='utf8')
        file.write(f'{url}\n')
        x += 1
    file.close()
    print(f'写入已完成,总计{x-1}个子链接')



#启动爬虫
if __name__ == '__main__':
    url = url_get()
    spider = Spider(url)
    #传入要爬取的子链接数量100
    urllist = spider.crawler(100)
    writetofile(urllist)








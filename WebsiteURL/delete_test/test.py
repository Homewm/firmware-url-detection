# coding:utf-8


from collections import Counter
#count the string edit distance2
def editDisSim2(s1,s2):
    m = len(s1)
    n = len(s2)
    if m == 0 and n == 0:
        return 1.0
    elif (m*n==0):
        if m<10 or n<10:
            return 0.3
        else:
            return 0.0
    else:
        colsize = m + 1
        matrix = []
        for i in range((m + 1) * (n + 1)):
            matrix.append(0)
        for i in range(colsize):
            matrix[i] = i
        for i in range(n + 1):
            matrix[i * colsize] = i
        for i in range(n + 1)[1:n + 1]:
            for j in range(m + 1)[1:m + 1]:
                cost = 0
                if s1[j - 1] == s2[i - 1]:
                    cost = 0
                else:
                    cost = 1
                minValue = matrix[(i - 1) * colsize + j] + 1
                if minValue > matrix[i * colsize + j - 1] + 1:
                    minValue = matrix[i * colsize + j - 1] + 1
                if minValue > matrix[(i - 1) * colsize + j - 1] + cost:
                    minValue = matrix[(i - 1) * colsize + j - 1] + cost
                matrix[i * colsize + j] = minValue
        return 1.0 -float(matrix[n * colsize + m]) / max(m,n)


#count the string edit distance1
def editDisSim(s1,s2):
    m =len(s1)
    n = len(s2)
    if m == 0 and n == 0:
        return 1.0
    elif (m*n==0):
        if m<10 or n<10:
            return 0.3
        else:
            return 0.0
    else:
        data = [[0 for c in range(n + 1)] for r in range(m + 1)]
        for r in range(m+1):
            for c in range(n+1):
                if not r or not c:
                    data[r][c]=r+c
                else:
                    data[r][c] = min(data[r][c - 1] + 1, data[r - 1][c] + 1, data[r - 1][c - 1] + (s1[r - 1] != s2[c - 1]))
        return 1.0-float(data[m][n])/max(m,n)


set1 = ["chang","qing","a","b","c"]
set2 = ["changqing","chang"]
s1 = "www.support.xerox.com"
s2 = "www.xerox.com"
e1 = editDisSim(s1, s2)
# e2 = editDisSim2()
# print e1
# print e2


import difflib
a= 'www.12345.com'
b= 'www.123.com'
print difflib.SequenceMatcher(None,a,b).ratio()



###使用相似度计算，判断是属于同一域名
def url_filtrate1(urlprotocol,dns, pagelinks):
    website_url = []
    for link in pagelinks:
        url_split = urlparse.urlparse(pagelinks)
        pagelinks_urlprotocol = url_split.scheme
        pagelinks_dns = url_split.netloc
        sim =  difflib.SequenceMatcher(None, dns, pagelinks_dns).ratio()
        if (urlprotocol == pagelinks_urlprotocol) and (sim > 0.65):
            website_url.append(link)
        unrepeat_url = url_unrepeat(website_url)
        return unrepeat_url

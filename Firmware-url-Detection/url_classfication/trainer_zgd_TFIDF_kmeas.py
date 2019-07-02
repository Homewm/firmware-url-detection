# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=433)


def getTokens(input):
    tokensBySlash = str(input.encode('utf-8')).split('/')	#get tokens after splitting by slash
    # print tokensBySlash
    allTokens = []
    for i in tokensBySlash:
        tokens = str(i).split('-')	#get tokens after splitting by dash
        tokensByDot = []

        for j in range(0,len(tokens)):
            tempTokens = str(tokens[j]).split('_')	#get tokens after splitting by dot
            tokensByDot = tokensByDot + tempTokens

        allTokens = allTokens + tokens + tokensByDot
    allTokens = list(set(allTokens))	#remove redundant tokens
    # print allTokens
    list_comm = ['http:','https:','com','www']
    for i in list_comm:
        if i in allTokens:
            allTokens.remove(i)	#removing .com since it occurs a lot of times and it should not be included in our feature

    return allTokens


###有的时候可以使滑动窗口的方法，ngrams。代替getTokens(input)
def get_ngrams(query):
    tempQuery = str(query)
    ngrams = []
    for i in range(0, len(tempQuery) - 3 + 1):
        ngrams.append(tempQuery[i:i + 3])
    return ngrams


def kmeans(weight):
    print 'kmeans之前矩阵大小： ' + str(weight.shape)
    weight = weight.tolil().transpose()
    # print weight
    # 同一组数据 同一个k值的聚类结果是一样的。保存结果避免重复运算
    try:
        with open('model_k' + str(k) + '.label', 'r') as input:
            print 'loading kmeans success'
            a = input.read().split(' ')
            self.label = [int(i) for i in a[:-1]]

    except Exception, e:
        print 'Start Kmeans '
        k = 80
        clf = KMeans(n_clusters=k, precompute_distances=False )
        s = clf.fit(weight)
        print s
        # 保存聚类的结果
        label = clf.labels_

        # with open('model/' + self.getname() + '.kmean', 'wb') as output:
        #     pickle.dump(clf, output)
        with open('model_k' + str(k) + '.label', 'w') as output:
            for i in label:
                output.write(str(i) + ' ')
    print 'kmeans 完成,聚成 ' + str(k) + '类'
    return weight

def transform(weight):

    from scipy.sparse import coo_matrix

    a = set()
    # 用coo存 可以存储重复位置的元素
    row = []
    col = []
    data = []
    # i代表旧矩阵行号 label[i]代表新矩阵的行号
    for i in range(len(label)):
        if label[i] in a:
            continue
        a.add(label[i])
        for j in range(i, len(label)):
            if label[j] == label[i]:
                temp = weight[j].rows[0]
                col += temp
                temp = [self.label[i] for t in range(len(temp))]
                row += temp
                data += weight[j].data[0]
    print row
    # print col
    # print data
    newWeight = coo_matrix((data, (row, col)), shape=(k, weight.shape[1]))
    return newWeight.transpose()


def TL():
    allurls = 'all_url_label.csv'  # path to our all urls file
    allurlscsv = pd.read_csv(allurls,',',error_bad_lines=False)	 #reading file
    allurlsdata = pd.DataFrame(allurlscsv)	#converting to a dataframe   ###数据格式化

    allurlsdata = np.array(allurlsdata)	#converting it into an array
    np.random.shuffle(allurlsdata)	#shuffling    ####随机排序

    y = [d[1] for d in allurlsdata]	 #all labels   ###所有的标签
    corpus = [d[0] for d in allurlsdata]	#all urls corresponding to a label (either good or bad)  ###所有的url

    vectorizer = TfidfVectorizer(tokenizer=getTokens)	#get a vector for each url but use our customized tokenizer ###添加过滤规则
    # count_vec = CountVectorizer(stop_words=None)
    # X = count_vec.fit_transform(corpus)  # get the X vector

    X = vectorizer.fit_transform(corpus)	#get the X vector
    # print X.shape    ###向量化后维度
    X = kmeans(X)
    X = transform(X)

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #split into training and testing set 80/20 ratio
    #
    # lgs = LogisticRegression()	#using logistic regression
    # lgs.fit(X_train, y_train)
    # # print(lgs.score(X_test, y_test))	#pring the score. It comes out to be 98%
    # return vectorizer, lgs        ###返回向量和模型
    # # return count_vec, lgs


if __name__ == "__main__":
    # vectorizer, lgs = TL()
    TL()

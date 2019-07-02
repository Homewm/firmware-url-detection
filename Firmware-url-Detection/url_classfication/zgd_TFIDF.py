# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
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


def TL():
	allurls = 'all_url_label.csv'	#path to our all urls file
	allurlscsv = pd.read_csv(allurls,',',error_bad_lines=False)	 #reading file
	allurlsdata = pd.DataFrame(allurlscsv)	#converting to a dataframe   ###数据格式化

	allurlsdata = np.array(allurlsdata)	#converting it into an array
	np.random.shuffle(allurlsdata)	#shuffling    ####随机排序

	y = [d[1] for d in allurlsdata]	 #all labels   ###所有的标签
	corpus = [d[0] for d in allurlsdata]	#all urls corresponding to a label (either good or bad)  ###所有的url

	# vectorizer = TfidfVectorizer(tokenizer=getTokens)	#get a vector for each url but use our customized tokenizer ###添加过滤规则
	count_vec = CountVectorizer(stop_words=None)
	X = count_vec.fit_transform(corpus)  # get the X vector

	# X = vectorizer.fit_transform(corpus)	#get the X vector

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)	#split into training and testing set 80/20 ratio

	lgs = LogisticRegression()	#using logistic regression
	lgs.fit(X_train, y_train)
	print(lgs.score(X_test, y_test))	#pring the score. It comes out to be 98%
	# return vectorizer, lgs        ###返回向量和模型
	return count_vec, lgs



if __name__ == "__main__":
	vectorizer, lgs = TL()

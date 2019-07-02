# -*- coding:utf-8 -*-


import pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import numpy
# from sklearn import svm
import svm
# from sklearn import cross_validation as cv
from sklearn.model_selection import cross_validate as cv
import matplotlib.pylab as plt
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas", lineno=570)


def return_nonstring_col(data_cols):
    cols_to_keep = []
    train_cols = []
    for col in data_cols:

        if col != 'url' and col != 'getContentType':
            # print col
            cols_to_keep.append(col)
            if col != 'firmware_bool' and col != 'result':
                train_cols.append(col)
    return [cols_to_keep, train_cols]


# ###svm分类
def svm_classifier(train, query, train_cols):      ###特征数据，带查询的特征数据，去除字符串的特征信息
    clf = svm.SVC()    ##分类器
    train[train_cols] = preprocessing.scale(train[train_cols])
    query[train_cols] = preprocessing.scale(query[train_cols])
    print clf.fit(train[train_cols], train['firmware_bool'])
    scores = cv.cross_val_score(clf, train[train_cols], train['firmware_bool'], cv=30)
    print('Estimated score SVM: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))
    query['result'] = clf.predict(query[train_cols])
    print query[['url', 'result']]


# def forest_classifier_gui(train, query, train_cols):
#     rf = RandomForestClassifier(n_estimators=150)
#     print rf.fit(train[train_cols], train['malicious'])
#     query['result'] = rf.predict(query[train_cols])
#     print query[['URL', 'result']].head(2)
#     return query['result']


def forest_classifier(train, query, train_cols):
    rf = RandomForestClassifier(n_estimators=150)
    print rf.fit(train[train_cols], train['firmware_bool'])
    scores = cv.cross_val_score(rf, train[train_cols], train['firmware_bool'], cv=30)
    print('Estimated score RandomForestClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))
    query['result'] = rf.predict(query[train_cols])
    print query[['url', 'result']]


def train(db, test_db):   ###url提取的特征，待测试的特征
    query_csv = pandas.read_csv(test_db)   ###读取和加载查询的特征集
    cols_to_keep, train_cols = return_nonstring_col(query_csv.columns)  ###cols_to_keep为特征列名，两个值一样
    query = query_csv[cols_to_keep]   ###根据列名称输出内容
    # print train_cols

    train_csv = pandas.read_csv(db)  ###读取和加载数据
    cols_to_keep, train_cols = return_nonstring_col(train_csv.columns)  ###去除带字符串的情况
    train = train_csv[cols_to_keep]   ###根据列名输出所有内容


    svm_classifier(train_csv, query_csv, train_cols)   ###特征数据，查询的特征数据，去除带字符串的情况
    forest_classifier(train_csv, query_csv, train_cols)


if __name__ == '__main__':
    t = train('url_features.csv', 'query_features.csv')
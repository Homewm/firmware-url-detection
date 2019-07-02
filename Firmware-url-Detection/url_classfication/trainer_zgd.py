# -*- coding:utf-8 -*-
'''训练svm分类器'''

import pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split  # 划分数据 交叉验证
from sklearn.neighbors import KNeighborsClassifier   # 一个简单的模型，只有K一个参数，类似K-means
import matplotlib.pylab as plt
from sklearn.ensemble import GradientBoostingClassifier
# from keras.layers.core import Dense, Activation
# from keras.models import load_model
# from keras import Sequential

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas", lineno=570)
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=196)
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=433)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sklearn", lineno=268)


###过滤掉字符串内容
def return_nonstring_col(data_cols):
    cols_to_keep = []
    train_cols = []
    for col in data_cols:
        if col != 'url' and col != 'getContentType':
            cols_to_keep.append(col)     ###除去url和文件内容类型
            if col != 'firmware_bool' and col != 'result':
                train_cols.append(col)   ###除去标签和结果
    return [cols_to_keep, train_cols]


# ###svm
def svm_classifier(train_csv, cols_to_keep, train_cols):      ###特征数据，带查询的特征数据，去除字符串的特征信息
    clf = svm.SVC()    ##分类器
    train_csv[train_cols] = preprocessing.scale(np.asarray(train_csv[train_cols]))    ###数据转换  解决了数据转换的问题
    clf.fit(train_csv[train_cols], train_csv['firmware_bool'])
    scores = cross_val_score(clf, train_csv[train_cols], train_csv['firmware_bool'], cv=10)   ###交叉验证
    print scores
    print('Estimated score SVM: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std()/2))
    print "---------END---------"


# ##RandomForest
def randomForest_classifier(train_csv, cols_to_keep, train_cols):
    clf = RandomForestClassifier(n_estimators=150)
    clf.fit(train_csv[train_cols], train_csv['firmware_bool'])
    scores = cross_val_score(clf, train_csv[train_cols], train_csv['firmware_bool'], cv=10)
    print scores
    print('Estimated score RandomForestClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std()/2))
    print "---------END---------"


# ##LogisticRegression
def logisticRegression_classifier(train_csv, cols_to_keep, train_cols):
    clf = LogisticRegression()
    clf.fit(train_csv[train_cols], train_csv['firmware_bool'])
    scores = cross_val_score(clf, train_csv[train_cols], train_csv['firmware_bool'], cv=10)
    print scores
    print ('Estimated score LogisticRegressionClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std()/2))
    print "---------END---------"


# ##DecisionTreeClassifier
def decisionTree_classifier(train_csv, cols_to_keep, train_cols):
    tree = DecisionTreeClassifier()
    tree.fit(train_csv[train_cols], train_csv['firmware_bool'])
    # r = tree.predict(test)
    # err = abs(r - test_result)
    # acc = 1 - np.sum(err) / len(err)
    # print(acc)
    scores = cross_val_score(tree, train_csv[train_cols], train_csv['firmware_bool'], cv=10)
    print scores
    print ('Estimated score DecisionTreeClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))
    print "---------END---------"


## KNeighborsClassifier
def KNeighbors_classifier(train_csv, cols_to_keep, train_cols):
    X = train_csv[train_cols]
    y = train_csv['firmware_bool']
    # train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=1/3, random_state=3)
    cv_scores = []
    k_range = range(1, 31)
    for n in k_range:
        knn = KNeighborsClassifier(n_neighbors=n)   # 选择最优的K=3传入模型
        knn.fit(train_csv[train_cols], train_csv['firmware_bool'])
        scores = cross_val_score(knn, train_csv[train_cols], train_csv['firmware_bool'], cv=10, scoring='accuracy')
        cv_scores.append(scores.mean())
    plt.plot(k_range, cv_scores)
    plt.xlabel('K')
    plt.ylabel('Accuracy')  # 通过图像选择最好的参数
    plt.show()
    best_knn = KNeighborsClassifier(n_neighbors=3)   # 选择最优的K=3传入模型
    best_knn.fit(train_csv[train_cols], train_csv['firmware_bool'])
    scores = cross_val_score(best_knn, train_csv[train_cols], train_csv['firmware_bool'], cv=10, scoring='accuracy')
    print scores
    print ('Estimated score KNeighborsClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))
    print "---------END---------"


def GBDT_classifier(train_csv, cols_to_keep, train_cols):
    model = GradientBoostingClassifier()
    model.fit(train_csv[train_cols], train_csv['firmware_bool'])
    scores = cross_val_score(model, train_csv[train_cols], train_csv['firmware_bool'], cv=10, scoring='accuracy')
    print scores
    print ('Estimated score KNeighborsClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))
    print "---------END---------"

# def keras_classifier(train_csv, cols_to_keep, train_cols):
#     net = Sequential()
#     net.add(Dense(5, activation='relu', input_dim=5))
#     net.add(Dense(16, activation='relu'))
#     net.add(Dense(1, activation='sigmoid'))
#     net.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#     net.fit(train_csv[train_cols], train_csv['firmware_bool'], epochs=100, batch_size=1)
#     scores = cross_val_score(net, train_csv[train_cols], train_csv['firmware_bool'], cv=10, scoring='accuracy')
#     print scores
#
#     # net.save("model.h5")
#     # net = load_model("model.h5")                  #载入训练好的模型
#     # predict_result = net.predict_classes(test_set)
#     # error = abs(true_result - predict_result)
#     # err = np.sum(error)
#     # accuracy = 1 - err / len(test_set)
#     # print(accuracy)


# def forest_classifier_gui(train, query, train_cols):
#     rf = RandomForestClassifier(n_estimators=150)
#     print rf.fit(train[train_cols], train['malicious'])
#     query['result'] = rf.predict(query[train_cols])
#     print query[['URL', 'result']].head(2)
#     return query['result']


def train(url_features):   ###url提取的特征，待测试的特征
    train_csv = pandas.read_csv(url_features)   ###读取和加载查询的特征集
    cols_to_keep, train_cols = return_nonstring_col(train_csv.columns)  ###cols_to_keep为特征列名，两个值不一样，一个是包含了标签，一个是没有包含标签
    train = train_csv[cols_to_keep]   ###根据列名称输出内容，包含标签值


    ####使用各种模型区分
    svm_classifier(train_csv, cols_to_keep, train_cols)
    randomForest_classifier(train_csv, cols_to_keep, train_cols)
    logisticRegression_classifier(train_csv, cols_to_keep, train_cols)
    decisionTree_classifier(train_csv, cols_to_keep, train_cols)
    KNeighbors_classifier(train_csv, cols_to_keep, train_cols)
    GBDT_classifier(train_csv, cols_to_keep, train_cols)
    # keras_classifier(train_csv, cols_to_keep, train_cols)



    # query_csv = pandas.read_csv(test_db)   ###读取和加载查询的特征集
    # cols_to_keep, train_cols = return_nonstring_col(query_csv.columns)  ###cols_to_keep为特征列名，两个值不一样，一个是包含了标签，一个是没有包含标签
    # query = query_csv[cols_to_keep]   ###根据列名称输出内容，包含标签值
    #
    # svm_classifier(query_csv, cols_to_keep, train_cols)


    # svm_classifier(train_csv, query_csv, train_cols)   ###特征数据，查询的特征数据，去除带字符串的情况
    # forest_classifier(train_csv, query_csv, train_cols)


if __name__ == '__main__':
    t = train('url_features_zgd_1201.csv')
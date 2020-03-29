import os
import sys
from settings import *
from Extract_U_file import *
from sklearn.svm import OneClassSVM
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd


def compute_fpr_tpr(userid, positive_scores, negative_scores, plot = True):
    zeros = np.zeros(len(negative_scores))
    ones = np.ones(len(positive_scores))
    y = np.concatenate((zeros, ones))
    scores = np.concatenate((negative_scores, positive_scores))
    fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=1)
    roc_auc = metrics.auc(fpr, tpr)
    if( plot == True ):
        plot_ROC( userid, fpr, tpr, roc_auc )
    return roc_auc


def plot_ROC(userid, fpr, tpr, roc_auc):
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
    lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC - user ' + userid)
    plt.legend(loc="lower right")
    plt.show()


def load_datas(dataset):

    data = pd.read_csv(dataset)    
    y = data.author
    authors_list = unique(y)
    authors_list.sort()
    SIZE = len(authors_list)
    
    for i in range (0,SIZE):

        users = data.loc[data['author'] == authors_list[i]]
        indexNames = data[data['author'] == authors_list[i]].index
        other_users_array = data.drop(indexNames)
        X = users.drop("author",axis = 1)
        X =  X.drop("function",axis=1)
        other_users_array = other_users_array.drop("author",axis = 1)
        other_users_array = other_users_array.drop("function",axis = 1)
        Num_Of_Functions = users.shape[0]
        user_train = X.head(int(Num_Of_Functions*2/3))
        user_test = X.tail(Num_Of_Functions - user_train.shape[0])

        clf = OneClassSVM(gamma='scale').fit(user_train)
        clf.fit(user_train)
        positive_scores = clf.score_samples(user_test)
        negative_scores = clf.score_samples(other_users_array)

        print(str(authors_list[i]) + " : " +str('%.2f' % compute_fpr_tpr(authors_list[i],positive_scores,negative_scores)))


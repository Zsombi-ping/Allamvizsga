import os
import sys
from settings import *
from Extract_U_file import *
from sklearn.svm import OneClassSVM
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import statistics 


result_table = pd.DataFrame(columns=['author', 'fpr','tpr','auc'])

def compute_fpr_tpr(userid, positive_scores, negative_scores, plot = False):
    zeros = np.zeros(len(negative_scores))
    ones = np.ones(len(positive_scores))
    y = np.concatenate((zeros, ones))
    scores = np.concatenate((negative_scores, positive_scores))
    fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=1)
    roc_auc = metrics.auc(fpr, tpr)
    global result_table

    result_table = result_table.append({'author': userid,
                                            'fpr':fpr, 
                                            'tpr':tpr, 
                                            'auc':roc_auc}, ignore_index=True)

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


def load_datas(dataset,Processing_Unit, n=10): # 0 < n <= 100

    S = 0
    #data = pd.read_csv(dataset)
    data = dataset
    y = data.author
    authors_list = unique(y)
    authors_list.sort()
    SIZE = len(authors_list)
    roc_array = []
    for i in range (0,SIZE):

        users = data.loc[data['author'] == authors_list[i]]
        indexNames = data[data['author'] == authors_list[i]].index
        other_users_array = data.drop(indexNames)
        X = users.drop("author",axis = 1)
        other_users_array = other_users_array.drop("author",axis = 1)
        if Processing_Unit == "FUNCTION":
            X =  X.drop("function",axis=1)
            other_users_array = other_users_array.drop("function",axis = 1)
        Num_Of_Functions = users.shape[0]
        user_train = X.head(int(Num_Of_Functions*2/3))
        user_test = X.tail(Num_Of_Functions - user_train.shape[0])

        clf = OneClassSVM(gamma='scale').fit(user_train)
        clf.fit(user_train)
        positive_scores = clf.score_samples(user_test)
        negative_scores = clf.score_samples(other_users_array)

        #print(str(authors_list[i]) + " : " +str('%.2f' % compute_fpr_tpr(authors_list[i],positive_scores,negative_scores)))
        val = compute_fpr_tpr(authors_list[i],positive_scores,negative_scores)
        S+=val
        roc_array.append(val)

    avg = S/SIZE
    #print("avg : " + str('%.4f' % avg))
    w = open("C:/Users/Zsombi/Desktop/Allamvizsga/Programs/aux_res.txt",'w')
    w.truncate(0)
    w.write("avg AUC : " + str('%.4f' % avg))
    w.close()
    #print("stdev: " + str('%.4f' % statistics.stdev(roc_array)))


    
    # global result_table
    # result_table.set_index('author', inplace=True)

    # fig = plt.figure(figsize=(10,10))

    # j = 0
    # for i in result_table.index:
    #     plt.plot(result_table.loc[i]['fpr'], result_table.loc[i]['tpr'], label="{}, AUC={:.3f}".format(i, result_table.loc[i]['auc']))
    #     j+=1
    #     if j==n:
    #         break

    # plt.plot([0,1], [0,1], color='black', linestyle='--')

    # plt.xticks(np.arange(0.0, 1.1, step=0.1))
    # plt.xlabel("False Positive Rate", fontsize=15)

    # plt.yticks(np.arange(0.0, 1.1, step=0.1))
    # plt.ylabel("True Positive Rate", fontsize=15)

    # plt.title('ROC Curve Analysis', fontweight='bold', fontsize=15)
    # plt.legend(prop={'size':10}, loc='lower right')

    # plt.show()
    

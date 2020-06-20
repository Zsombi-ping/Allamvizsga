import os
import sys
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import eli5
from eli5.sklearn import PermutationImportance
import settings 

def permutation_importance(dataset, Processing_Unit):
    data = dataset      
    y = data.author
    X = data.drop("author",axis = 1)
    if Processing_Unit == "FUNCTION":
        X = X.drop("function", axis = 1)
    
    feature_names = [i for i in data.columns if data[i].dtype in [np.int64]]
    X = data[feature_names]
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
    my_model = RandomForestClassifier(n_estimators=100,
                                  random_state=0).fit(train_X, train_y)
                                
    perm = PermutationImportance(my_model, random_state=1).fit(val_X, val_y)

    #print(eli5.format_as_text(eli5.explain_weights(perm,feature_names = val_X.columns.tolist())))
    w = open(settings.aux_perm,'w')
    w.truncate(0)
    w.write(eli5.format_as_text(eli5.explain_weights(perm,feature_names = val_X.columns.tolist())))
def norm (dataset,Proc_unit):

    X = pd.read_csv(dataset)
    permutation_importance(X,Proc_unit)
    authors = X['author']
    if Proc_unit == "FUNCTION":
        func = X['function']
        X = X.drop("function",axis = 1)
    X = X.drop("author",axis = 1)
    scaler = MinMaxScaler()
    features = scaler.fit_transform(X)
    features = pd.DataFrame(features)
    features['author'] = authors
    if Proc_unit == "FUNCTION":
        features['function'] = func
    #print(features)
    return features 
import sys
import os
import settings
from Extract_U_file import *
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import eli5
from eli5.sklearn import PermutationImportance

def KfoldVal(dataset,Processing_Unit):

    data = dataset
        
    y = data.author
    X = data.drop("author",axis = 1)
    if Processing_Unit == "FUNCTION":
        X = X.drop("function", axis = 1)

    model = RandomForestClassifier(n_estimators=100)   
  
    scoring = ['accuracy']
    num_folds = 3
    scores = cross_val_score(model , X ,y , cv = num_folds)
    #print("Accuracy : %0.4f   Dev : %0.4f" % (scores.mean() , scores.std())) 
    w = open(settings.aux_res,'w')
    w.truncate(0)
    w.write("Accuracy : %0.4f   Dev : %0.4f" % (scores.mean() , scores.std()))
    w.close()

    



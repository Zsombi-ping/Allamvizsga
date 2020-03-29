import sys
import os
from settings import *
from Extract_U_file import *
from sklearn.ensemble import RandomForestClassifier

def KfoldVal(dataset,Processing_Unit):

    data = pd.read_csv(dataset)
        
    y = data.author
    X = data.drop("author",axis = 1)
    if Processing_Unit == "FUNCTION":
        X = X.drop("function", axis = 1)

    model = RandomForestClassifier(n_estimators=100)   
    #model =  DecisionTreeClassifier(random_state=30)
    scoring = ['accuracy']
    num_folds = 3
    #scores = cross_validate(model, X, y, scoring=scoring, cv=num_folds) 
    scores = cross_val_score(model , X ,y , cv = num_folds)

    # for i in range(0,num_folds):
    #     print('\tFold '+str(i+1)+':' + str(scores['test_accuracy'][ i ]))
        
    print("accuracy : %0.4f (%0.4f)" % (scores.mean() , scores.std())) 

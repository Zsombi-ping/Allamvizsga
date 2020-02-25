import sys
sys.path.append('C:/Users/Zsombi/Desktop/Allamvizsga/Programs')
from settings import *
from Building_AST_and_unigrams import *

def KfoldVal(load_file):

        data = pd.read_csv(load_file)
        
        y = data.author
        X = data.drop("author",axis = 1)

        #model = RandomForestClassifier(n_estimators=100)   
        model =  DecisionTreeClassifier(random_state=30)
        scoring = ['accuracy']
        num_folds = 3
        #scores = cross_validate(model, X, y, scoring=scoring, cv=num_folds) 
        scores = cross_val_score(model , X ,y , cv = num_folds)

        # for i in range(0,num_folds):
        #     print('\tFold '+str(i+1)+':' + str(scores['test_accuracy'][ i ]))
        
        print("accuracy : %0.4f (%0.4f)" % (scores.mean() , scores.std())) 


def main():

    #KfoldVal(Bigrams_AST_dataset)
    #KfoldVal (big_dataset)
    #KfoldVal(small_dataset)
    KfoldVal (Bigrams_AST_dataset)

if __name__ == '__main__':
    main()

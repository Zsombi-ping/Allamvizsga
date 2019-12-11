import subprocess
import sys
import re
import os
from os import listdir
from os.path import isfile, join
import glob
import pandas as pd
import numpy as np
import signal 
import timeout_decorator
from interruptingcow import timeout
import time
import eventlet
from threading import Timer
import traceback
import threading
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split , cross_validate









def unique(list1): 
      
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    return unique_list



def search_func_names(filename):
    f_names = []
    file_o=open(filename,encoding='utf8', errors='ignore')   
    content=file_o.read()                
    for line in content.split('\n'):
        if re.findall(r'(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+\s*)\(\s*(?:(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))(?:\s*,\s*(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))*\s*\)', line) or re.findall(r'[a-z]+\s+[a-z]+\s*\(\s*\)',line):
            aux_list = line.split('(')
            cutted_list = aux_list[0]
            space_list = cutted_list.split()
            f_names.append(space_list[len(space_list)-1].strip())
        if "main" in line:
            f_names.append("main")
    return f_names



def redirect_to_file(text,outfile):
    #print("\n\n----------REDIRECTING------------\n\n")
    original = sys.stdout
    sys.stdout = open(outfile, 'a',encoding='utf8', errors='ignore')
    for line in text.split('\n'):
        print(line)
    sys.stdout = original



def create_subprocess_file_pipe(filepath,outfile):

    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    text = stdout
    StrTxt = text.decode("utf-8")
    redirect_to_file(StrTxt,outfile)
 


def build_ast(list_of_names,filename,outfile,filepath):
    
    f = open(outfile,"w",encoding='utf8', errors='ignore')
    f.truncate(0)
    for name in list_of_names:
        build_command = "clang-check -extra-arg=-std=c++1y -ast-dump -ast-dump-filter="
        build_command = build_command + name + " " + filename
        f = open(filepath, "w")
        f.write(build_command)
        f.close()
        #print("\n\n----------BUILD_AST------------\n\n")
        create_subprocess_file_pipe(filepath,outfile)



def counting_attributes(folder_path,outfile,filepath,wrong_files):

    w = open(wrong_files,'w')
    w.truncate(0)
    w.close()
    attributes = 'AbiTagAttr,AccessSpecDecl,ArraySubscriptExpr,BinaryOperator,CStyleCastExpr,CXXBoolLiteralExpr,CXXConstructExpr,CXXConstructorDecl,CXXConversionDecl,CXXCtorInitializer,CXXDependentScopeMemberExpr,CXXDestructorDecl,CXXFunctionalCastExpr,CXXMemberCallExpr,CXXMethodDecl,CXXOperatorCallExpr,CXXRecordDecl,CXXStaticCastExpr,CXXTemporaryObjectExpr,CXXThisExpr,CXXUnresolvedConstructExpr,CallExpr,ClassTemplateSpecialization,CompoundAssignOperator,CompoundStmt,ConditionalOperator,ConstantExpr,CopyAssignment,CopyConstructor,DeclRefExpr,DeclStmt,DefaultConstructor,DefinitionData,DependentNameType,Destructor,EnumConstantDecl,ExprWithCleanups,FieldDecl,ForStmt,FormatAttr,FriendDecl,FunctionDecl,FunctionTemplateDecl,ImplicitCastExpr,IntegerLiteral,MaterializeTemporaryExpr,MemberExpr,MoveAssignment,MoveConstructor,NoThrowAttr,NullStmt,public,ParenExpr,ParenListExpr,ParmVarDecl,PureAttr,ReturnStmt,StringLiteral,TemplateArgument,TemplateSpecializationType,TemplateTypeParmDecl,TypedefDecl,UnaryOperator,UnresolvedLookupExpr,UsingDecl,UsingShadowDecl,WhileStmt'
    atrib_list = attributes.split(',')
    names = []
    author = []
    dictionary = {}
    for key in atrib_list:
        dictionary[key] = []
    users_folder = os.listdir(folder_path)
    for folder in users_folder:
        folder_str = ""
        folder_str = folder_path+"/"+folder+"/*.cpp"
        for file in glob.iglob(folder_str):  
            try:
                start = time.time()
                name = search_func_names(file)
                names = unique(name)
                if len(names) == 0 :
                    w = open(wrong_files,'a')
                    w.write(folder+" : "+file+'\n')
                    w.close()
                    for attr in atrib_list:
                        refresh_list = dictionary[attr]
                        refresh_list.append(0)
                        dictionary[attr]=refresh_list
                    author.append(folder)
                    continue  
                        
                build_ast(names,file,outfile,filepath)
                f = open(outfile,"r",encoding='utf8', errors='ignore')
                content = f.read()
                f.close()
                for attr in atrib_list:
                    count = content.count(attr)
                    refresh_list = dictionary[attr]
                    refresh_list.append(count)
                    dictionary[attr]=refresh_list
                author.append(folder)
                end = time.time()
                print(end-start)
                print("SECONDS")
            except RuntimeError:
                print("CANNOT DECODE FILE")
                continue
            except IndexError:
                w = open(wrong_files,'a')
                w.write("#####################################      "+folder+" : "+file+'\n')
                w.close()
                
    dictionary['authors'] = author
    df = pd.DataFrame(dictionary)
    return df
        


def KfoldVal(load_file):

        data = pd.read_csv(load_file)
        
        y = data.authors
        X = data.drop("authors",axis = 1)

        #model = RandomForestClassifier(n_estimators=100)   
        model =  DecisionTreeClassifier(random_state=30)
        scoring = ['accuracy']
        num_folds = 3
        scores = cross_validate(model, X, y, scoring=scoring, cv=num_folds) 


        for i in range(0,num_folds):
            print('\tFold '+str(i+1)+':' + str(scores['test_accuracy'][ i ]))



def main():
        
    #  folderpath = "C:/Users/Zsombi/Desktop/Allamvizsga/DIPLOMA/data/100_users"
    #  filepath="C:/Users/Zsombi/Desktop/Allamvizsga/foo.bat"
    #  outfile = 'C:/Users/Zsombi/Desktop/Allamvizsga/out.log'
    #  wrong_files = 'C:/Users/Zsombi/Desktop/Allamvizsga/wrong_files.log'
    #  df = counting_attributes(folderpath,outfile,filepath,wrong_files)
    #  print(frame.shape)
    #  export_csv = df.to_csv (r'C:/Users/Zsombi/Desktop/Allamvizsga/dataframe_export.csv', index = None, header=True)
    #  print(df)
     load_file = 'C:/Users/Zsombi/Desktop/Allamvizsga/dataframe_export.csv'
     KfoldVal(load_file) 

if __name__ == '__main__':
    main()

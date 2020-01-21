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
from settings import *








def unique(list1): 
      
    list_set = set(list1) 
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
            continue
        if "main" in line:
            f_names.append("main")
    return f_names



def redirect_to_file(text,outfile):

    original = sys.stdout
    sys.stdout = open(outfile, 'a',encoding='utf8', errors='ignore')
    for line in text.split('\n'):
        print(line)
    sys.stdout = original



def create_subprocess_file_pipe(filepath,outfile):

    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    text = stdout
    StrTxt = text.decode("utf-8").strip()
    redirect_to_file(StrTxt,outfile)
 


def build_ast(list_of_names,filename,outfile,filepath):
    
    f = open(outfile,"w",encoding='utf8', errors='ignore')
    f.truncate(0)
    for name in list_of_names:
        build_command = clang_command
        build_command = build_command + name + " " + filename
        f = open(filepath, "w")
        f.write(build_command)
        f.close()
        create_subprocess_file_pipe(filepath,outfile)



def counting_attributes(folder_path,outfile,filepath,wrong_files):

    i = 0
    w = open(wrong_files,'w')
    w.truncate(0)
    w.close()
    attributes = 'AbiTagAttr,AccessSpecDecl,ArraySubscriptExpr,BinaryOperator,CStyleCastExpr,CXXBoolLiteralExpr,CXXConstructExpr,CXXConstructorDecl,CXXConversionDecl,CXXCtorInitializer,CXXDependentScopeMemberExpr,CXXDestructorDecl,CXXFunctionalCastExpr,CXXMemberCallExpr,CXXMethodDecl,CXXOperatorCallExpr,CXXRecordDecl,CXXStaticCastExpr,CXXTemporaryObjectExpr,CXXThisExpr,CXXUnresolvedConstructExpr,CallExpr,ClassTemplateSpecialization,CompoundAssignOperator,CompoundStmt,ConditionalOperator,ConstantExpr,CopyAssignment,CopyConstructor,DeclRefExpr,DeclStmt,DefaultConstructor,DefinitionData,DependentNameType,Destructor,EnumConstantDecl,ExprWithCleanups,FieldDecl,ForStmt,FormatAttr,FriendDecl,FunctionDecl,FunctionTemplateDecl,ImplicitCastExpr,IntegerLiteral,MaterializeTemporaryExpr,MemberExpr,MoveAssignment,MoveConstructor,NoThrowAttr,NullStmt,public,ParenExpr,ParenListExpr,ParmVarDecl,PureAttr,ReturnStmt,StringLiteral,TemplateArgument,TemplateSpecializationType,TemplateTypeParmDecl,TypedefDecl,UnaryOperator,UnresolvedLookupExpr,UsingDecl,UsingShadowDecl,WhileStmt'
    atrib_list = attributes.split(',')
    names = []
    author = []
    all_author = []

    dictionary_all = {}
    dictionary_first_100 = {}
    for key in atrib_list:
        dictionary_first_100[key] = []
        dictionary_all[key] = []

    users_folder = os.listdir(folder_path)
    for folder in users_folder:
        folder_str = ""
        folder_str = folder_path+"/"+folder+"/*.cpp"
        file_check = True
        for file in glob.iglob(folder_str):  
            name = search_func_names(file)
            names = unique(name)
            if len(names) == 0 :
                file_check = False
                w = open(wrong_files,'a')
                w.write(folder+'\n')
                w.close()
                break
        if file_check == True:
            i = i + 1
            for file in glob.iglob(folder_str):  
                try:
                    print(file)
                    name = search_func_names(file)
                    names = unique(name)
                    build_ast(names,file,outfile,filepath)
                    f = open(outfile,"r",encoding='utf8', errors='ignore')
                    content = f.read()
                    f.close()
                    if i<=100 :         
                        for attr in atrib_list:
                            count = content.count(attr)
                            refresh_list = dictionary_first_100[attr]
                            refresh_list.append(count)
                            dictionary_first_100[attr]=refresh_list
                        author.append(folder)
                    for attr in atrib_list:
                        count = content.count(attr)
                        refresh_list = dictionary_all[attr]
                        refresh_list.append(count)
                        dictionary_all[attr] = refresh_list
                    all_author.append(folder)             
                except RuntimeError:
                    print("CANNOT DECODE FILE")
                    continue
                except IndexError:
                    w = open(wrong_files,'a')
                    w.write("#####################################      "+folder+" : "+file+'\n')
                    w.close()
                except UnicodeDecodeError:
                    print("CANNOT DECODE FILE")

    dictionary_all['authors'] = all_author
    dictionary_first_100['authors'] = author
    df_100 = pd.DataFrame(dictionary_first_100)
    df_all = pd.DataFrame(dictionary_all)
    return (df_100,df_all)
        


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



def clear_junks_from_dataset(dataset):
     
    wrong_authors = []
    dataframe = pd.read_csv(dataset)
    author_list = dataframe.authors
    authors_unique = unique(author_list)
    f = open(dataset,"r")
    content = f.read()
    f.close()
    for author in authors_unique:
        count = content.count(author)
        if count % 9 !=0 :
            wrong_authors.append(author)     
    f = open (dataset,"w")
    for line in content.split('\n'):
        accept = True
        for author in wrong_authors:
            if author in line:
                accept = False
                break
        if accept == True:
            f.write(line+'\n')
    f.close()




def main():
    
    #df_100 , df_all = counting_attributes(folderpath,outfile,filepath,wrong_files)
    #df_100.to_csv (small_dataset, index = None, header=True)
    #df_all.to_csv (big_dataset, index = None, header=True)
    #load_file = big_dataset
    #KfoldVal(load_file) 
    #clear_junks_from_dataset(big_dataset)
    name = search_func_names("C:/Users/Zsombi/Desktop/Allamvizsga/main.cpp")
    print(name)



if __name__ == '__main__':
    main()

# Extracting Unigrams, Bigrams and Handcrafted features from functions for each file

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
from sklearn.model_selection import train_test_split , cross_validate , cross_val_score
from settings import *
from bigrams_indent import *
from Handcrafted_features_function import *


PRINT_HEADER_BIGRAM = True
PRINT_HEADER_FEATURES = True

# Remove duplicated elements

def unique(list1): 
      
    list_set = set(list1) 
    unique_list = (list(list_set)) 
    return unique_list


# Extract function names from file

def search_func_names(filename):
    comment = False
    f_names = []
    file_o=open(filename,encoding='utf8', errors='ignore')   
    content=file_o.read()                
    for line in content.split('\n'):
        if '/*' in line:
            comment = True
        if '*/' in line:
            comment = False
        if comment == True:
            continue
        if re.findall(r'(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+\s*)\(\s*(?:(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))(?:\s*,\s*(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))*\s*\)', line) or re.findall(r'[a-z]+\s+[a-z]+\s*\(\s*\)',line):
            aux_list = line.split('(')
            cutted_list = aux_list[0]
            space_list = cutted_list.split()
            if len(space_list) < 2 or space_list[0] == '//':
                continue
            f_names.append(space_list[len(space_list)-1].strip())
            continue
        if re.findall(r'\s*[\w_][\w\d_]*\s*.*\s*[\w_][\w\d_]*\s*\(.*\)\s*$',line):
             if 'if' not in line and 'for' not in line and 'while' not in line and 'switch' not in line and 'min' not in line and 'max' not in line and 'pragma' not in line and 'define' not in line:
                aux_list = line.split('(')
                cutted_list = aux_list[0]
                space_list = cutted_list.split()
                if len(space_list) < 2 or space_list[0] == '//':
                    continue
                f_names.append(space_list[len(space_list)-1].strip())
                continue
    return f_names


# Redirecting standard output into a file

def redirect_to_file(text,outfile):

    i = 0
    original = sys.stdout
    sys.stdout = open(outfile, 'w',encoding='utf8', errors='ignore')
    for line in text.split('\n'):
        print(line)
    sys.stdout = original

# Executing shell command for redirection 

def create_subprocess_file_pipe(filepath,outfile):

    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    text = stdout
    StrTxt = text.decode("utf-8").strip()
    redirect_to_file(StrTxt,outfile)
 
# Truncate output file and creating the command string, then start writeing into

def build_ast(name,filename,outfile,filepath):
    
    f = open(outfile,"w",encoding='utf8', errors='ignore')
    f.truncate(0)

    build_command = clang_command
    build_command = build_command + name + " " + filename
    f = open(filepath, "w")
    f.write(build_command)
    f.close()
    create_subprocess_file_pipe(filepath,outfile)

# Extract CLANG AST nodes from the created output

def counting_attributes(folder_path,outfile,filepath,wrong_files):

    index_counter_bigram = 1
    index_counter_features = 1
    csv_file_bigram = GCJ_100_bigrams_functions
    csv_file_features = GCJ_100_features_functions

    i = 0
    w = open(wrong_files,'w')
    w.truncate(0)
    w.close()
    attributes = 'AbiTagAttr,AccessSpecDecl,ArraySubscriptExpr,BinaryOperator,CStyleCastExpr,CXXBoolLiteralExpr,CXXConstructExpr,CXXConstructorDecl,CXXConversionDecl,CXXCtorInitializer,CXXDependentScopeMemberExpr,CXXDestructorDecl,CXXFunctionalCastExpr,CXXMemberCallExpr,CXXMethodDecl,CXXOperatorCallExpr,CXXRecordDecl,CXXStaticCastExpr,CXXTemporaryObjectExpr,CXXThisExpr,CXXUnresolvedConstructExpr,CallExpr,ClassTemplateSpecialization,CompoundAssignOperator,CompoundStmt,ConditionalOperator,ConstantExpr,CopyAssignment,CopyConstructor,DeclRefExpr,DeclStmt,DefaultConstructor,DefinitionData,DependentNameType,Destructor,EnumConstantDecl,ExprWithCleanups,FieldDecl,ForStmt,FormatAttr,FriendDecl,FunctionDecl,FunctionTemplateDecl,ImplicitCastExpr,IntegerLiteral,MaterializeTemporaryExpr,MemberExpr,MoveAssignment,MoveConstructor,NoThrowAttr,NullStmt,public,ParenExpr,ParenListExpr,ParmVarDecl,PureAttr,ReturnStmt,StringLiteral,TemplateArgument,TemplateSpecializationType,TemplateTypeParmDecl,TypedefDecl,UnaryOperator,UnresolvedLookupExpr,UsingDecl,UsingShadowDecl,WhileStmt'
    atrib_list = attributes.split(',')
    names = []
    author = []
    function = []
    dictionary_first_100 = {}

    for key in atrib_list:
        dictionary_first_100[key] = []


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
                    names.sort()
                    
                    for name in names:
                        build_ast(name,file,outfile,filepath)
                        print("\n\n"+str(name)+"\n\n")
                        
                        # Save datas into CSV file
                       
                        global PRINT_HEADER_BIGRAM
                        global PRINT_HEADER_FEATURES

                        csv_columns_bigram , bigrams  = bigrams_by_function(outfile,name)
                        csv_columns_features , features  = extract_function_handcrafted(file,name,names,outfile)
                        
                        bigrams['author'] = folder 
                        bigrams['function'] = name
                        features['author'] = folder 
                        features['function'] = name
                        
                        df_bigram=pd.DataFrame(bigrams,index=[index_counter_bigram])
                        df_features=pd.DataFrame(features,index=[index_counter_features])
                       
                        if PRINT_HEADER_BIGRAM:
                            df_bigram.to_csv(csv_file_bigram, mode = 'w', header=csv_columns_bigram, index = False) 
                            PRINT_HEADER_BIGRAM = False
                        else:
                            df_bigram.to_csv(csv_file_bigram, mode = 'a', header = False, index = False) 
                        
                        
                        if PRINT_HEADER_FEATURES:
                            df_features.to_csv(csv_file_features, mode = 'w',float_format='%.2f', header=csv_columns_features, index = False) 
                            PRINT_HEADER_FEATURES = False
                        else:
                            df_features.to_csv(csv_file_features, mode = 'a',float_format='%.2f', header = False, index = False) 
                        

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
                            function.append(name)
                except RuntimeError:
                    print("CANNOT DECODE FILE")
                    continue
                except IndexError:
                    w = open(wrong_files,'a')
                    w.write("#####################################      "+folder+" : "+file+'\n')
                    w.close()
                except UnicodeDecodeError:
                    print("CANNOT DECODE FILE")
        if i == 100:
            break

    dictionary_first_100['author'] = author
    dictionary_first_100['function'] = function
    df_100 = pd.DataFrame(dictionary_first_100)

    return df_100
        

def main():
    
    df_100 = counting_attributes(folderpath,outfile,filepath,wrong_files)
    df_100.to_csv (GCJ_100_unigram_functions, index = None, header=True)

    
if __name__ == '__main__':
    main()

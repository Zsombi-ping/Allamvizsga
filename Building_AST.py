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
        if re.findall(r'(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+)\(\s*(?:(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))(?:\s*,\s*(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))*\s*\){?', line):
            aux_list = line.split()
            name = aux_list[1]
            func_name = name.split('(')
            f_names.append(func_name[0])   
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



def counting_attributes(folder_path,outfile,filepath):

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
    dictionary['authors'] = author
    df = pd.DataFrame(dictionary)
    return df
        


def main():
        
    folderpath = "C:/Users/Zsombi/Desktop/Allamvizsga/DIPLOMA/data/100_users"
    filepath="C:/Users/Zsombi/Desktop/Allamvizsga/foo.bat"
    outfile = 'C:/Users/Zsombi/Desktop/Allamvizsga/out.log'
    df = counting_attributes(folderpath,outfile,filepath)
    #print(frame.shape)
    export_csv = df.to_csv (r'C:/Users/Zsombi/Desktop/Allamvizsga/dataframe_export.csv', index = None, header=True)
    print(df)
    

if __name__ == '__main__':
    main()
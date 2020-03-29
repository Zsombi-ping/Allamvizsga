import os
import sys
import re
from settings import *
from Extract_U_file import *

#Initializing part

def initialize_features():

     header = ['Function Name Readability','Variable Name Readability','Tabulators','Tab Indents','Space Indents','Prefer Tabs Over Spaces','Unique Words','author','function']

     Handcrafted_features = {'Function Name Readability': 0 ,
                             'Variable Name Readability' : 0 ,
                             'Tabulators' : 0 , 
                             'Tab Indents' : 0 ,
                             'Space Indents' : 0, 
                             'Prefer Tabs Over Spaces' : 0 ,
                             'Unique Words' : 0
                            }

     return (header, Handcrafted_features)

#Counting tabs

def count_tabs(line):
    return len(re.findall(r'\t', line))

#Check tab indent in a line

def check_tab_indent(line):
    if re.findall(r'^\t+', line):
         return 1
    else:
         return 0

#Check space indent in a line

def check_space_indent(line):
    if re.findall(r'^\s+', line):
         return 1
    else:
         return 0


#Check if a function name is readable or not

def check_func_name_readability(word):

    readable = 0
    en_words_from_dict = ""
    hu_words_from_dict = ""

    with open(englishtxt, 'r') as en_readable_words:
          en_words_from_dict = en_readable_words.read()
          en_is_readable = word in en_words_from_dict
    with open(hungariantxt,'r') as hu_readable_words:
          hu_words_from_dict = hu_readable_words.read()
          hu_is_readable = word in hu_words_from_dict
    if en_is_readable or hu_is_readable:
            readable = 1

    return readable

#Check if a variable name is readable or not

def check_variable_readability(words):
     if not words:
          return 0

     readable = 0
     en_words_from_dict = ""
     hu_words_from_dict = ""

     for word in words:
          with open(englishtxt, 'r') as en_readable_words:
               en_words_from_dict = en_readable_words.read()
               en_is_readable = word in en_words_from_dict
          with open(hungariantxt,'r') as hu_readable_words:
               hu_words_from_dict = hu_readable_words.read()
               hu_is_readable = word in hu_words_from_dict
          if en_is_readable or hu_is_readable:
               readable += 1
     return readable / len(words) if len(words) > 0 else 0

#Extracting variable names from clang AST tree output

def extract_variable_names(filename,function_name):

     f = open (filename,"r")
     content = f.read()
    
     stop_string = "Dumping "+function_name
     start_reading = False

     variable_list = []

     for line in content.split("\n"):
          if start_reading ==True and line == '':
               break 
          if stop_string in line:
               start_reading = True
          if start_reading == True:
               if 'ParmVarDecl' in line or 'VarDecl' in line:
                    if re.findall(r'used.*', line):
                         pattern = re.findall(r'used.*', line)
                         list = pattern[0].split(" ")
                         variable_list.append(list[1])

     return (unique(variable_list))

#Building attribute dictionary 

def extract_function_handcrafted(filename ,function_name, functions, outfile):

     line_num = 0
     over_iter = True
     words = []
     header,features = initialize_features()
     f = open(filename,"r")
     take_line = False
     content = f.read()
     for line in content.split("\n"):
          if 'include' in line:
               continue
          if re.findall(r'(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+\s*)\(\s*(?:(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))(?:\s*,\s*(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))*\s*\)', line) or re.findall(r'[a-z]+\s+[a-z]+\s*\(\s*\)',line):
               aux_list = line.split('(')
               cutted_list = aux_list[0]
               space_list = cutted_list.split()
               if len(space_list) < 2 or space_list[0] == '//':
                    continue
               pattern_word = space_list[len(space_list)-1].strip()
               if function_name == pattern_word:
                    take_line = True
          if re.findall(r'\s*[\w_][\w\d_]*\s*.*\s*[\w_][\w\d_]*\s*\(.*\)\s*$',line):
               if 'if' not in line and 'for' not in line and 'while' not in line and 'switch' not in line and 'min' not in line and 'max' not in line and 'pragma' not in line and 'define' not in line:
                    aux_list = line.split('(')
                    cutted_list = aux_list[0]
                    space_list = cutted_list.split()
                    if len(space_list) < 2 or space_list[0] == '//':
                         continue
                    pattern_word = space_list[len(space_list)-1].strip()
                    if function_name == pattern_word:
                         take_line = True
          if (take_line == False):
               continue
          if line_num > 0:
               for name in functions:
                    if re.findall(r'(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+\s*)\(\s*(?:(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))(?:\s*,\s*(?:\w+(?:\[\d+\]|<\w+>)?[*&]?\s+)+(\w+))*\s*\)', line) or re.findall(r'[a-z]+\s+[a-z]+\s*\(\s*\)',line):
                         if name in line and name != function_name and take_line == True:
                              over_iter = False
                              #print("1")
                              break
                    if re.findall(r'\s*[\w_][\w\d_]*\s*.*\s*[\w_][\w\d_]*\s*\(.*\)\s*$',line):
                         if 'if' not in line and 'for' not in line and 'while' not in line and 'switch' not in line and 'min' not in line and 'max' not in line and 'pragma' not in line and 'define' not in line:
                              if name in line and name != function_name and take_line == True:
                                   over_iter = False
                                   #print("2")
                                   break
          if over_iter == False:
               break
          
          line_num+=1
          #print(line)
          features['Tabulators'] += count_tabs(line)
          features['Tab Indents'] += check_tab_indent(line)
          features['Space Indents'] += check_space_indent(line)

          words_line = re.findall(r'([A-Z]?[a-z]+|[A-Z]+)', line)
          for word in words_line:
               words.append(word)

     variables = extract_variable_names(outfile,function_name)

     features['Function Name Readability'] = check_func_name_readability(function_name)
     features['Variable Name Readability'] = check_variable_readability(variables)
     features['Prefer Tabs Over Spaces'] = 1 if features['Tab Indents'] > features['Space Indents'] else 0
     features['Unique Words'] = len(unique(words))
     return header,features



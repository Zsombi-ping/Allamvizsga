                                        # ---- SETTINGS --- #
import os
import sys
from oneClassSVM import *
from KfoldCrossVal import *
from enum import Enum
from normalize import *
from interface import *


#Constants
baseDirectory = os.path.dirname('C:/Users/Zsombi/Desktop/Allamvizsga/')
folderpath = os.path.join(baseDirectory,"DIPLOMA/alldata")
filepath = os.path.join(baseDirectory,"foo.bat")
outfile = os.path.join(baseDirectory,"TXT/out.log")
definetxt = os.path.join(baseDirectory,"TXT/define.txt")
functiontxt = os.path.join(baseDirectory,"TXT/function.txt")
variabletxt = os.path.join(baseDirectory,"TXT/variable.txt")
hungariantxt = os.path.join(baseDirectory,"TXT/hungarian.txt")
typetxt = os.path.join(baseDirectory,"TXT/type.txt")
englishtxt = os.path.join(baseDirectory,"TXT/english.txt")
wrong_files = os.path.join(baseDirectory,"TXT/wrong_files.log")
nodesfile = os.path.join(baseDirectory,"TXT/matchers.txt")
nodesfile_all = os.path.join(baseDirectory,"TXT/matchers_all.txt")
aux_perm = os.path.join(baseDirectory,"TXT/aux_perm.txt")
aux_res =  os.path.join(baseDirectory,"TXT/aux_res.txt")
aux_file = os.path.join(baseDirectory,"TXT/aux_file.txt")
GCJ_100_unigram_file =  os.path.join(baseDirectory,'CSV/GCJ_100_unigram_file.csv')
GCJ_ALL_unigram_file = os.path.join(baseDirectory,'CSV/GCJ_ALL_unigram_file.csv')
GCJ_all_bigram_file = os.path.join(baseDirectory,'CSV/GCJ_all_bigram_file.csv')
GCJ_all_bigrams_functions = os.path.join(baseDirectory,'CSV/GCJ_all_bigrams_functions.csv')
GCJ_100_bigram_file = os.path.join(baseDirectory,'CSV/GCJ_100_bigram_file.csv')
GCJ_100_handcrafted_file = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_file.csv')
GCJ_100_handcrafted_unigram_file = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_unigram_file.csv')
GCJ_100_handcrafted_unigram_bigram_file = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_unigram_bigram_file.csv')
GCJ_100_handcrafted_bigram_file = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_bigram_file.csv')
GCJ_100_unigram_bigram_file = os.path.join(baseDirectory,'CSV/GCJ_100_unigram_bigram_file.csv')
GCJ_100_unigram_functions = os.path.join(baseDirectory,'CSV/GCJ_100_unigram_functions.csv')
GCJ_100_bigrams_functions = os.path.join(baseDirectory,'CSV/GCJ_100_bigrams_functions.csv')
GCJ_100_features_functions = os.path.join(baseDirectory,'CSV/GCJ_100_features_functions.csv')
GCJ_100_handcrafted_unigram_functions = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_unigram_functions.csv')
GCJ_100_handcrafted_bigram_functions = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_bigram_functions.csv')
GCJ_100_handcrafted_unigram_bigram_functions = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_unigram_bigram_functions.csv')
GCJ_100_unigram_bigram_functions = os.path.join(baseDirectory,'CSV/GCJ_100_unigram_bigram_functions.csv')

dataset1 = os.path.join(baseDirectory,'Programs/dataset1.txt')
dataset2 = os.path.join(baseDirectory,'Programs/dataset2.txt')
concatenated_dataset = os.path.join(baseDirectory,'Programs/concatenated_dataset.txt')

clang_command = "clang-check -extra-arg=-std=c++1y -ast-dump -ast-dump-filter="



#Choose Processing unit type:

#   FILE
#   FUNCTION


Processing_Unit = "FILE"  # Dont use space before or after




#Choose Feature category:

    # HANDCRAFTED
    # UNIGRAM
    # BIGRAM
    # HANDCRAFTED_UNIGRAM
    # HANDCRAFTED_BIGRAM
    # UNIGRAM_BIGRAM
    # HANDCRAFTED_UNIGRAM_BIGRAM


Feature_Type = "HANDCRAFTED_UNIGRAM_BIGRAM" # Dont use space before or after




#Choose Measurement type:

#   IDENTIFICATION  
#   VERIFICATION


MEASUREMENT_TYPE = "IDENTIFICATION" # Dont use space before or after


class Feature_Type_File (Enum):
    
    HANDCRAFTED = GCJ_100_handcrafted_file
    UNIGRAM = GCJ_100_unigram_file
    BIGRAM = GCJ_100_bigram_file
    HANDCRAFTED_UNIGRAM = GCJ_100_handcrafted_unigram_file
    HANDCRAFTED_BIGRAM = GCJ_100_handcrafted_bigram_file
    UNIGRAM_BIGRAM = GCJ_100_unigram_bigram_file
    HANDCRAFTED_UNIGRAM_BIGRAM = GCJ_100_handcrafted_unigram_bigram_file

class Feature_Type_Function (Enum):
   
    HANDCRAFTED = GCJ_100_features_functions
    UNIGRAM = GCJ_100_unigram_functions
    BIGRAM = GCJ_100_bigrams_functions
    HANDCRAFTED_UNIGRAM = GCJ_100_handcrafted_unigram_functions
    HANDCRAFTED_BIGRAM = GCJ_100_handcrafted_bigram_functions
    UNIGRAM_BIGRAM = GCJ_100_unigram_bigram_functions
    HANDCRAFTED_UNIGRAM_BIGRAM = GCJ_100_handcrafted_unigram_bigram_functions


    
def main():
    
    

    f = open(aux_file,'r')
    vec = f.read()
    words = vec.split(",")
  
    Feature_Type = words[0]
    Processing_Unit = words[1]
    MEASUREMENT_TYPE = words[2]

    f.close()

    

    if Processing_Unit !="FILE" and Processing_Unit !="FUNCTION":
        print('Settings problem')
    else:
        if Processing_Unit == "FILE":
            dataset = Feature_Type_File[Feature_Type].value
        else:
            dataset = Feature_Type_Function[Feature_Type].value
        print("\n\nCurrent dataset is    ---     " + str(dataset) + "    ---\n\n")        
        dataset = norm(dataset,Processing_Unit)
        if MEASUREMENT_TYPE == "VERIFICATION":
            load_datas(dataset,Processing_Unit)
        elif MEASUREMENT_TYPE =="IDENTIFICATION":
            KfoldVal(dataset,Processing_Unit)
        else:
            print("Settings problem")
    

if __name__ == '__main__':
    main()

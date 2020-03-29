                                        # ---- SETTINGS --- #
import os
import sys
from oneClassSVM import *
from KfoldCrossVal import *
from enum import Enum

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
GCJ_100_unigram =  os.path.join(baseDirectory,'CSV/GCJ_100_unigram.csv')
GCJ_ALL_unigram = os.path.join(baseDirectory,'CSV/GCJ_ALL_unigram.csv')
GCJ_100_bigram = os.path.join(baseDirectory,'CSV/GCJ_100_bigram.csv')
GCJ_100_handcrafted = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted.csv')
GCJ_100_handcrafted_unigram = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_unigram.csv')
GCJ_100_handcrafted_unigram_bigram = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_unigram_bigram.csv')
GCJ_100_handcrafted_bigram = os.path.join(baseDirectory,'CSV/GCJ_100_handcrafted_bigram.csv')
GCJ_100_unigram_bigram = os.path.join(baseDirectory,'CSV/GCJ_100_unigram_bigram.csv')
GCJ_100_unigram_functions = os.path.join(baseDirectory,'CSV/GCJ_100_unigram_functions.csv')
GCJ_100_bigrams_functions = os.path.join(baseDirectory,'CSV/GCJ_100_bigrams_functions.csv')
GCJ_100_unigram_bigrams_functions = os.path.join(baseDirectory,'CSV/GCJ_100_unigram_bigrams_functions.csv')
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



Processing_Unit = "FUNCTION"


#Choose Feature category:

    # HANDCFRATED 
    # UNIGRAM
    # BIGRAM
    # HANDCRAFTED_UNIGRAM
    # HANDCRAFTED_BIGRAM
    # UNIGRAM_BIGRAM
    # HANDCRAFTED_UNIGRAM_BIGRAM



Feature_Type = "UNIGRAM" 


#Choose Measurement type:

#   IDENTIFICATION  
#   VERIFICATION


MEASUREMENT_TYPE = "VERIFICATION"


class Feature_Type_File (Enum):
    HANDCRAFTED = GCJ_100_handcrafted
    UNIGRAM = GCJ_100_unigram
    BIGRAM = GCJ_100_bigram
    HANDCRAFTED_UNIGRAM = GCJ_100_handcrafted_unigram
    HANDCRAFTED_BIGRAM = GCJ_100_handcrafted_bigram
    UNIGRAM_BIGRAM = GCJ_100_unigram_bigram
    HANDCRAFTED_UNIGRAM_BIGRAM = GCJ_100_handcrafted_unigram_bigram

class Feature_Type_Function (Enum):
    HANDCRAFTED = GCJ_100_features_functions
    UNIGRAM = GCJ_100_unigram_functions
    BIGRAM = GCJ_100_bigrams_functions
    HANDCRAFTED_UNIGRAM = GCJ_100_handcrafted_unigram_functions
    HANDCRAFTED_BIGRAM = GCJ_100_handcrafted_bigram_functions
    UNIGRAM_BIGRAM = GCJ_100_unigram_bigrams_functions
    HANDCRAFTED_UNIGRAM_BIGRAM = GCJ_100_handcrafted_unigram_bigram_functions

    
def main():
    
    global Processing_Unit
    global Feature_Type
    global MEASUREMENT_TYPE
    
    if Processing_Unit !="FILE" and Processing_Unit !="FUNCTION":
        print('Settings problem')
    else:
        if Processing_Unit == "FILE":
            dataset = Feature_Type_File[Feature_Type].value
        else:
            dataset = Feature_Type_Function[Feature_Type].value


        print("\n\nCurrent dataset is    ---     " + str(dataset) + "    ---\n\n")
        
        
        if MEASUREMENT_TYPE == "VERIFICATION":
            load_datas(dataset)
        elif MEASUREMENT_TYPE =="IDENTIFICATION":
            KfoldVal(dataset,Processing_Unit)
        else:
            print("Settings problem")
    

if __name__ == '__main__':
    main()

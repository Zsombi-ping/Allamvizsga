import os


baseDirectory = os.path.dirname('C:/Users/Zsombi/Desktop/Allamvizsga/')
folderpath = os.path.join(baseDirectory,"DIPLOMA/alldata/")
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
clang_command = "clang-check -extra-arg=-std=c++1y -ast-dump -ast-dump-filter="


import os


baseDirectory = os.path.dirname('C:/Users/Zsombi/Desktop/Allamvizsga/')
folderpath = os.path.join(baseDirectory,"DIPLOMA/data/100_users")
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
small_dataset =  os.path.join(baseDirectory,'CSV/dataframe_export_first_100.csv')
big_dataset = os.path.join(baseDirectory,'CSV/dataframe_export_all.csv')
Bigrams_AST_dataset = os.path.join(baseDirectory,'CSV/AST_bigramms_GCJ_100.csv')
LL_features = os.path.join(baseDirectory,'CSV/LL_features_first_100_GCJ.csv')
clang_command = "clang-check -extra-arg=-std=c++1y -ast-dump -ast-dump-filter="


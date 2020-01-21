import os


baseDirectory = os.path.dirname(__file__)
folderpath = os.path.join(baseDirectory,"DIPLOMA/alldata")
filepath = os.path.join(baseDirectory,"foo.bat")
outfile = os.path.join(baseDirectory,"out.log")
wrong_files = os.path.join(baseDirectory,"wrong_files.log")
small_dataset =  os.path.join(baseDirectory,'dataframe_export_first_100.csv')
big_dataset = os.path.join(baseDirectory,'dataframe_export_all.csv')
clang_command = "clang-check -extra-arg=-std=c++1y -ast-dump -ast-dump-filter="
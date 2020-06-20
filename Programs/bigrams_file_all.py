# Extracting Bigrams from each file

import sys

import clang
import clang.cindex
from settings import *
from Extract_U_file import *

PRINT_HEADER = True

list_nodes = []

#Cleaning node name

def trimClangNodeName(nodeName):
    ret = str(nodeName)
    ret = ret.split(".")[1]
    return ret
    
#Traverse the AST tree from the root recursively

def traverseAST(node , bigrams_set):
        if node is not None:
            #list_nodes.append(trimClangNodeName(node.kind))
            # Recurse for children of this node
            for childNode in node.get_children():
                bigrams_set[trimClangNodeName(node.kind) + trimClangNodeName(childNode.kind)] +=1
                traverseAST(childNode, bigrams_set)
        
#Initializing part

def init_bigrams():
    
    headers = []
    bigrams = {}
    f = open(nodesfile_all,"r",encoding='utf8', errors='ignore')
    content1 = f.read()
    f.close()
    f = open(nodesfile_all,"r",encoding='utf8', errors='ignore')
    content2 = f.read()
    f.close()
   
    for first_attr in content1.split('\n'):
        for second_attr in content2.split('\n'):
            bigrams[first_attr + second_attr] = 0
            headers.append(first_attr + second_attr)
    
    headers.append("author")
    return (headers,bigrams)
      
#Iterate over folders and extract the bigrams

def build_bigrams():
    i = 0
    index_counter = 1
    csv_file = GCJ_100_bigram_file

    users_folder = os.listdir(folderpath)
    for folder in users_folder:
        folder_str = ""
        folder_str = folderpath+"/"+folder+"/*.cpp"
        file_check = True
        for file in glob.iglob(folder_str):  
            name = search_func_names(file)
            names = unique(name)
            if len(names) == 0 :
                file_check = False
                break
        if file_check == True:
            i = i + 1
            for file in glob.iglob(folder_str):
                try:      
                    print(file)
                    global PRINT_HEADER
                    csv_columns , bigrams  = init_bigrams() 
                    index = clang.cindex.Index.create()
                    translationUnit = index.parse(file)
                    rootNode = translationUnit.cursor
                    traverseAST(rootNode, bigrams)
                    bigrams['author'] = folder
                    df=pd.DataFrame(bigrams,index=[index_counter])
                    if PRINT_HEADER:
                        df.to_csv(csv_file, mode = 'w', header=csv_columns, index = False) 
                        PRINT_HEADER = False
                    else:
                        df.to_csv(csv_file, mode = 'a', header = False, index = False) 
                except ValueError:
                    bigrams['author'] = folder
                    df=pd.DataFrame(bigrams,index=[index_counter])
                    if PRINT_HEADER:
                        df.to_csv(csv_file, mode = 'w', header=csv_columns, index = False)
                        PRINT_HEADER = False
                    else:
                        df.to_csv(csv_file, mode = 'a', header = False, index = False)
                    continue
        if i==100:
            break

def main():

    build_bigrams()
    
if __name__ == '__main__':
    main()




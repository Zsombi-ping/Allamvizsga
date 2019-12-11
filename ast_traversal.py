import sys
import clang
import clang.cindex


tree_list = []
i = 0

def trimClangNodeName(nodeName):
    ret = str(nodeName)
    ret = ret.split(".")[1]
    return ret
    
def printASTNode(node, level): 
    global i 
    i = i +1
    print(i)
    print (trimClangNodeName(node.kind)+" -> ("+str(level)+")\n")

def traverseAST(node, level):
        if node is not None:
            level = level+1
            printASTNode(node, level)
            # Recurse for children of this node
            for childNode in node.get_children():
                tree_list.append(trimClangNodeName(node.kind) + ":"+ trimClangNodeName(childNode.kind))
                traverseAST(childNode,level)
            level = level-1



index = clang.cindex.Index.create()
translationUnit = index.parse("C:/Users/Zsombi/Desktop/Allamvizsga/main.cpp")
rootNode = translationUnit.cursor
try:
    traverseAST(rootNode, 0)
except ValueError:
    print ("Wrong type")

print("\n\n\n")
for x in tree_list:
    print(x)
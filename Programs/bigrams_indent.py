import os
import re


# Extracting bigrams from functions for each file

def bigrams_by_function(filename, function_name):

    attributes = '<<<NULL>>>,AbiTagAttr,AccessSpecDecl,ArraySubscriptExpr,BinaryOperator,CStyleCastExpr,CXXBoolLiteralExpr,CXXConstructExpr,CXXConstructorDecl,CXXConversionDecl,CXXCtorInitializer,CXXDependentScopeMemberExpr,CXXDestructorDecl,CXXFunctionalCastExpr,CXXMemberCallExpr,CXXMethodDecl,CXXOperatorCallExpr,CXXRecordDecl,CXXStaticCastExpr,CXXTemporaryObjectExpr,CXXThisExpr,CXXUnresolvedConstructExpr,CallExpr,ClassTemplateSpecialization,CompoundAssignOperator,CompoundStmt,ContinueStmt,ConditionalOperator,ConstantExpr,CopyAssignment,CopyConstructor,DeclRefExpr,DeclStmt,DefaultConstructor,DefinitionData,DependentNameType,Destructor,EnumConstantDecl,ExprWithCleanups,FieldDecl,ForStmt,FormatAttr,FriendDecl,FunctionDecl,FunctionTemplateDecl,ImplicitCastExpr,IfStmt,IntegerLiteral,MaterializeTemporaryExpr,MemberExpr,MoveAssignment,MoveConstructor,NoThrowAttr,NullStmt,public,ParenExpr,ParenListExpr,ParmVarDecl,PureAttr,ReturnStmt,StringLiteral,TemplateArgument,TemplateSpecializationType,TemplateTypeParmDecl,TypedefDecl,UnaryOperator,UnresolvedLookupExpr,UsingDecl,VarDecl,UsingShadowDecl,WhileStmt'
    atrib_list = attributes.split(',')
    bigrams = {}
    headers = []

    for x in atrib_list:
        for y in atrib_list:
            bigrams[x +"_"+ y] = 0
            headers.append(x + "_" + y)
   
    headers.append("author")
    headers.append("function")
    f = open (filename,"r")
    content = f.read()

    list_pair = [("FunctionDecl",-1)]

    stop_string = "Dumping "+function_name
    start_reading = False

    for line in content.split("\n"):
        if start_reading ==True and line == '':
            break 
        if stop_string in line:
            start_reading = True
        if start_reading == True:
            #print(line)
            for attr in atrib_list:
                str_srch = "-"+attr
                if re.search('(.*)'+str_srch+'(.*)',line) and re.search(r'^.*?(?=-)', line):
                    countx =  re.search(r'^.*?(?=-)', line)
                    size_reg = len(countx.group(0))
                    list_pair.append((attr,size_reg))


    size = len(list_pair)
    i = 1

# Checking indent level 

    for pair in list_pair:
        (attr1 , indent_num1) = pair
        j = 0
        for pair2 in list_pair:
            if j<i:
                j+=1
                continue
            (attr2 , indent_num2) = pair2
            if indent_num2 <= indent_num1:
                break
            elif indent_num2 - indent_num1 == 2:
                bigrams[attr1 + "_" + attr2] +=1
        i+=1

    return (headers , bigrams)



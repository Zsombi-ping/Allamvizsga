import subprocess
import sys
import re


def search_func_names(filename):
    f_names = []
    file_o=open(filename)   
    content=file_o.read()                
    for line in content.split('\n'):
        if  re.search("(?![a-z])[^\:,>,\.]([a-z,A-Z]+[_]*[a-z,A-Z]*)+[(]",line):
            if re.search("^(void |int |unsigned |long |float |double |char )",line):
               if not line.find("int main"):
                   continue
               aux_list = line.split()
               name = aux_list[1]
               func_name = name.split('(')
               f_names.append(func_name[0])   
    return f_names


def redirect_to_file(text,outfile):
    original = sys.stdout
    sys.stdout = open(outfile, 'a')
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
    
    f = open(outfile,"w")
    f.truncate(0)
    for name in list_of_names:
        build_command = "clang-check -extra-arg=-std=c++1y -ast-dump -ast-dump-filter="
        build_command = build_command + name + " " + filename
        f = open(filepath, "w")
        f.write(build_command)
        f.close()
        create_subprocess_file_pipe(filepath,outfile)


def main():
        
    filepath="C:/Users/Zsombi/Desktop/Allamvizsga/foo.bat"
    outfile = 'C:/Users/Zsombi/Desktop/Allamvizsga/out.log'
    filename = "C:/Users/Zsombi/Desktop/Allamvizsga/main.cpp"
    list_of_func_names = search_func_names(filename)
    print ("Function names : ")
    print(list_of_func_names)
    print('\nBuilding AST for cpp file '+filename)
    build_ast(list_of_func_names,filename,outfile,filepath)
    print('\nOpen '+outfile +' to see the result')


if __name__ == '__main__':
    main()
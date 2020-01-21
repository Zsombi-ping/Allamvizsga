# Allamvizsga

This project is about code analysing (C++ source code) via Clang LLVM compiler. The Building_AST python script grabs the function names from code and
building AST (Abstract Syntax Tree) for each of them through a filter command. Clang has 68 identifier node , so these can help us to visualize C++ code in abstract form.
The dataset is from GCJ (Google Code Jam) codeing competition , each author has 9 source code. The primary target is to extract informations , occurences
from code and afterwards to export them into a CSV file. Once it is done we can perform different Machine-learning algorithms on this dataset to figure out who could be
the author of that code (De-anonymizing Programmers via Code Stylometry)

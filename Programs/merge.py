# Mergeing 2 different file into 1 for measuring

from settings import *
from Extract_U_file import *

i = 0

with open(dataset1) as f1, open(dataset2) as f2 ,  open (concatenated_dataset,'a')as outf:
  for x, y in zip(f1, f2):
    x = x.replace("\n","")
    line = x + ","+ y
    outf.write(line)


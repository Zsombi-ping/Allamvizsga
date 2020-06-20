#import os
#import sys



import matplotlib.pyplot as plt

vals = [257.2, 144.9, 145.0, 248.4, 160.2, 245.8, 228.0, 236.3, 0.0, 231.9, 198.4, 141.7, 211.0, 244.6, 354.6, 190.6, 111.1, 221.0, 193.3, 342.4, 168.2, 282.0, 173.9, 79.6, 313.7, 69.6, 174.3, 184.0, 150.9, 322.0, 196.6, 214.8, 185.6, 187.7, 360.8, 246.3, 210.1, 345.7, 248.0, 234.1, 292.0, 203.4, 154.4, 161.6, 176.9, 229.8, 171.1, 303.9, 129.1, 293.3, 244.4, 161.1, 137.0, 419.6, 215.8, 76.6, 174.4, 196.0, 154.4, 229.9, 308.3, 165.8, 166.2, 280.9, 245.4, 135.8, 208.1, 282.3, 195.3, 201.4, 34.8, 205.9, 199.7, 327.9, 269.7, 194.9, 145.2, 151.7, 202.0, 376.6, 111.2, 362.8, 220.1, 225.7, 240.8, 249.0, 227.8, 124.1, 205.2, 237.2, 129.0, 127.6, 284.4, 255.4, 0.0, 244.7, 166.1, 160.9, 190.3, 278.1]




n, bins, patches = plt.hist(vals, bins=90, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7)

n = n.astype('int') # it MUST be integer

for i in range(len(patches)):
    patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))


plt.title('Szavak gyakorisága szerző forrásállományaiként átlagolva GCJ_100', fontsize=12)
plt.xlabel('Szavak száma', fontsize=12)
plt.ylabel('Gyakoriság', fontsize=12)
plt.show()
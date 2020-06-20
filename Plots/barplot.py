import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 7
VERIFICATION_FILE = (64,76,84,81,87,77,87)
VERIFICATION_FUNCTION = (61,60,67,67,62,60,62)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, VERIFICATION_FILE , bar_width,
alpha=opacity,
color='b',
label='Verification file')

rects2 = plt.bar(index + bar_width,VERIFICATION_FUNCTION , bar_width,
alpha=opacity,
color='g',
label='Verification function')

plt.xlabel('Feature Category',fontsize=12)
plt.ylabel('Scores',fontsize=12)
plt.title('VERIFICATION GCJ-100',fontsize=12)
plt.xticks(index + bar_width, ('U', 'B', 'H', 'H-U','H-B','U-B','H-U-B'),fontsize = 12)
plt.legend()

plt.tight_layout()
plt.show()
#fig.savefig('file_res.png')

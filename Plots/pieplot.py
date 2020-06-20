from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
labels = ['unique_words','comments','function_block_braces','tabulators','spaces','functions','nesting_depth','tab_indents','prefers_tabs_over_spaces','for_keywords']
students = [96.9,72.0,64.0,59.6,51.6,48.9,48.9,37.3,30.2,30.2]
ax.pie(students, labels = labels,autopct='%1.2f%%', textprops={'fontsize': 15})
plt.show()

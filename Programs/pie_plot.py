# import matplotlib.pyplot as plt

# # Pie chart, where the slices will be ordered and plotted counter-clockwise:
# labels = 'CXXOperatorCallExpr', 'StringLiteral', 'ParenExpr', 'ReturnStmt','DeclStmt','FunctionDecl','CXXConstructExpr','ArraySubscriptExpr','CStyleCastExpr','IntegerLiteral'
# sizes = [0.0560, 0.0436, 0.0329, 0.0320,0.0302,0.0267,0.0142,0.0142,0.0133,0.0124]
# explode = (0, 0, 0, 0,0,0,0,0,0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%',
#         shadow=False, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# a
# plt.show()

from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
labels = ['unique_words','comments','function_block_braces','tabulators','spaces','functions','nesting_depth','tab_indents','prefers_tabs_over_spaces','for_keywords']
students = [96.9,72.0,64.0,59.6,51.6,48.9,48.9,37.3,30.2,30.2]
ax.pie(students, labels = labels,autopct='%1.2f%%', textprops={'fontsize': 15})
plt.show()

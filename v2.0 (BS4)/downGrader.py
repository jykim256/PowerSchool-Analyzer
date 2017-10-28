from cleanTableR import loadData, getFileName
import numpy as np
import random


def printArray(a, heading):
   print()
   print(heading)
   for i in range(len(a)):
      for j in a[i]:
         print(j, end="\t")
      print()
   print()


checkEqual, allAssignments, updateHistoryInitial = loadData(getFileName(), [
                                                            ''])
printArray(updateHistoryInitial, 'Before:')

editClass = [i for i in range(random.randint(0, len(updateHistoryInitial)))]
for i in editClass:
   updateHistoryInitial[i][0] = 'Do you even lift ' + \
       str(random.randint(5, 15)) + ' kgs?'

np.savez(getFileName(), allAssignments, updateHistoryInitial)
print('Data saved to file ' + getFileName() + ' in same directory')

printArray(updateHistoryInitial, 'After:')

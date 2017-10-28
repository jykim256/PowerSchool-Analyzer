import numpy as np

def getAssignmentRow(assignments,i,j,schoolYear):
	if j == len(assignments) - 1:
		className = assignments[1].select('td')[0].text
		print('Found class #' + str(i + 1) + ': ' + className + '!')
	#checks if the row is actually a row
	item = assignments[j].text
	if '/' in item and (schoolYear[0] in item or schoolYear[1] in item):
		#goes into each table column and adds the text
		rowElements = assignments[j].select('td')
		row = ['' for _ in range(len(rowElements) - 1)]
		#separate the categories in each row
		for k in range(len(rowElements)):
			# print(rowElements[k].text)
			# separates the date
			if k < 3:
				row[k] = rowElements[k].text
			# separates the score
			elif k == 8:
				s = rowElements[k].text
				try:
					divider = s.index('/')
				except:
					row[3] = 0
					row[4] = 0
				else:
					row[3] = s[:divider]
					row[4] = s[divider+1:]
			# puts in everything else
			elif k > 7 and k <= len(row):
				row[k - 4] = rowElements[k].text
		#morgan in case assignments are excluded
		try:
			row[len(row) - 3] = assignments[j].select('img')[0].get('alt')
		except:
			pass
	return row

# Returns the name of the class
def getClassNames(assignments):
	return assignments[1].select('td')[0].text[0:3]

# Returns the date at when grade was last updated
def getUpdateHistory(classPage):
	return classPage.find(id='legend').select('.center')[0].text

def getGrades(assignments):
	return assignments[1].select('td')[3].text

def loadData(fileName, updateHistory):
	# loads the file
	data = np.load(fileName)
	allAssignments = data['allAssignments']
	updateHistoryInitial = data['classes']
	checkEqual = np.array([[True]])

	# legacy code where i didn't know how to save
	# # makes an array of the dimensions of each array
	# lenArray = list(map(lambda x: len(np.shape(x)),[data[data.files[0]],data[data.files[1]]]))
	# # array with 2 dimension is grades array
	# updateIndex = lenArray.index(2)
	# updateHistoryInitial = data[data.files[updateIndex]]
	# # finds the other two arrays
	# allAssignments = data[data.files[lenArray.index(1)]]


	try:
		checkEqual = np.array(updateHistory) == updateHistoryInitial
	except:
		checkEqual[0] = [False]

	return [checkEqual, allAssignments, updateHistoryInitial]

def getFileName():
	return 'PSData.npz'

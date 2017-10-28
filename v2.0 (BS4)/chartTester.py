import os.path,os,time,openpyxl
from openpyxl.chart import BarChart, Reference,Series



tableOffset = 2
maxNumCols = 10

# CLASSES
categories = [['X', 'X', 'X', 'X'],
				  ['X', 'X', 'X', 'X'],
				  ['X', 'X', 'X', 'X'],
				  ['X', 'X', 'X', 'X']]
classes = [['X','Grades last updated on 12/05/2015'],
			  ['X','Grades last updated on 12/05/2015'],
			  ['X','Grades last updated on 12/05/2015'],
			  ['X','Grades last updated on 12/05/2015']]
class2 = ['a','b','c','d']

num = 1

sheet,book='',''
if num == 0:	XLName = 'ChartTester.xlsx'
	#XLName = 'Grades 3.xlsx'
else:	XLName = 'Grades.xlsx'

book = openpyxl.load_workbook(filename = XLName)

for i in range(4):
	if num == 0:		sheet = book[class2[i]]
	else:					sheet = book[classes[i][0]]
	
	ccc = categories[i]

	if True:
		chart = BarChart()
		chart.type = "col"
		chart.style = 2
		chart.title = "Category Percentage"
		chart.x_axis.title = 'Categories'
		chart.y_axis.title = 'Percent (%)'
		chart.x_axis.delete = True
		chart.y_axis.scaling.min = 50
		chart.y_axis.scaling.max = 101
	
	start = maxNumCols + tableOffset + 1
	end = start+len(ccc) - 1
	cats = Reference(sheet, min_col=start, max_col=end, min_row=1, max_row=1)
	for j in range(start,end+1):
		data = Reference(sheet, min_col=j, min_row=4, max_row=4)
		series = Series(data, title = ccc[j - start])
		chart.series.append(series)

	#chart.grouping = 'clustered'
	sheet.add_chart(chart, 'K15')

if True:
	isOpen = True
	while(isOpen):
		try:
			book.save(XLName)
			isOpen = False
		except:
			#os.system('taskkill /F /IM excel.exe')
			print('Close Excel Spreadsheet!')
			time.sleep(0.8)
	print(XLName + ' updated.')
	os.system(XLName)
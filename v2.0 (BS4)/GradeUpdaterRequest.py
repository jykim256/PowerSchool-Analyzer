import os.path,requests,bs4,time,sys
from cleanTableR import getClassNames,getUpdateHistory,loadData,getGrades
from requestTester import getAssignments,login,getClassLinks,getUserLogin,printTime
from Datareader import exportXL,getXLName
from datetime import date


###### TODO ######
# - Color grades/assignments based on category or grade
# - Set column width to automatic
# - Save the class weights
# - Port to java
# - (DONE) Bar graph of categories
# - (DONE) actual dates


# USER INPUT
username = 'XXXX'
password = 'XXXX'
schoolYear = ['2015', '2016']
gradingPeriod = 'P1'

# uncomment below line if you want to input through the command line
username, password, schoolYear, gradingPeriod = getUserLogin()
fileName = 'PSData.npz'
userInput = [username, password, schoolYear, fileName, gradingPeriod]

c0 = time.clock()

# checks if file exists
if os.path.isfile(fileName):
    print('Previous data exists!')
    # print out previous data
    if(False):
        a = loadData(fileName,[''])
        print(a[1])
    BASE_URL = 'https://powerschool.sandi.net/guardian/'
    with requests.Session() as s:
        mainPage = login(s,username,password)
        c0 = printTime(c0,'logging in.')
        # find classes
        print('-- Searching for ' + gradingPeriod + ' entries --')
        classLinks = getClassLinks(mainPage,schoolYear,gradingPeriod)
        # get the update history
        updateHistory = ['' for _ in range(len(classLinks))]
        grades = ['' for _ in range(len(classLinks))]
        for i in range(len(classLinks)):
            classPage = bs4.BeautifulSoup(s.get(BASE_URL + classLinks[i]).text,'lxml')
            assignments = classPage.select('tr')
            updateHistory[i] = [getClassNames(assignments),getUpdateHistory(classPage)]
            grades[i] = getGrades(assignments)
        
        c0 = printTime(c0,'grabbing update history.')

        # to show grade history
        # find max length of class name
        if len(updateHistory) == 0:
            print('PowerSchool Maintenance')
            sys.exit()
        maxLength = len(updateHistory[0])
        for i in updateHistory:
            length = len(i[0])
            if maxLength < length:
                maxLength = length
        # print grade history formatted
        maxGradeLength = 8
        gradeString = grades.copy()
        for i in range(len(grades)):
            grades[i] = int('0'+''.join(list(filter(str.isdigit, grades[i]))))
            gradeString[i] = grades[i]
            while(gradeString[i] > 100):
                gradeString[i] /= 10.0
            gradeString[i] = '['+ str(gradeString[i]) + '%] '
            gradeString[i] = gradeString[i] + ''.join(['-' for _ in range(maxGradeLength - len(gradeString[i]) + 1)])

        print()
        uHist = updateHistory
        for i in range(len(uHist)):
            # Get when it was updated
            update = uHist[i][1][-10:]
            # Get when today is
            update = date(int(update[-4:]),int(update[:2]),int(update[3:5]))
            # Make string of time difference
            # replace 'Updated' with uHist[i][1][:-13] if you want 'Grades updated'
            update = ' Updated ' + str((date.today() - update).days) + ' days before.'
            print(gradeString[i] + ' [' + uHist[i][0] + '] ' +''.join(['-' for _ in range(maxLength - len(uHist[i][0]) + 5)]) + update)
        print()
    #obtains data from file
    try:
        checkEqual,allAssignments,classes = loadData(fileName,updateHistory)
        checkEqual = checkEqual.all(axis=1)
        for i in range(len(checkEqual)):
            if not(checkEqual[i]):
                print(uHist[i][0] + ' updated!')
        if not(checkEqual.all()):
            print()
    except Exception as e:
        print(e)
        print('File Corrupted: New Download Required')
        allAssignments,classes = getAssignments(userInput,[s,mainPage])
    else:
        #checks if new updates have happened
        try:
            if(checkEqual.all()):
                print('No Updates Needed!')
                updatedData = True
                c0 = printTime(c0,'checking for updates')
            else:
                c0 = printTime(c0,'checking for updates')
                print('Found New Updates: Updates Required')
                allAssignments,classes = getAssignments(userInput,[s,mainPage])
        except:
            c0 = printTime(c0,'checking for updates')
            print('File Corrupted: New Download Required')
            allAssignments,classes = getAssignments(userInput,[s,mainPage])
else:
    print('File Not Found: Updates Required')
    allAssignments,classes = getAssignments(userInput)
    grades = [0 for i in range(4)] # special case for current account, remove or move to 6 for general
#Now all data has been gathered
exportXL(grades,allAssignments,classes,getXLName())
printTime(c0,'exporting data to Excel')
print('Punctum finis.')
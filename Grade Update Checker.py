import os.path
from selenium import webdriver
from cleanTable import getClassNames, getUpdateHistory
from PowerSchoolAnalysis import PSAnalysis, login, getClassData, loadData
from Datareader import exportXL, getXLName

# USER INPUT
username = 'XXXX'
password = 'XXXX'
schoolYear = ['2015', '2016']
fileName = 'PSData.npz'

# username,password,schoolYear = getUserLogin()
fileName = 'PSData.npz'
userInput = [username, password, schoolYear, fileName]

# checks if file exists
if os.path.isfile(fileName):
    print('Previous data exists!')

    # print out previous data
    if(False):
        a = loadData(fileName, [''])
        print(a[1])

    driver = webdriver.Chrome()
    driver.set_window_position(-2000, -2000)
    # login
    login(driver, username, password)
    # find classes
    classLinks, grades = getClassData(driver)
    for i in grades:
        print(i)

    # get the update history
    updateHistory = ['' for _ in range(len(classLinks))]
    for i in range(len(classLinks)):
        driver.get(classLinks[i])
        assignments = driver.find_elements_by_tag_name('tr')
        updateHistory[i] = [getClassNames(assignments), getUpdateHistory(driver)]
    driver.close()

    # obtains data from file
    try:
        checkEqual, allAssignments, classes, grades = loadData(fileName, updateHistory)
    except Exception:
        print('File Corrupted: New Download Required')
        allAssignments, classes = PSAnalysis(userInput)
    else:
        # checks if new updates have happened
        try:
            if(checkEqual.all()):
                print('No Updates Needed!')
                updatedData = True
            else:
                print('Found New Updates: Updates Required')
                allAssignments, classes = PSAnalysis(userInput)
        except Exception:
            print('Found New Updates: Updates Required')
            allAssignments, classes = PSAnalysis(userInput)
else:
    print('File Not Found: Updates Required')
    allAssignments, classes = PSAnalysis(userInput)

# Now all data has been gathered
exportXL(allAssignments, classes, getXLName())

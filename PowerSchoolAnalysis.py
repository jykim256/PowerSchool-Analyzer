from selenium import webdriver
from cleanTable import cleanTable, getClassNames, getUpdateHistory
import numpy as np

yes = ['yes', 'y']
no = ['no', 'n']


def getUserLogin():
    username = input('Enter your PowerSchool Username: ')
    password = input('Enter your PowerSchool Password: ')

    schoolYear = ''
    legitimateInput = False
    while not(legitimateInput):
        schoolYear = input('Is the school year 2015 - 2016? (Y/N) ')
        if schoolYear.lower() in yes:
            schoolYear = ['2015', '2016']
            legitimateInput = True
        elif schoolYear.lower() in no:
            schoolCheck = True
            while schoolCheck:
                intercept = input('Enter years since 2015 - 2016 school year:')
                try:
                    intercept = int(intercept)
                except Exception:
                    pass
                else:
                    schoolYear = [str(2015 + intercept), str(2016 + intercept)]
                    schoolCheck = False
                    legitimateInput = True
        else:
            continue
    return[username, password, schoolYear]


def login(driver, username, password):
    driver.get('https://powerschool.sandi.net/public/home.html')
    loginGood = False
    while not(loginGood):
        try:
            driver.find_element_by_id('fieldAccount').send_keys(username)
            driver.find_element_by_id('fieldPassword').send_keys(password)
            driver.find_element_by_id('btn-enter').click()
        except Exception:
            return  # internet is down
        else:
            try:
                driver.find_element_by_id('btn-enter')
            except Exception:
                loginGood = True
            else:
                print('Wrong login details!')
                username, password, _ = getUserLogin()


def getClassData(driver):
    allLinks = driver.find_elements_by_tag_name('a')
    # these are the links for the classLinks
    classLinks = []
    for i in range(len(allLinks)):
        if '\n' in allLinks[i].text:
            classLinks.append(i)
    # these are the links for the classLinks
    classLinks = np.array(classLinks)
    numQuarters = driver.find_element_by_class_name("th2").text.count(' ') - 7

    classLinks = classLinks[0 + numQuarters - 1:len(classLinks):numQuarters]
    classData = list(map(lambda x: [allLinks[x].get_attribute('href'),
                                    allLinks[x].text], classLinks))
    return [[classData[i][0] for i in range(len(classData))],
            [classData[i][1] for i in range(len(classData))]]


def loadData(fileName, updateHistory):
    # loads the file
    data = np.load(fileName)
    # makes an array of the dimensions of each array
    lenArray = list(map(lambda x: len(np.shape(x)), [data[data.files[0]],
                                                     data[data.files[1]],
                                                     data[data.files[2]]]))
    # array with 2 dimension is grades array
    updateIndex = lenArray.index(2)
    updateHistoryInitial = data[data.files[updateIndex]]
    # finds the other two arrays
    firstIndex = lenArray.index(1)
    secondIndex = lenArray[firstIndex + 1:].index(1) + firstIndex + 1
    # tries to see which one is three dimensional, since that
    # one is allAssignments (classes, assignments, individual columns)
    if len(np.shape(data[data.files[firstIndex]][0])) == 2:
        allAssignments = data[data.files[firstIndex]]
        grades = data[data.files[secondIndex]]
    else:
        grades = data[data.files[firstIndex]]
        allAssignments = data[data.files[secondIndex]]
    checkEqual = updateHistory == updateHistoryInitial
    return [checkEqual, allAssignments, updateHistoryInitial, grades]


def PSAnalysis(userInput):
    username, password, schoolYear, fileName = userInput
    driver = webdriver.Chrome()
    driver.set_window_position(-2000, -2000)
    # login
    login(driver, username, password)
    # find classes
    classLinks, grades = getClassData(driver)

    # get data from each class into one array
    allAssignments = ['' for _ in range(len(classLinks))]
    classes = [['', ''] for _ in range(len(classLinks))]
    for i in range(len(classLinks)):
        # go to each period
        driver.get(classLinks[i])
        # get the tr entries
        assignments = driver.find_elements_by_tag_name('tr')
        allAssignments[i] = list(map(lambda j: cleanTable(assignments, i, j, schoolYear),
                                               range(3,len(assignments))))
        classes[i] = [getClassNames(assignments), getUpdateHistory(driver)]
    # print(allAssignments)
    # print(classes)

    possibleDashes = [0, 1, 2, 5, 6]

    # split the string of each row into arrays
    for i in range(len(allAssignments)):
        for j in range(len(allAssignments[i])):
            stringRow = allAssignments[i][j]
            row = ['' for _ in range(10)]
            for k in range(len(row)):
                if not(k in possibleDashes):
                    if '|' in stringRow:
                        index = stringRow.find('|')
                else:
                    indexA = 500
                    indexB = 500
                    if '/' in stringRow:
                        indexA = stringRow.find('/')
                    if '|' in stringRow:
                        indexB = stringRow.find('|')
                    if indexA > indexB:
                        index = indexB
                    else:
                        index = indexA

                row[k] = stringRow[:index]
                stringRow = stringRow[index + 1:]
            allAssignments[i][j] = row
    # print(allAssignments)
    driver.close()

    for i in range(len(allAssignments)):
        allAssignments[i] = np.array(allAssignments[i], dtype=str)
        classes = np.array(classes, dtype=str)
        grades = np.array(grades, dtype=str)

    np.savez(fileName, allAssignments, classes, grades)
    print('Data saved to file ' + fileName + ' in same directory')
    return [allAssignments, classes]
# PSAnalysis()


if __name__ == "__main__":
    username = 'XXXX'
    password = 'XXXX'
    schoolYear = ['2015', '2016']
    fileName = 'PSData.npz'

    # username, password, schoolYear = getUserLogin()
    fileName = 'PSData.npz'
    userInput = [username, password, schoolYear, fileName]
    PSAnalysis(userInput)

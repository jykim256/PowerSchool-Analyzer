from selenium import webdriver

username = 'XXXX'
password = 'XXXX'
schoolYear = ['2015', '2016']
driver = webdriver.Chrome()


def getRow(inputArray, k):
    row = ''
    ia = inputArray[k]
    row = ia.text
    try:
        if ia.find_element_by_tag_name('img').get_attribute('alt') == 'Excluded':
            row += 'EX '
    except Exception:
        row = row
    return row


# login
driver.get('https://powerschool.sandi.net/public/home.html')
driver.find_element_by_id('fieldAccount').send_keys(username)
driver.find_element_by_id('fieldPassword').send_keys(password)
driver.find_element_by_id('btn-enter').click()
# find classes
allLinks = driver.find_elements_by_tag_name('a')
gradeLinks = [0] * 6
gradeIndex = [17, 20, 23, 26, 29, 32]
for i in range(0, 6):
    gradeLinks[i] = allLinks[gradeIndex[i]].get_attribute('href')
# print(gradeLinks)

# get data from each class into one array
allAssignments = [[0 for _ in range(360)] for _ in range(6)]
for i in range(0, 6):
    counter = 0
    driver.get(gradeLinks[i])
    assignments = driver.find_elements_by_tag_name('tr')
    for j in range(len(assignments)):
        item = assignments[j].text
        if '/' in item and (schoolYear[0] in item or schoolYear[1] in item):
            allAssignments[i][counter] = getRow(assignments, j)
            # if j.get_attribute('alt') == 'Excluded':
            #   allAssignments[i][counter] = j.text + '$EXCLUDED'
            counter += 1
print(allAssignments)

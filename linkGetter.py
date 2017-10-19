from selenium import webdriver
import numpy as np
from PowerSchoolAnalysis import login

username = 'XXXX'
password = 'XXXX'


driver = webdriver.Chrome()
# login
login(driver, username, password)
# find classes
allLinks = driver.find_elements_by_tag_name('a')
classLinks = []
for i in range(len(allLinks)):
    if '\n' in allLinks[i].text:
        print(str(i) + ' ' + allLinks[i].text)
        classLinks.append(i)
# these are the links for the classLinks
classLinks = np.array(classLinks)
numQuarters = driver.find_element_by_class_name("th2").text.count(' ') - 7

classLinks = classLinks[0 + numQuarters - 1:len(classLinks):numQuarters]

classData = list(map(lambda x: [allLinks[x].get_attribute('href'), allLinks[x].text], classLinks))
print(classData)
print([classData[i][0] for i in range(len(classData))])
print('')
print(grades)
print([grades[i][0] for i in range(len(grades))])
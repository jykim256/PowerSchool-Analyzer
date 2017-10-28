import requests
import bs4
import numpy as np
from cleanTableR import getAssignmentRow, getClassNames, getUpdateHistory
import time


def getUserLogin():
   username = input('Enter your PowerSchool Username: ')
   password = input('Enter your PowerSchool Password: ')

   schoolYear = ''
   legitimateInput = False

   yes = ['yes', 'y']
   no = ['no', 'n']

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
            except:
               pass
            else:
               schoolYear = [str(2015 + intercept), str(2016 + intercept)]
               schoolCheck = False
               legitimateInput = True
      else:
         continue
   return[username, password, schoolYear]


def printTime(c0, message='.'):
   c1 = time.clock()
   print(str(round(c1 - c0, 2)) + ' secs elapsed ' + message)
   return c1


def login(s, username, password):
   LOGIN_URL = 'https://powerschool.sandi.net/guardian/home.html'
   payload = {
       'account': username,
       'pw': password,
       'ldappassword': password
   }
   return bs4.BeautifulSoup(s.post(LOGIN_URL, data=payload).text, 'lxml')


def getClassLinks(mainPage, schoolYear, gradingPeriod):
   # find the links to the grades and class links
   allLinks = mainPage.select('a')
   classLinks = []
   # go through each link that has <a> and find the class links
   for i in range(len(allLinks)):
      link = allLinks[i].get('href')
      if (schoolYear[0] in link or schoolYear[1] in link) and 'scores.html' in link and gradingPeriod in link:
         # #########################################################
         # ## CORRECT FOR WHEN THERE ARE P2 AND S2 IN THE GRADES ###
         # #########################################################
         classLinks.append(i)

   return np.array(list(map(lambda x: allLinks[x].get('href'), classLinks)), dtype=str)


def getAssignments(userInput, loginData=''):
   c0 = time.clock()
   username, password, schoolYear, fileName, gradingPeriod = userInput
   BASE_URL = 'https://powerschool.sandi.net/guardian/'
   with requests.Session() as s:
      # login to PowerSchool but check if data was already sent
      try:
         a = loginData + ''
      except:
         s = loginData[0]
         mainPage = loginData[1]
      else:
         mainPage = login(s, username, password)
      c0 = printTime(c0, 'logging in.')
      # get classLinks and grades
      classLinks = getClassLinks(mainPage, schoolYear, gradingPeriod)

      # get data from each class into one array
      allAssignments = ['' for _ in range(len(classLinks))]
      classes = [['', ''] for _ in range(len(classLinks))]
      print()
      for i in range(len(classLinks)):
         # go to each period
         classPage = bs4.BeautifulSoup(
             s.get(BASE_URL + classLinks[i]).text, 'lxml')
         # get the tr entries
         assignments = classPage.select('tr')
         # find all the assignments
         allAssignments[i] = list(map(lambda j: getAssignmentRow(
             assignments, i, j, schoolYear), range(3, len(assignments))))
         # get the update history
         classes[i] = [getClassNames(assignments), getUpdateHistory(classPage)]
      print()
      c0 = printTime(c0, 'grabbing assignment data.')
      # convert the lists to arrays
      for i in range(len(allAssignments)):
         allAssignments[i] = np.array(allAssignments[i], dtype=str)
      classes = np.array(classes, dtype=str)

      np.savez(fileName, allAssignments, classes)
      print('Data saved to file ' + fileName + ' in same directory')
   return [allAssignments, classes]


if __name__ == "__main__":
   username = 'XXXX'
   password = 'XXXX'
   schoolYear = ['2015', '2016']
   fileName = 'PSData.npz'
   gradingPeriod = 'P1'

   #username,password,schoolYear = getUserLogin()
   fileName = 'PSData.npz'
   userInput = [username, password, schoolYear, fileName, gradingPeriod]
   getAssignments(userInput)

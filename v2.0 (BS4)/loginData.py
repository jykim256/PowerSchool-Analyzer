import numpy as np
import time
from requestTester import login
import requests

username = 'XXXX'
password = 'XXXX'
BASE_URL = 'https://powerschool.sandi.net/guardian/'


def getData():
   dataSize = 500

   timeArray = np.array([0.0 for _ in range(dataSize)])

   for i in range(len(timeArray)):
      c0 = time.clock()
      with requests.Session() as s:
         _ = login(s, username, password)
         tDelta = time.clock() - c0
         timeArray[i] = tDelta
         print('Login #' + str(i + 1) + ': ' +
               str(round(tDelta, 3)) + ' seconds')
         s.close()
      s = 5
   np.savetxt('loginTimes.txt', timeArray)


def oneCheck():
   c0 = time.clock()
   with requests.Session() as s:
      _ = login(s, username, password)
      tDelta = time.clock() - c0
      print(str(round(tDelta, 3)) + ' seconds')


for i in range(4):
   time.sleep(2)
   oneCheck()

# getData()

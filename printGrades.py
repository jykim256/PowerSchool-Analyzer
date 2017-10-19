import numpy as np


# for the purpose of reading the grades
def printGrades(grades, indOrder):
    # sort the list by the column index
    grades.sort(key=lambda x: x[indOrder])

    # find the maximum # of chars in string for indenting purposes
    maxArray = [0 for _ in range(len(grades[0]))]
    for i in range(len(maxArray)):
        for j in range(len(grades)):
            if maxArray[i] < len(grades[j][i]):
                maxArray[i] = len(grades[j][i])
    # take each row as string, add periods inbetween
    numSpace = 2
    for i in range(len(grades)):
        s = ''
        for j in range(len(grades[i])):
            s += grades[i][j] + ''.join(['.' for _ in range(numSpace + maxArray[j] - len(grades[i][j]))])
        if not(grades[i][9] == 'E'):
            print(s)


def printCategories(catNames, num, den, grades, className):
    num = np.round(num, 3)
    den = np.round(den, 3)
    grades = np.round(grades, 3)
    max = 7
    for i in catNames:
        if max < len(i):
            max = len(i)
    numSpace = 2
    s = ''
    for i in catNames:
        s += str(i) + ''.join(['.' for _ in range(numSpace + max - len(i))])
    s += '\n'
    for i in num:
        s += str(i) + ''.join(['.' for _ in range(numSpace + max - len(str(i)))])
    s += '\n'
    for i in den:
        s += str(i) + ''.join(['.' for _ in range(numSpace + max - len(str(i)))])
    s += '\n'
    for i in grades:
        s += str(i) + ''.join(['.' for _ in range(numSpace + max - len(str(i)))])
    print(className)
    print(s)

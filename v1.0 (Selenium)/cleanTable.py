def cleanTable(assignments, i, j, schoolYear):
    if j == len(assignments) - 1:
        className = assignments[1].find_elements_by_tag_name('td')[0].text
        print('Found Class ' + str(i + 1) + ': ' + className + '!')
    # checks if the row is actually a row
    item = assignments[j].text
    if '/' in item and (schoolYear[0] in item or schoolYear[1] in item):
        row = ''
        # goes into each table column and adds the text
        rowElements = assignments[j].find_elements_by_tag_name('td')
        # separate the categories in each row
        for k in range(len(rowElements)):
            if not(k in range(3, 8)):
                row += rowElements[k].text + '|'
            else:
                row = row
        # print(row)
        # Some classes in case assignments are excluded
        try:
            row += assignments[j].find_element_by_tag_name('img').get_attribute('alt')
        except Exception:
            row = row
        return row
    else:
        return ''


# Returns the name of the class
def getClassNames(assignments):
    return assignments[1].find_elements_by_tag_name('td')[0].text


# Returns the date at when grade was last updated
def getUpdateHistory(driver):
    return driver.find_element_by_id('legend').find_element_by_class_name('center').text

import mysql.connector
from datetime import datetime

Host = "localhost"
user = ""
password = ""
database = "LPMdb"

def sanitiseSQLTerm():
    pass # ToDo, or check for existing functionality

def getCurrentSqlTimestamp():
    return str(datetime.utcnow())

def connectDB(Server = Host, Database = database, username = user, password = password):
    return mysql.connector.connect (
        host = Server,
        database = Database,
        user = username,
        passwd = password
    )

def getCursor(MyDBConnector):
    return MyDBConnector.cursor()

'''
    tableName is a string
    valueDict is a dictionary containing the column names as keys and the values as values.
'''
def getIdOfDataInTable(myCursor, tableName, valueDict):
    command = "SELECT * FROM `" + tableName + "`"
    initialCommandLength = len(command)
    for key in valueDict:
        command += " AND " if len(command) > initialCommandLength else " WHERE "
        command += "`" + key + "` = '" + str(valueDict[key]) + "'"
    command += ";"
    myCursor.execute(command)
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertDataIntoTable(myCursor, tableName, valueDict): # ToDo: put this in module to be referred from other pieces of code efficiently
    command = "INSERT INTO `" + tableName + "`(`id` "
    valueString = "NULL"
    for key in valueDict:
        command += ", `" + str(key) + "`"
        valueString += ", '" + str(valueDict[key]) + "'"
    command += ") VALUES (" + valueString + ");"
    myCursor.execute(command)

'''
    tableName is a string
    valueDict is a dictionary containing the column names as keys and the values as values.
    
    Check if the entry to be added already exists.
    If yes, simply return its id.
    If not, add it and a timestamp in editHistory and return its id.
'''
def ensureEntryInTable(myCursor, tableName, valueDict, userId='1'):
    entryId = getIdOfDataInTable(myCursor, tableName, valueDict)
    if entryId == -1:
        tableId = getIdOfDataInTable(myCursor, 'existingTables', {'tableName': tableName})
        insertDataIntoTable(myCursor, tableName, valueDict)
        entryId = getIdOfDataInTable(myCursor, tableName, valueDict)
        insertDataIntoTable(myCursor, 'editHistory', {'date': getCurrentSqlTimestamp(), 'userId': 1, 'tableId': tableId, 'rowId': entryId, 'description': 'Added'})
        protocolEntry = 'Successfully added entry: ' + str(valueDict)
    else:
        protocolEntry = 'Entry existed already: ' + str(valueDict)
    return {'entryId' : entryId, 'protocolEntry' : protocolEntry}

'''
    MySQL command for retrieval of a specific entry given a value of a specific column in a given table
'''
def getRowsByValue(myCursor, tableName, key, value):
    command = "SELECT * from `" + tableName + "` WHERE `" + key + "` = " + str(value)
    myCursor.execute(command)
    results = myCursor.fetchall()
    if len(results) > 0:
        return results
    return -1

def getFirstRowByValue(myCursor, tableName, key, value):
    rows = getRowsByValue(myCursor, tableName, key, value)
    return rows[0] if rows != -1 else -1

def getRowsByValues(myCursor, tableName, key, valueList):
    rows = list()
    for value in valueList:
        rows.extend(getRowsByValue(myCursor, tableName, key, value))
    return rows

'''
    This is the function which is going to be used in later releases
'''
def addTexDocumentEntryJSON(formData):
    print(formData)
    title = formData['title']
    path = formData['path']
    username = formData['author']
    filePathList = formData['files']

    informationArrayList = formData['informationArray']
    informationList=list()
    informationTypeList=list()
    for item in informationArrayList:
        informationList.append(item['information'])
        informationTypeList.append(item['type'])

    packageArrayList = formData['packages']
    packageList=list()
    packageOptionsList=list()
    for item in packageArrayList:
        packageList.append(item['package'])
        packageOptionsList.append(item['options'])
    
    return addTexDocumentEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList)


def addTexDocumentEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):
    mydbConnector = connectDB()
    myCursor = getCursor(mydbConnector)
    
    procedureProtocol = dict()
    procedureProtocol['databaseTableStatuses'] = dict()

    # Add content
    dataDictToAdd = {'title' : title, 'path' : path}
    insertionOutput = ensureEntryInTable(myCursor, 'contents', dataDictToAdd)
    contentId = insertionOutput['entryId']
    procedureProtocol['databaseTableStatuses']['contents'] = insertionOutput['protocolEntry']

    # Add user
    dataDictToAdd = {'username': username}
    insertionOutput = ensureEntryInTable(myCursor, 'users', dataDictToAdd)
    userId = insertionOutput['entryId']
    procedureProtocol['databaseTableStatuses']['users'] = insertionOutput['protocolEntry']
    
    # Add information type and information if not already existing
    informationTypeIds = list()
    informationIds = list()
    if len(informationTypeList) != len(informationList):
        print("Error! informationList and informationTypeList must be of same length!")
        procedureProtocol['databaseTableStatuses']['informationType'] = 'Error! informationList and informationTypeList must be of same length!'
        procedureProtocol['databaseTableStatuses']['information'] = 'Error! informationList and informationTypeList must be of same length!'
    else:
        procedureProtocol['databaseTableStatuses']['informationType'] = dict()
        procedureProtocol['databaseTableStatuses']['information'] = dict()
    for i in range(0, len(informationTypeList)):
        dataDictToAdd = {'type' : informationTypeList[i]}
        insertionOutput = ensureEntryInTable(myCursor, 'informationType', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['informationType'][str(i)] = insertionOutput['protocolEntry']
        informationTypeIds.append(insertionOutput['entryId'])

        dataDictToAdd = {'information' : informationList[i], 'informationTypeId' : insertionOutput['entryId']}
        insertionOutput = ensureEntryInTable(myCursor, 'information', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['information'][str(i)] = insertionOutput['protocolEntry']
        informationIds.append(insertionOutput['entryId'])

    # Add package and options combination if not already existing
    packageIds = list()
    packageOptionIds = list()
    if len(packageList) != len(packageOptionsList):
        print("Error! packageList and packageOptionsList must be of same length!")
        procedureProtocol['databaseTableStatuses']['packageOptions'] = 'Error! packageList and packageOptionsList must be of same length!'
        procedureProtocol['databaseTableStatuses']['packages'] = 'Error! packageList and packageOptionsList must be of same length!'
    else:
        procedureProtocol['databaseTableStatuses']['packageOptions'] = dict()
        procedureProtocol['databaseTableStatuses']['packages'] = dict()
        procedureProtocol['databaseTableStatuses']['packageRoption'] = dict()
        for i in range(0, len(packageList)):
            procedureProtocol['databaseTableStatuses']['packageRoption'][str(i)] = dict()
            dataDictToAdd = {'package' : packageList[i]}
            insertionOutput = ensureEntryInTable(myCursor, 'packages', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['packages'][str(i)] = insertionOutput['protocolEntry']
            packageIds.append(insertionOutput['entryId'])

            procedureProtocol['databaseTableStatuses']['packageOptions'][str(i)] = dict()
            packageOptionIds.append(list())

            for j in range(0, len(packageOptionsList[i])):
                dataDictToAdd = {'option' : packageOptionsList[i][j]}
                insertionOutput = ensureEntryInTable(myCursor, 'packageOptions', dataDictToAdd)
                procedureProtocol['databaseTableStatuses']['packageOptions'][str(i)] = insertionOutput['protocolEntry']
                packageOptionIds[i].append(insertionOutput['entryId'])

                # Add relation from package to package option
                dataDictToAdd = {'packageId' : packageIds[i], 'optionId' : insertionOutput['entryId']}
                insertionOutput = ensureEntryInTable(myCursor, 'packageRoption', dataDictToAdd)
                procedureProtocol['databaseTableStatuses']['packageRoption'][str(i)][str(j)] = insertionOutput['protocolEntry']

    # Add file paths if not already existing
    fileIds = list()
    procedureProtocol['databaseTableStatuses']['files'] = dict()
    for i in range(0, len(filePathList)):
        dataDictToAdd = {'path' : filePathList[i]}
        insertionOutput = ensureEntryInTable(myCursor, 'files', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['files'][str(i)] = insertionOutput['protocolEntry']
        fileIds.append(insertionOutput['entryId'])

    # Add contentRuser, contentRfile, contentRinformation and contentRpackages entry
    procedureProtocol['databaseTableStatuses']['contentRuser'] = dict()
    dataDictToAdd = {'contentId' : contentId, 'userId' : userId}
    insertionOutput = ensureEntryInTable(myCursor, 'contentRuser', dataDictToAdd)
    procedureProtocol['databaseTableStatuses']['contentRuser']['protocolEntry'] = insertionOutput['protocolEntry']

    procedureProtocol['databaseTableStatuses']['contentRfile'] = dict()
    for i in range(0, len(fileIds)):
        dataDictToAdd = {'contentId' : contentId, 'fileId' : fileIds[i]}
        insertionOutput = ensureEntryInTable(myCursor, 'contentRfile', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['contentRfile'][str(i)] = insertionOutput['protocolEntry']
    
    procedureProtocol['databaseTableStatuses']['contentRinformation'] = dict()
    for i in range(0, len(informationIds)):
        dataDictToAdd = {'contentId' : contentId, 'informationId' : informationIds[i]}
        insertionOutput = ensureEntryInTable(myCursor, 'contentRinformation', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = insertionOutput['protocolEntry']

    procedureProtocol['databaseTableStatuses']['contentRpackage'] = dict()
    for i in range(0, len(packageIds)):
        dataDictToAdd = {'contentId' : contentId, 'packageId' : packageIds[i]}
        if getIdOfDataInTable(myCursor, 'contentRpackage', dataDictToAdd) == -1:
            ensureEntryInTable(myCursor, 'contentRpackage', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRpackage'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRpackage'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

    mydbConnector.commit()
    mydbConnector.close()

    return procedureProtocol



def removeEntry(Id):
    pass



'''
    Return an entry if existing, -1 else.
    contentId: number
'''
def getTexDocumentEntry(contentId):
    mydbConnector = connectDB()
    myCursor = getCursor(mydbConnector)

    texDocumentEntry = dict()

    rows = getRowsByValue(myCursor, 'contents', 'id', contentId)
    if rows == -1:
        return -1
    row = rows[0]
    texDocumentEntry['title'] = row[1]
    texDocumentEntry['path'] = row[2]

    # todo: get the user who created the content entry via editHistory table
    index = getRowsByValue(myCursor, 'contentRuser', 'contentId', contentId)
    texDocumentEntry['username'] = getFirstRowByValue(myCursor, 'users', 'id', index[0][2])[1]

    indices = list()
    rows = getRowsByValue(myCursor, 'contentRfile', 'contentId', contentId)
    for row in rows:
        indices.append(row[2])
    texDocumentEntry['filePaths'] = dict()
    for i in range(0, len(indices)):
        texDocumentEntry['filePaths'][str(i)] = getFirstRowByValue(myCursor, 'files', 'id', indices[i])[1]

    texDocumentEntry['information'] = dict()
    indices = list()
    rows = getRowsByValue(myCursor, 'contentRinformation', 'contentId', contentId)
    for row in rows:
        indices.append(row[2])
    rows = getRowsByValues(myCursor, 'information', 'id', indices)
    for i in range(0, len(rows)):
        texDocumentEntry['information'][str(i)] = dict()
        texDocumentEntry['information'][str(i)]['information'] = row[1]
        texDocumentEntry['information'][str(i)]['type'] = getFirstRowByValue(myCursor, 'informationType', 'id', row[2])[1]
    

    texDocumentEntry['packages'] = dict()
    indices = list() # indices will hold the indices of packages belonging to the content
    rows = getRowsByValue(myCursor, 'contentRpackage', 'contentId', contentId)
    for row in rows:
        indices.append(row[2])
    rows = getRowsByValues(myCursor, 'packages', 'id', indices)
    for i in range(0, len(rows)):
        texDocumentEntry['packages'][str(i)] = dict()
        texDocumentEntry['packages'][str(i)]['package'] = rows[i][1]
        relationRows = getRowsByValue(myCursor, 'packageRoption', 'packageId', rows[i][0])
        texDocumentEntry['packages'][str(i)]['options'] = dict()
        for j in range(0, len(relationRows)):
            texDocumentEntry['packages'][str(i)]['options'][str(j)] = getFirstRowByValue(myCursor, 'packageOptions', 'id', relationRows[j][2])[1]
            
    mydbConnector.commit()
    mydbConnector.close()

    return texDocumentEntry

'''
    Return JSON-object containing the information of a TexDocument.
    Indicator is the contents table,
    extract the rows (and the corresponding data of the other tables)
    beginning from index startAt up to maxResults.
    startAt: number
    maxResults: number
'''
def getTexDocumentEntries(startAt, maxResults):
    texDocumentEntries = dict()
    for i in range(startAt, startAt + maxResults):
        candidate = getTexDocumentEntry(i)
        if candidate != -1:
            texDocumentEntries[str(i)] = candidate
        else:
            break
    return texDocumentEntries

if __name__ == "__main__":
    pass

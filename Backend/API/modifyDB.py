import mysql.connector
from datetime import datetime, timezone, timedelta

Host = "localhost"
user = ""
password = ""
database = "LPMdb"

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
    tableId = getIdOfDataInTable(myCursor, 'existingTables', {'tableName': tableName})
    entryId = getIdOfDataInTable(myCursor, tableName, valueDict)
    if entryId == -1:
        insertDataIntoTable(myCursor, tableName, valueDict)
        insertDataIntoTable(myCursor, 'editHistory', {'date': getCurrentSqlTimestamp(), 'userId': 1, 'tableId': tableId, 'rowId': entryId, 'description': 'Added'})
        protocolEntry = 'Successfully added entry: ' + str(valueDict)
    else:
        protocolEntry = 'Entry existed already: ' + str(valueDict)
    return {'entryId' : getIdOfDataInTable(myCursor, tableName, valueDict), 'protocolEntry' : protocolEntry}

'''
    MySQL command for retrieval of a specific entry given its id in a given table
'''
def getRowOfTable(myCursor, tableName, entryId):
    command = "SELECT * from `" + tableName + "` WHERE `id` = " + str(entryId)
    myCursor.execute(command)





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

    # Add contentRfiles, contentRinformation and contentRpackages entry
    procedureProtocol['databaseTableStatuses']['contentRfile'] = dict()
    for i in range(0, len(fileIds)):
        dataDictToAdd = {'contentId' : contentId, 'fileId' : fileIds[i]}
        if getIdOfDataInTable(myCursor, 'contentRfile', dataDictToAdd)== -1:
            ensureEntryInTable(myCursor, 'contentRfile', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRfile'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRfile'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)
    
    procedureProtocol['databaseTableStatuses']['contentRinformation'] = dict()
    for i in range(0, len(informationIds)):
        dataDictToAdd = {'contentId' : contentId, 'informationId' : informationIds[i]}
        if getIdOfDataInTable(myCursor, 'contentRinformation', dataDictToAdd) == -1:
            ensureEntryInTable(myCursor, 'contentRinformation', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

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
    index: number
'''
def getTexDocumentEntry(index):
    title = "TestTitle"
    path = "TestPath"
    username = "TestUsername"
    filePathList = ["fp1","fp2"]
    informationList = ["info1","info2"]
    informationTypeList = ["infoType1","infoType2"]
    packageList = ["package1","package2"]
    packageOptionsList = [["opt1","opt2","opt3"], ["opt3","opt4"]]

    texDocumentEntry = dict()
    # title
    texDocumentEntry['title'] = title
    # path
    texDocumentEntry['path'] = path
    # username
    texDocumentEntry['username'] = username
    # filePathList
    texDocumentEntry['filePaths'] = dict()
    for i in range(0, len(filePathList)):
        texDocumentEntry['filePaths'][str(i)] = filePathList[i]
    # informationList
    texDocumentEntry['information'] = dict()
    for i in range(0, len(informationList)):
        texDocumentEntry['information'][str(i)] = dict()
        texDocumentEntry['information'][str(i)]['information'] = informationList[i]
        texDocumentEntry['information'][str(i)]['type'] = informationTypeList[i]
    # packageList
    texDocumentEntry['packages'] = dict()
    for i in range(0, len(packageList)):
        texDocumentEntry['packages'][str(i)] = dict()
        texDocumentEntry['packages'][str(i)]['package'] = packageList[i]
        texDocumentEntry['packages'][str(i)]['options'] = dict()
        for j in range(0, len(packageOptionsList[i])):
            texDocumentEntry['packages'][str(i)]['options'][str(j)] = packageOptionsList[i][j]

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
    for i in range(startAt, startAt + maxResults):
        getTexDocumentEntry(i)
    return getTexDocumentEntry(0)

if __name__ == "__main__":
    pass

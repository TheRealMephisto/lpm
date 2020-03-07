import mysql.connector
from datetime import date

Host = "localhost"
user = ""
password = ""
database = "LPMdb"

def getTodaysSqlTimestamp():
    today = date.today()
    sqlTimestamp = str(today.year) + "-"
    if today.month < 10:
        sqlTimestamp += "0" + str(today.month) + "-"
    else:
        sqlTimestamp += str(today.month) + "-"
    if today.day < 10:
        sqlTimestamp += "0" + str(today.day)
    else:
        sqlTimestamp += str(today.day)
    return sqlTimestamp
    

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
    If not, add it and return its id.
'''
def ensureEntryInTable(myCursor, tableName, valueDict):
    entryId = getIdOfDataInTable(myCursor, tableName, valueDict)
    if entryId == -1:
        insertDataIntoTable(myCursor, tableName, valueDict)
        entryId = getIdOfDataInTable(myCursor, tableName, valueDict)
        protocolEntry = 'Successfully added entry: ' + str(valueDict)
    else:
        protocolEntry = 'Entry existed already: ' + str(valueDict)
    return {'entryId' : entryId, 'protocolEntry' : protocolEntry}



def addEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):
    mydbConnector = connectDB()
    myCursor = getCursor(mydbConnector)
    
    procedureProtocol = dict()
    procedureProtocol['databaseTableStatuses'] = dict()

    # Add content
    dataDictToAdd = {'title' : title, 'path' : path, 'creationDate' : getTodaysSqlTimestamp()}
    
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
        procedureProtocol['databaseTableStatuses']['packageRoptions'] = dict()
        for i in range(0, len(packageList)):
            procedureProtocol['databaseTableStatuses']['packageRoptions'][str(i)] = dict()
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
                insertionOutput = ensureEntryInTable(myCursor, 'packageRoptions', dataDictToAdd)
                procedureProtocol['databaseTableStatuses']['packageRoptions'][str(i)][str(j)] = insertionOutput['protocolEntry']

    # Add file paths if not already existing
    fileIds = list()
    procedureProtocol['databaseTableStatuses']['files'] = dict()
    for i in range(0, len(filePathList)):
        dataDictToAdd = {'path' : filePathList[i]}
        insertionOutput = ensureEntryInTable(myCursor, 'files', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['files'][str(i)] = insertionOutput['protocolEntry']
        fileIds.append(insertionOutput['entryId'])

    # Add contentRfiles, contentRinformation and contentRpackages entry
    procedureProtocol['databaseTableStatuses']['contentRfiles'] = dict()
    for i in range(0, len(fileIds)):
        dataDictToAdd = {'contentId' : contentId, 'fileId' : fileIds[i]}
        if getIdOfDataInTable(myCursor, 'contentRfiles', dataDictToAdd)== -1:
            ensureEntryInTable(myCursor, 'contentRfiles', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRfiles'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRfiles'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)
    
    procedureProtocol['databaseTableStatuses']['contentRinformation'] = dict()
    for i in range(0, len(informationIds)):
        dataDictToAdd = {'contentId' : contentId, 'informationId' : informationIds[i]}
        if getIdOfDataInTable(myCursor, 'contentRinformation', dataDictToAdd) == -1:
            ensureEntryInTable(myCursor, 'contentRinformation', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

    procedureProtocol['databaseTableStatuses']['contentRpackages'] = dict()
    for i in range(0, len(packageIds)):
        dataDictToAdd = {'contentId' : contentId, 'packageId' : packageIds[i]}
        if getIdOfDataInTable(myCursor, 'contentRpackages', dataDictToAdd) == -1:
            ensureEntryInTable(myCursor, 'contentRpackages', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRpackages'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRpackages'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

    mydbConnector.commit()
    mydbConnector.close()

    return procedureProtocol



def removeEntry(Id):
    pass



if __name__ == "__main__":
    pass

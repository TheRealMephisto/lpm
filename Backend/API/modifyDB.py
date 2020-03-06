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

def disconnect():
    pass

def getPackageId(myCursor, package):
    myCursor.execute("SELECT * FROM `packages` WHERE `package` = '" + package + "'")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertPackage(myCursor, package):
    myCursor.execute("INSERT INTO `packages` (`id`, `package`) VALUES (NULL, '" + package + "');")

def getPackageOptionId(myCursor, packageOption):
    myCursor.execute("SELECT * FROM `packageOptions` WHERE `option` = '" + packageOption + "'")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertPackageOption(myCursor, packageOption):
    myCursor.execute("INSERT INTO `packageOptions` (`id`, `packageOption`) VALUES (NULL, '" + packageOption + "');")

def getPackageROptionsId(myCursor, packageId, optionId):     
    myCursor.execute("SELECT * FROM `packageRoptions` WHERE `packageId` = " + packageId + " AND `optionId` = " + optionId + "")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertPackageROptions(myCursor, packageId, optionId):
    myCursor.execute("INSERT INTO `packageRoptions` (`id`, `packageId`, `optionId`) VALUES (NULL, " + str(packageId) + ", " + str(optionId) + ");")

def getFileId(myCursor, filePath):
    myCursor.execute("SELECT * FROM `files` WHERE `path` = '" + filePath + "' ")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertFile(myCursor, filePath):
    myCursor.execute("INSERT INTO `files` (`id`, `path`) VALUES (NULL, '" + filePath + "');")

def getContentRFileId(myCursor, contentId, fileId):     
    myCursor.execute("SELECT * FROM `contentRfiles` WHERE `contentId` = " + contentId + " AND `fileId` = " + fileId + "")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertContentRFile(myCursor, contentId, fileId):
    myCursor.execute("INSERT INTO `contentRfiles` (`id`, `contentId`, `fileId`) VALUES (NULL, " + str(contentId) + ", " + str(fileId) + ");")

def getContentRPackageId(myCursor, contentId, packageId):     
    myCursor.execute("SELECT * FROM `contentRpackages` WHERE `contentId` = " + contentId + " AND `fileId` = " + packageId + "")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertContentRPackage(myCursor, contentId, packageId):
    myCursor.execute("INSERT INTO `contentRpackages` (`id`, `contentId`, `packageId`) VALUES (NULL, " + str(contentId) + ", " + str(packageId) + ");")

def insertContentRInformation(myCursor, contentId, informationId):
    myCursor.execute("INSERT INTO `contentRinformation` (`id`, `contentId`, `informationId`) VALUES (NULL, " + str(contentId) + ", " + str(informationId) + ");")

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

'''
    tableName is a string
    valueDict is a dictionary containing the column names as keys and the values as values.
    
    Check if the entry to be added already exists.
    If yes, simply return its id.
    If not, add it and return its id.
'''
def insertDataIntoTable(myCursor, tableName, valueDict):
    entryId = getIdOfDataInTable(myCursor, tableName, valueDict)
    if entryId == -1:
        command = "INSERT INTO `" + tableName + "`(`id`"
        valueString = "NULL"
        for key in valueDict:
            command += ", `" + str(key) + "`"
            valueString += ", '" + str(valueDict[key]) + "'"
        command += ") VALUES (" + valueString + ");"
        myCursor.execute(command)
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
    
    insertionOutput = insertDataIntoTable(myCursor, 'contents', dataDictToAdd)
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
        insertionOutput = insertDataIntoTable(myCursor, 'informationType', dataDictToAdd)
        informationTypeId = insertionOutput['entryId']
        procedureProtocol['databaseTableStatuses']['informationType'][str(i)] = insertionOutput['protocolEntry']
        informationTypeIds.append(informationTypeId)

        dataDictToAdd = {'information' : informationList[i], 'informationTypeId' : informationTypeId}
        insertionOutput = insertDataIntoTable(myCursor, 'information', dataDictToAdd)
        informationId = insertionOutput['entryId']
        procedureProtocol['databaseTableStatuses']['information'][str(i)] = insertionOutput['protocolEntry']
        informationIds.append(informationId)


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
            insertionOutput = insertDataIntoTable(myCursor, 'packages', dataDictToAdd)
            packageId = insertionOutput['entryId']
            procedureProtocol['databaseTableStatuses']['packages'][str(i)] = insertionOutput['protocolEntry']
            packageIds.append(packageId)

            procedureProtocol['databaseTableStatuses']['packageOptions'][str(i)] = dict()
            packageOptionIds.append(list())

            for j in range(0, len(packageOptionsList[i])):
                dataDictToAdd = {'option' : packageOptionsList[i][j]}
                insertionOutput = insertDataIntoTable(myCursor, 'packageOptions', dataDictToAdd)
                packageOptionId = insertionOutput['entryId']
                procedureProtocol['databaseTableStatuses']['packageOptions'][str(i)] = insertionOutput['protocolEntry']
                packageOptionIds[i].append(packageOptionId)

                # Add relation from package to package option
                dataDictToAdd = {'packageId' : packageIds[i], 'optionId' : packageOptionId}
                insertionOutput = insertDataIntoTable(myCursor, 'packageRoptions', dataDictToAdd)
                procedureProtocol['databaseTableStatuses']['packageRoptions'][str(i)][str(j)] = insertionOutput['protocolEntry']

    # Add file paths if not already existing
    fileIds = list()
    procedureProtocol['databaseTableStatuses']['files'] = dict()
    for i in range(0, len(filePathList)):
        dataDictToAdd = {'path' : filePathList[i]}
        insertionOutput = insertDataIntoTable(myCursor, 'files', dataDictToAdd)
        fileId = insertionOutput['entryId']
        procedureProtocol['databaseTableStatuses']['files'][str(i)] = insertionOutput['protocolEntry']
        fileIds.append(fileId)


    # Add contentRfiles, contentRinformation and contentRpackages entry
    procedureProtocol['databaseTableStatuses']['contentRfiles'] = dict()
    for i in range(0, len(fileIds)):
        dataDictToAdd = {'contentId' : contentId, 'fileId' : fileIds[i]}
        relationId = getIdOfDataInTable(myCursor, 'contentRfiles', dataDictToAdd)
        if relationId == -1:
            insertDataIntoTable(myCursor, 'contentRfiles', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRfiles'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRfiles'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)
    
    procedureProtocol['databaseTableStatuses']['contentRinformation'] = dict()
    for i in range(0, len(informationIds)):
        dataDictToAdd = {'contentId' : contentId, 'informationId' : informationIds[i]}
        relationId = getIdOfDataInTable(myCursor, 'contentRinformation', dataDictToAdd)
        if relationId == -1:
            insertDataIntoTable(myCursor, 'contentRinformation', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

    procedureProtocol['databaseTableStatuses']['contentRpackages'] = dict()
    for i in range(0, len(packageIds)):
        dataDictToAdd = {'contentId' : contentId, 'packageId' : packageIds[i]}
        relationId = getIdOfDataInTable(myCursor, 'contentRpackages', dataDictToAdd)
        if relationId == -1:
            insertDataIntoTable(myCursor, 'contentRpackages', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRpackages'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['contentRpackages'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

    mydbConnector.commit()
    mydbConnector.close()

    return procedureProtocol

def removeEntry(Id):
    pass

if __name__ == "__main__":
    addEntry("testtitle", "testpath", "testusername", ["testfilepath"], ["infotest"], ["infotesttype2"], ["testpkg2"], ["testopt2"])


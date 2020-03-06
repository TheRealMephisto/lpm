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
'''
def insertDataIntoTable(myCursor, tableName, valueDict):
    command = "INSERT INTO `" + tableName + "`(`id`"
    valueString = "NULL"
    for key in valueDict:
        command += ", `" + str(key) + "`"
        valueString += ", '" + str(valueDict[key]) + "'"
    command += ") VALUES (" + valueString + ");"
    myCursor.execute(command)


def addEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):
    mydbConnector = connectDB()
    myCursor = getCursor(mydbConnector)
    
    procedureProtocol = dict()
    procedureProtocol['databaseTableStatuses'] = dict()

    # Add content
    dataDictToAdd = {'title' : title, 'path' : path, 'creationDate' : getTodaysSqlTimestamp()}
    contentId = getIdOfDataInTable(myCursor, 'contents', dataDictToAdd)

    if contentId == -1:
        insertDataIntoTable(myCursor, 'contents', dataDictToAdd)
        contentId = getIdOfDataInTable(myCursor, 'contents', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['contents'] = 'Successfully added entry: ' + str(dataDictToAdd)
    else:
        print("This content already exists! Consider editing it instead of adding it again. Aborting...")
        procedureProtocol['databaseTableStatuses']['contents'] = 'Entry existed already: ' + str(dataDictToAdd)
    
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
        informationTypeId = getIdOfDataInTable(myCursor, 'informationType', dataDictToAdd)
        if informationTypeId == -1:
            insertDataIntoTable(myCursor, 'informationType', dataDictToAdd)
            informationTypeId = getIdOfDataInTable(myCursor, 'informationType', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['informationType'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['informationType'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)
        informationTypeIds.append(informationTypeId)

        dataDictToAdd = {'information' : informationList[i], 'informationTypeId' : informationTypeId}
        informationId = getIdOfDataInTable(myCursor, 'information', dataDictToAdd)
        if informationId == -1:
            insertDataIntoTable(myCursor, 'information', dataDictToAdd)
            informationId = getIdOfDataInTable(myCursor, 'information', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['information'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['information'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)
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
    for i in range(0, len(packageList)):
        dataDictToAdd = {'package' : packageList[i]}
        packageId = getIdOfDataInTable(myCursor, 'packages', dataDictToAdd)
        if packageId == -1:
            insertDataIntoTable(myCursor, 'packages', dataDictToAdd)
            informationTypeId = getIdOfDataInTable(myCursor, 'packages', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['packages'][str(i)] = 'Successfully added entry: ' + str(dataDictToAdd)
        else:
            procedureProtocol['databaseTableStatuses']['packages'][str(i)] = 'Entry existed already: ' + str(dataDictToAdd)

    # Add file paths if not already existing
    fileIds = list()
    for filePath in filePathList:
        fileId = getFileId(myCursor, filePath)
        if fileId == -1:
            insertFile(myCursor, filePath)
            fileId = getFileId(myCursor, filePath)
        fileIds.append(fileId)

    # Add contentRfile entry and contentRinformation entry
    for fileId in fileIds:
        insertContentRFile(myCursor, contentId, fileId)    
    for informationId in informationIds:
        insertContentRInformation(myCursor, contentId, informationId)

    mydbConnector.commit()
    mydbConnector.close()

def removeEntry(Id):
    pass

def test():
    addEntry("testtitle", "testpath", "testusername", ["testfilepath"], ["infotest"], ["infotesttype2"], ["testpkg2"], ["testopt2"])
    addEntry("testtitle2", "testpath2", "testusername", ["testfilepath"], ["infotest"], ["infotesttype2"], ["testpkg2"], ["testopt2"])
    addEntry("testtitle3", "testpath3", "testusername", ["testfilepath1", "testfilepath2", "testfilepath3"], ["infotest1", "infotest2", "infotest3"], ["infotesttype1", "infotesttype2", "infotesttype3"], ["testpkg1", "testpkg2", "testpkg3"], [["testopt1", "testopt2", "testopt3"], ["testopt4", "testopt5", "testopt6"], ["testopt3", "testopt7", "testopt8"]])


if __name__ == "__main__":
    addEntry("testtitle", "testpath", "testusername", ["testfilepath"], ["infotest"], ["infotesttype2"], ["testpkg2"], ["testopt2"])


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

'''
    Check information type table and retrieve Id, if existing.
    Returns -1 if not existing.
'''
def getInformationTypeId(myCursor, informationType):
    myCursor.execute("SELECT * FROM `informationType` WHERE `type` = '" + informationType + "';")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertInformationType(myCursor, informationType):
    myCursor.execute("INSERT INTO `informationType` (`id`, `type`) VALUES (NULL, '" + informationType + "');")

def getInformationId(myCursor, information):
    myCursor.execute("SELECT * FROM `information` WHERE `information` = '" + information + "';")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertInformation(myCursor, information, informationTypeId):
    myCursor.execute("INSERT INTO `information` (`id`, `information`, `informationTypeId`) VALUES (NULL, '" + information + "', '" + str(informationTypeId) + "');")

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

def getContentId(myCursor, title, path, date = getTodaysSqlTimestamp()):
    myCursor.execute("SELECT * FROM `contents` WHERE `title` = '" + title + "' AND `creationDate` = '" + date + "' AND `path` = '" + path + "';")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertContent(myCursor, title, path, date = getTodaysSqlTimestamp()):
    myCursor.execute("INSERT INTO `contents` (`id`, `title`, `creationDate`, `path`) VALUES (NULL, '" + title + "', '" + date + "', '" + path + "');")

def addEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):
    mydbConnector = connectDB()
    myCursor = getCursor(mydbConnector)

    # Add content
    contentId = getContentId(myCursor, title, path)
    if contentId == -1:
        insertContent(myCursor, title, path)
        contentId = getContentId(myCursor, title, path)
    else:
        print("This content already exists! Consider editing it instead of adding it again. Aborting...")
        mydbConnector.close()
        return
    
    # Add information type and information if not already existing
    informationTypeIds = list()
    informationIds = list()
    if len(informationTypeList) != len(informationList):
        print("Error! informationList and informationTypeList must be of same length!")
        return
    for i in range(0, len(informationTypeList)):
        informationTypeId = getInformationTypeId(myCursor, informationTypeList[i])
        if informationTypeId == -1:
            insertInformationType(myCursor, informationTypeList[i])
            informationTypeId = getInformationTypeId(myCursor, informationTypeList[i])
        informationTypeIds.append(informationTypeId)
        informationId = getInformationId(myCursor, informationList[i])
        if informationId == -1:
            insertInformation(myCursor, informationList[i], informationTypeId)
            informationId = getInformationId(myCursor, informationList[i])
        informationIds.append(informationId)

    # Add package and options combination if not already existing
    packageIds = list()
    packageOptionIds = list()
    if len(packageList) != len(packageOptionsList):
        print("Error! packageList and packageOptionsList must be of same length!")
        return
    for i in range(0, len(packageList)):
        pass

    #for package in packageList:
    #    for packageOptions in packageOptionsList:
    #        PkgOptId = getPackageAndOptionsId(myCursor, package, packageOption)
    #        if PkgOptId == -1:
    #            insertPackageAndOptions(myCursor, package, packageOption)
    #            PkgOptId = getPackageAndOptionsId(myCursor, package, packageOption)

    #
    #fileTypeIds = list()
    #fileType in fileTypes:
    #    fileTypeId = getFileTypeId(myCursor, fileType)
    #    pass

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
    addEntry("testtitle3", "testpath3", "testusername", ["testfilepath", "2", "3"], ["infotest", "2", "3"], ["infotesttype2", "2", "3"], ["testpkg2", "2", "3"], [["testopt2", "2", "3"], ["testopt4", "5", "6"], ["testopt3", "7", "8"]])


if __name__ == "__main__":
    addEntry("testtitle", "testpath", "testusername", ["testfilepath"], ["infotest"], ["infotesttype2"], ["testpkg2"], ["testopt2"])


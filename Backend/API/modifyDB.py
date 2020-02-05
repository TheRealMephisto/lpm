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
    Check information type table and retrieve id, if existing.
    Returns -1 if not existing.
'''
def getInformationTypeID(myCursor, informationType):
    myCursor.execute("SELECT * FROM `informationType` WHERE `type` = '" + informationType + "';")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertInformationType(myCursor, informationType):
    myCursor.execute("INSERT INTO `informationType` (`id`, `type`) VALUES (NULL, '" + informationType + "');")

def getPackageAndOptionsID(myCursor, package, packageOptions):
    myCursor.execute("SELECT * FROM `packages` WHERE `package` = '" + package + "' AND `options` = '" + packageOptions + "'")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertPackageAndOptions(myCursor, package, packageOptions):
    myCursor.execute("INSERT INTO `packages` (`id`, `package`, `options`) VALUES (NULL, '" + package + "', '" + packageOptions + "');")

def getFileID(myCursor, filePath):
    myCursor.execute("SELECT * FROM `files` WHERE `path` = '" + filePath + "' ")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertFile(myCursor, filePath):
    myCursor.execute("INSERT INTO `files` (`id`, `path`) VALUES (NULL, '" + filePath + "');")

def getContentRFileID(myCursor, contentID, fileID):     
    myCursor.execute("SELECT * FROM `contentRfiles` WHERE `contentID` = " + contentId + " AND `fileID` = " + fileID + "")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1
    pass

def insertContentRFile(myCursor, contentID, fileID):
    myCursor.execute("INSERT INTO `contentRfiles` (`id`, `contentID`, `fileID`) VALUES (NULL, " + str(contentID) + ", " + str(fileID) + ");")

def getContentID(myCursor, title, path, date = getTodaysSqlTimestamp()):
    myCursor.execute("SELECT * FROM `contents` WHERE `title` = '" + title + "' AND `creationDate` = '" + date + "' AND `path` = '" + path + "';")
    results = myCursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    return -1

def insertContent(myCursor, title, path, date = getTodaysSqlTimestamp()):
    myCursor.execute("INSERT INTO `contents` (`id`, `title`, `creationDate`, `path`) VALUES (NULL, '" + title + "', '" + date + "', '" + path + "');")

def addEntry(title, path, username, filePaths, information, informationType, package, packageOptions):
    mydbConnector = connectDB()
    myCursor = getCursor(mydbConnector)
    
    # Add information type if not already existing
    InformationTypeID = getInformationTypeID(myCursor, informationType)
    if InformationTypeID == -1:
        insertInformationType(myCursor, informationType)
        InformationTypeID = getInformationTypeID(myCursor, informationType)

    # Add package and options combination if not already existing
    PkgOptID = getPackageAndOptionsID(myCursor, package, packageOptions)
    if PkgOptID == -1:
        insertPackageAndOptions(myCursor, package, packageOptions)
        PkgOptID = getPackageAndOptionsID(myCursor, package, packageOptions)

    #
    #fileTypeIDs = list()
    #fileType in fileTypes:
    #    fileTypeID = getFileTypeID(myCursor, fileType)
    #    pass

    # Add file paths if not already existing
    fileIDs = list()
    for filePath in filePaths:
        fileID = getFileID(myCursor, filePath)
        if fileID == -1:
            insertFile(myCursor, filePath)
            fileID = getFileID(myCursor, filePath)
        fileIDs.append(fileID)

    # Add content
    insertContent(myCursor, title, path)
    contentID = getContentID(myCursor, title, path)

    # Add contentRfile
    for fileID in fileIDs:
        insertContentRFile(myCursor, contentID, fileID)    

    mydbConnector.commit()
    mydbConnector.close()

def removeEntry(id):
    pass

if __name__ == "__main__":
    addEntry("testtitle", "testpath", "testusername", "testfilepath", "infotest", "infotesttype2", "testpkg2", "testopt2")


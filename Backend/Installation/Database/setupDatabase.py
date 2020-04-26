import mysql.connector

def loadConfig( Filepath ):
    pass


def ensureExistenceOfDatabase( MyCursor, DatabaseName ):
    MyCursor.execute("SHOW DATABASES")
    dbExists = False
    for x in MyCursor:
        if x[0] == DatabaseName:
            dbExists = True
            break
    if not dbExists:
        MyCursor.execute("CREATE DATABASE " + DatabaseName)
        print("Successfully created MySQL Database LPMdb")
    else:
        print("MySQL Database LPMdb already exists! Skipped creation.")



def ensureExistenceOfTables (TablesToCreate, MyCursor, DatabaseName):
    MyCursor.execute("SHOW TABLES")
    results = MyCursor.fetchall()

    for key in TablesToCreate:
        if (key, ) not in results:
            mycursor.execute(TablesToCreate[key])
            print("Successfully created table " + key)
        else:
            print("Table " + key + " already exists! Skipped creation.")

def insertDataIntoTable(myCursor, tableName, valueDict): # ToDo: put this in module to be referred from other pieces of code efficiently
    command = "INSERT INTO `" + tableName + "`(`id` "
    valueString = "NULL"
    for key in valueDict:
        command += ", `" + str(key) + "`"
        valueString += ", '" + str(valueDict[key]) + "'"
    command += ") VALUES (" + valueString + ");"
    myCursor.execute(command)



if __name__ == "__main__":

    DatabaseName = "LPMdb"

    #username = input("Enter username of your MySQL / MariaDB Database: ")
    #password = input("Password: ")

    mydb = mysql.connector.connect (
        host = "localhost",
        user = "max",
        passwd = "V#3$4mxQLnin.1"
    )

    mycursor = mydb.cursor()

    ensureExistenceOfDatabase(mycursor, DatabaseName)

    # Connect to Database
    mydb.connect (
        database = DatabaseName
    )

    # Create tables if not already existing
    TablesToCreate = {
        "contents" : "CREATE TABLE contents (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), mainFileRefId INT)", # Info: mainFileRefId points to an entry in table "contentRfile", specifying the main tex file of this content
        "information" : "CREATE TABLE information (id INT AUTO_INCREMENT PRIMARY KEY, information TEXT, informationTypeId INT)",
        "informationType" : "CREATE TABLE informationType (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255))",
        "files" : "CREATE TABLE files (id INT AUTO_INCREMENT PRIMARY KEY, path TEXT, content TEXT)",
        "contentRfile" : "CREATE TABLE contentRfile (id INT AUTO_INCREMENT PRIMARY KEY, contentId INT, fileId INT)",
        "contentRinformation" : "CREATE TABLE contentRinformation (id INT AUTO_INCREMENT PRIMARY KEY, contentId INT, informationId INT)",
        "contentRpackage" : "CREATE TABLE contentRpackage (id INT AUTO_INCREMENT PRIMARY KEY, contentId INT, packageId INT)",
        "contentRuser" : "CREATE TABLE contentRuser (id INT AUTO_INCREMENT PRIMARY KEY, contentId INT, userId INT)",
        "packages" : "CREATE TABLE packages (id INT AUTO_INCREMENT PRIMARY KEY, package VARCHAR(255), description VARCHAR(255))",
        "packageRoption": "CREATE TABLE packageRoption (id INT AUTO_INCREMENT PRIMARY KEY, packageId INT, optionId INT)",
        "packageOptions": "CREATE TABLE packageOptions (id INT AUTO_INCREMENT PRIMARY KEY, option VARCHAR(255), description VARCHAR(255))",
        "editHistory" : "CREATE TABLE editHistory (id INT AUTO_INCREMENT PRIMARY KEY, date TIMESTAMP, userId INT, tableId INT, rowId INT, description VARCHAR(255))", # is this functionality really needed? Compare use with effort!
        "users" : "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255))",
        "existingTables" : "CREATE TABLE existingTables (id INT AUTO_INCREMENT PRIMARY KEY, tableName VARCHAR(255))"
    }

    ensureExistenceOfTables(TablesToCreate, mycursor, DatabaseName)

    for key in TablesToCreate:
        insertDataIntoTable(mycursor, 'existingTables', {'tableName' : key})

    informationTypes = ['creationDate', 'editDate', 'targetGroupId', 'version', 'keywords', 'useDate']
    for infoType in informationTypes:
        insertDataIntoTable(mycursor, 'informationType', {'type': infoType})

    mydb.commit()
    mydb.close()
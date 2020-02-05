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





if __name__ == "__main__":

    DatabaseName = "LPMdb"

    #username = input("Enter username of your MySQL / MariaDB Database: ")
    #password = input("Password: ")

    mydb = mysql.connector.connect (
        host = "localhost",
        user = "",
        passwd = ""
    )

    mycursor = mydb.cursor()

    ensureExistenceOfDatabase(mycursor, DatabaseName)

    # Connect to Database
    mydb.connect (
        database = DatabaseName
    )

    # Create tables if not already existing
    TablesToCreate = {
        "contents" : "CREATE TABLE contents (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), creationDate DATE , path VARCHAR(255))",
        "information" : "CREATE TABLE information (id INT AUTO_INCREMENT PRIMARY KEY, information TEXT, informationTypeId INT)",
        "informationType" : "CREATE TABLE informationType (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255))",
        "files" : "CREATE TABLE files (id INT AUTO_INCREMENT PRIMARY KEY, path TEXT)",
        "contentRfiles" : "CREATE TABLE contentRfiles (id INT AUTO_INCREMENT PRIMARY KEY, contentID INT, fileID INT)",
        #"fileTypes" : "CREATE TABLE fileTypes (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255))",
        "packages" : "CREATE TABLE packages (id INT AUTO_INCREMENT PRIMARY KEY, package VARCHAR(255), options VARCHAR(255))",
        "editHistory" : "CREATE TABLE editHistory (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, userId INT)",
        "users" : "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255))"
    }

    ensureExistenceOfTables(TablesToCreate, mycursor, DatabaseName)
import mysql.connector

import sys
sys.path.append('/etc/lpm/libraries')
from configUtils import ConfigReader
from dbUtils import dbConnector
from dbUtils import dbReader
from dbUtils import dbWriter

def ensureExistenceOfDatabase(DatabaseName):
    mydb = mysql.connector.connect (
            host = db_config['host'],
            user = db_config['user'],
            passwd = db_config['password']
        )
    MyCursor = mydb.cursor(buffered=True)
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
    mydb.commit()
    mydb.close()

TablesToCreate = {
                "contents" : "CREATE TABLE contents (id INT AUTO_INCREMENT PRIMARY KEY, className VARCHAR(255));",
                "information" : "CREATE TABLE information (id INT AUTO_INCREMENT PRIMARY KEY, value TEXT, linkedContentId INT, specificationId INT);",
                "contentRinformation" : "CREATE TABLE contentRinformation (id INT AUTO_INCREMENT PRIMARY KEY, contentId INT, informationId INT);",
                "contentRuser" : "CREATE TABLE contentRuser (id INT AUTO_INCREMENT PRIMARY KEY, contentId INT, userId INT);",
                "users" : "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255));",
                "specifications": "CREATE TABLE specifications (id INT AUTO_INCREMENT PRIMARY KEY, className VARCHAR(255), label VARCHAR(255), dataType VARCHAR(255), mandatory TINYINT DEFAULT 0, array TINYINT DEFAULT 0);",
                "history": "CREATE TABLE history (id INT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, type CHAR NULL DEFAULT NULL, jsonContent LONGTEXT, contentId INT NOT NULL DEFAULT -1);"
            }


if __name__ == "__main__":

    with ConfigReader.ConfigReader() as configReader:
        db_config = configReader.get_db_config()['Database']
        content_config = configReader.get_content_config()

        DatabaseName = db_config['database']

        ensureExistenceOfDatabase(DatabaseName)

        with dbWriter.dbWriter() as db_writer:

            db_writer.ensureExistenceOfTables(TablesToCreate, DatabaseName)

            specifications = list()
            for className in content_config:
                for config_key in content_config[className].keys():
                    for label, specs in content_config[className][config_key].items():
                        specifications.append({
                            'className': className,
                            'label': label,
                            'dataType': specs["dataType"],
                            'mandatory': 1 if config_key == 'mandatory' else 0,
                            'array': 1 if specs['array'] == True else 0
                        })

            for spec in specifications:
                db_writer.insertDataIntoTable('specifications', spec)
            
            db_writer.insertDataIntoTable('users', {"username": "admin"})

            db_writer.commit_write_queries()

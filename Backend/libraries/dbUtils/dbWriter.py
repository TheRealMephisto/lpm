import dbUtils
from dbUtils.dbConnector import dbConnector
from dbUtils.dbReader import dbReader
from InternalModel.TexDocument import TexDocument
from InternalModel.ContentObject import ContentObject
from InternalModel.ContentObjectHelper import ContentObjectHelper
from datetime import datetime

class dbWriter:

    def __init__(self):
        self.dbConnection = dbConnector()
        self.procedureProtocol = dict()
        self.userId = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dbConnection.close_connection()
        return

    def commit_write_queries(self):
        self.dbConnection.commit()

    def getCurrentSqlTimestamp(self):
        return str(datetime.utcnow())

    def ensureExistenceOfTables(self, TableCreationQueries, DatabaseName):
        tables = self.dbConnection.execute_read_query("SHOW TABLES;")
        if tables == -1:
            tables = []
        for key in TableCreationQueries:
            if (key, ) not in tables:
                self.dbConnection.append_write_query(TableCreationQueries[key])
                print("Successfully scheduled creation of table " + key)
            else:
                print("Table " + key + " already exists! Skipped creation.")
        self.commit_write_queries()
        print("Executed creation of all scheduled tables!")

    def insertDataIntoTable(self, tableName, valueDict):
        command = "INSERT INTO `{t}` (`id` ".format(t=tableName)
        valueString = "NULL"
        argsList = list()
        for key in valueDict:
            command += ", {k}".format(k=key)
            valueString += ", %s"
            argsList.append(str(valueDict[key]))
        command += ") VALUES ({v});".format(v=valueString)
        return self.dbConnection.append_write_query(command, argsList)

    def ensureEntryInTable(self, valueDict, tableName, protocolDepthIdentifiers = [], matchMode = False):
        '''
            tableName is a string
            valueDict is a dictionary containing the column names as keys and the values as values.
            
            Check if the entry to be added already exists.
            If yes, simply return its id.
            If not, insert it and return its id.
        '''
        with dbReader(self.dbConnection) as db_reader:
            entry = db_reader.getDbEntryIfPresent(tableName, valueDict, matchMode)
            if entry == -1:
                self.insertDataIntoTable(tableName, valueDict)
                entry = db_reader.getDbEntryIfPresent(tableName, valueDict, matchMode)

                if self.userId is None:
                    if tableName == 'users':
                        self.userId = entry['id']
                    else:
                        protocol_message = 'No valid userId provided!'

                protocol_message = 'Successfully added entry: ' + str(valueDict)
            else:
                protocol_message = 'Entry existed already: ' + str(valueDict)
        
        self.procedureProtocol[tableName] = self.create_protocol_entry(protocol_message, protocolDepthIdentifiers)
        
        return entry['id']

    def create_protocol_entry(self, message, depth_identifiers = []):
        if len(depth_identifiers) == 0:
            entry = message
        else:
            entry = dict()
            entry[depth_identifiers[0]] = self.create_protocol_entry(message, depth_identifiers[1:])
        return entry

    def editContentEntry(self, entry, contentId):
        '''
            Description should go here ...
        '''
        with dbReader(self.dbConnection) as db_reader:
            userEntry = db_reader.getDbEntryIfPresent("users", {"username": entry["user"]})
            if userEntry == -1:
                raise Exception("The provided user does not exist.")
        
            try:
                sanitised_content_object = ContentObject(entry["className"], entry["user"], entry["information"], db_reader)
            except:
                return {"success": False, "ErrorMessage": "Could not sanitise entry."}

            old_content_object = db_reader.getTexDocumentEntries(contentId, 1)["1"]
            
            calculated_updates = {}
            with ContentObjectHelper() as helper:
               calculated_updates = helper.calculate_updates(sanitised_content_object, old_content_object)

            if len(calculated_updates.keys()) != 3:
                return {"success": False, "ErrorMessage": "Error while calculating changes to be applied to the database."}
            if len(calculated_updates["information_ids_to_unlink"]) > 0:
                unlink_information_from_content_entry_command = dbUtils._unlink_information_from_content_entry_command

                for index in range(0, len(calculated_updates["information_ids_to_unlink"])-1):
                    unlink_information_from_content_entry_command += ", %s"
                unlink_information_from_content_entry_command += ");"

                self.dbConnection.append_write_query(unlink_information_from_content_entry_command, [contentId] + calculated_updates["information_ids_to_unlink"])
            
            for info_update in calculated_updates["information_updates"]:
                self.dbConnection.append_write_query(dbUtils._update_information_entry_command, [info_update["value"], info_update["Id"]])

            for new_info in calculated_updates["new_information"]:
                self._insert_information_entry(new_info["value"], new_info["specId"], contentId)

            self.insertDataIntoTable("history", 
                {
                    "type": 'e',
                    "jsonContent": str(entry),
                    "contentId": contentId
                }
            )
            self.dbConnection.commit()

            return {"success": True}

        return {"success": False, "ErrorMessage": "Could not initiliase database reader."}

    def addContentEntry(self, entry):
        '''
            Description goes here...

            example entry:
            {
                className: ...,
                user: (the user editing this entry),
                information: 
                [
                    {
                        value: (the content of the information, can be string or another contentEntry object),
                        label : (the label of the information piece),
                        dataType: (can be a basic type or one that occurs as className in specifications, using [] at the end to represent an array),
                        mandatory: (true / false)
                    },
                    ...
                ]
            }

            label, dataType and mandatory will be saved in table specifications
            className will be saved in table contents
            information will be saved in table information
        '''
        with dbReader(self.dbConnection) as db_reader:
            userEntry = db_reader.getDbEntryIfPresent("users", {"username": entry["user"]})
            if userEntry == -1:
                raise Exception("The provided user does not exist.")
        
            try:
                sanitised_content_object = ContentObject(entry["className"], entry["user"], entry["information"], db_reader)
            except:
                return "Something went wrong"

            contentId = self._insert_content_entry(sanitised_content_object.entry, userEntry["id"], db_reader)

            self.insertDataIntoTable("history", 
                {
                    "type": 'a',
                    "jsonContent": str(entry),
                    "contentId": contentId
                }
            )

            self.dbConnection.commit()
            
            return contentId

        raise Exception("Unable to read from database")

    def _insert_content_entry(self, entry, userId, db_reader):
        '''
            Insert the content entry.
            This function is recursive and returns the id of the inserted row of the content entry,
            to be used in the recursive calls of itself.
        '''
        contentId = self.insertDataIntoTable(
            "contents",
            {
                "className": entry["className"]
            }
        )

        for information in entry["information"]:
            if type(information["value"]) == dict:
                linkedContentId = self._insert_content_entry(information["value"], userId, db_reader)
                self._insert_information_entry("", information["specId"], contentId, linkedContentId)
            elif type(information["value"]) == list:
                for value in information["value"]:
                    if type(value) == dict:
                        linkedContentId = self._insert_content_entry(value, userId, db_reader)
                        self._insert_information_entry("", information["specId"], contentId, linkedContentId)
                    else:
                        self._insert_information_entry(value, information["specId"], contentId)
            else:
                self._insert_information_entry(information["value"], information["specId"], contentId)

        self.ensureEntryInTable(
            {
                "contentId": contentId,
                "userId": userId
            },
            "contentRuser"
        )

        return contentId

    def _insert_information_entry(self, value, specId, contentId, linkedContentId = None):
        """
            Does not commit the write operation
        """
        if linkedContentId is None:
            informationId = self.ensureEntryInTable(
                {
                    "value": value,
                    "specificationId": specId
                },
                "information",
                [],
                True
            )
        else:
            informationId = self.ensureEntryInTable(
                {
                    "linkedContentId": linkedContentId,
                    "specificationId": specId
                },
                "information",
                [],
                True
            )
        self.ensureEntryInTable(
            {
                "contentId": contentId,
                "informationId": informationId
            },
            "contentRinformation"
        )
        return

    def deleteContentEntry(self, contentId):
        '''
            Will only delete the entries with contentId in the tables:
                - contents
                - contentRinformation
                - contentRuser
        '''
        self.dbConnection.append_write_query(_delete_content_entry_command, [contentId])

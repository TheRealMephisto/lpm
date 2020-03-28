from dbUtils.dbConnector import dbConnector
from dbUtils.dbReader import dbReader
from datetime import datetime

class dbWriter:

    def __init__(self):
        self.dbConnection = dbConnector()
        self.procedureProtocol = dict()
        self.userId = None

    # https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dbConnection.close_connection()
        return

    def getCurrentSqlTimestamp(self):
        return str(datetime.utcnow())

    def insertDataIntoTable(self, tableName, valueDict): # ToDo: put this in module to be referred from other pieces of code efficiently
        command = "INSERT INTO `" + tableName + "` (`id` "
        valueString = "NULL"
        for key in valueDict:
            command += ", `" + str(key) + "`"
            valueString += ", '" + str(valueDict[key]) + "'"
        command += ") VALUES (" + valueString + ");"
        self.dbConnection.append_write_query(command)

    '''
        tableName is a string
        valueDict is a dictionary containing the column names as keys and the values as values.
        
        Check if the entry to be added already exists.
        If yes, simply return its id.
        If not, add it and a timestamp in editHistory and return its id.
    '''
    def ensureEntryInTable(self, valueDict, tableName, protocolDepthIdentifiers = []):
        with dbReader(self.dbConnection) as db_reader:
            entryId = db_reader.getIdOfDataInTable(tableName, valueDict)
            if entryId == -1:
                tableId = db_reader.getIdOfDataInTable('existingTables', {'tableName': tableName})
                self.insertDataIntoTable(tableName, valueDict)
                entryId = db_reader.getIdOfDataInTable(tableName, valueDict)
                if self.userId is None:
                    if tableName == 'users':
                        self.userId = entryId
                    else:
                        protocol_message = 'No valid userId provided!'
                self.insertDataIntoTable('editHistory', {'date': self.getCurrentSqlTimestamp(), 'userId':  self.userId, 'tableId': tableId, 'rowId': entryId, 'description': 'Added'})
                protocol_message = 'Successfully added entry: ' + str(valueDict)
            else:
                protocol_message = 'Entry existed already: ' + str(valueDict)
        
        self.procedureProtocol[tableName] = self.create_protocol_entry(protocol_message)
        
        return entryId

    def create_protocol_entry(self, message, depth_identifiers = []):
        if len(depth_identifiers) == 0:
            entry = message
        else:
            entry = dict()
            entry[depth_identifiers[0]] = self.create_protocol_entry(message, depth_identifiers[1:])
        return entry

    '''
        This is the function which is going to be used in later releases
    '''
    def addTexDocumentEntryJSON(self, formData):
        title = formData['title']
        path = formData['path']
        username = formData['author']
        filePathList = formData['files']

        informationArrayList = formData['informationArray']
        informationList=list()
        informationTypeList=list()
        for item in informationArrayList:
            informationList.append(item['information'])
            informationTypeList.append(item['type'])

        packageArrayList = formData['packages']
        packageList=list()
        packageOptionsList=list()
        for item in packageArrayList:
            packageList.append(item['package'])
            packageOptionsList.append(item['options'])
        
        return self.addTexDocumentEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList)


    def addTexDocumentEntry(self, title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):

        # ensure user in table and get id
        dataDictToAdd = {'username': username}
        self.userId = self.ensureEntryInTable(dataDictToAdd, 'users')

        # Add content
        dataDictToAdd = {'title' : title, 'path' : path}
        contentId = self.ensureEntryInTable(dataDictToAdd, 'contents')

        # Add information type and information if not already existing
        informationTypeIds = list()
        informationIds = list()
        creationDateProvided = False
        if len(informationTypeList) != len(informationList):
            self.procedureProtocol['informationType'] = 'Error! informationList and informationTypeList must be of same length!'
            self.procedureProtocol['information'] = 'Error! informationList and informationTypeList must be of same length!'
        for i in range(0, len(informationTypeList)):
            if informationTypeList[i] == 'creationDate':
                creationDateProvided = True
        if not creationDateProvided:
            dataDictToAdd= {'type' : 'creationDate'}
            entryId = self.ensureEntryInTable(dataDictToAdd, 'informationType')
            informationTypeIds.append(entryId)

            dataDictToAdd = {'information' : self.getCurrentSqlTimestamp(), 'informationTypeId' : entryId}
            entryId = self.ensureEntryInTable(dataDictToAdd, 'information')
            informationIds.append(entryId)
        for i in range(0 if creationDateProvided else 1, len(informationTypeList)):
            dataDictToAdd = {'type' : informationTypeList[i]}
            entryId = self.ensureEntryInTable(dataDictToAdd, 'informationType')
            informationTypeIds.append(entryId)

            dataDictToAdd = {'information' : informationList[i], 'informationTypeId' : entryId}
            entryId = self.ensureEntryInTable(dataDictToAdd, 'information')
            informationIds.append(entryId)

        # Add package and options combination if not already existing
        packageIds = list()
        packageOptionIds = list()
        if len(packageList) != len(packageOptionsList):
            self.procedureProtocol['packageOptions'] = 'Error! packageList and packageOptionsList must be of same length!'
            self.procedureProtocol['packages'] = 'Error! packageList and packageOptionsList must be of same length!'
        else:
            for i in range(0, len(packageList)):
                self.procedureProtocol['packageRoption'][str(i)] = dict()
                dataDictToAdd = {'package' : packageList[i]}
                entryId = self.ensureEntryInTable(dataDictToAdd, 'packages' [str(i)])
                packageIds.append(entryId)

                packageOptionIds.append(list())

                for j in range(0, len(packageOptionsList[i])):
                    dataDictToAdd = {'option' : packageOptionsList[i][j]}
                    entryId = self.ensureEntryInTable(dataDictToAdd, 'packageOptions', [str(i)])
                    packageOptionIds[i].append(entryId)

                    # Add relation from package to package option
                    dataDictToAdd = {'packageId' : packageIds[i], 'optionId' : insertionOutput['entryId']}
                    self.ensureEntryInTable(dataDictToAdd, 'packageRoption', [str(i), str(j)])

        # Add file paths if not already existing
        fileIds = list()
        for i in range(0, len(filePathList)):
            dataDictToAdd = {'path' : filePathList[i]}
            entryId = self.ensureEntryInTable(dataDictToAdd, 'files', ['files', str(i)])
            fileIds.append(entryId)

        # Add contentRuser, contentRfile, contentRinformation and contentRpackages entry
        dataDictToAdd = {'contentId' : contentId, 'userId' : self.userId}
        self.ensureEntryInTable(dataDictToAdd, 'contentRuser')

        for i in range(0, len(fileIds)):
            dataDictToAdd = {'contentId' : contentId, 'fileId' : fileIds[i]}
            self.ensureEntryInTable(dataDictToAdd, 'contentRfile', [str(i)])
        
        for i in range(0, len(informationIds)):
            dataDictToAdd = {'contentId' : contentId, 'informationId' : informationIds[i]}
            self.ensureEntryInTable(dataDictToAdd, 'contentRinformation', [str(i)])

        for i in range(0, len(packageIds)):
            dataDictToAdd = {'contentId' : contentId, 'packageId' : packageIds[i]}
            with dbReader() as db_reader:
                self.ensureEntryInTable(dataDictToAdd, 'contentRpackage', [str(i)])

        self.dbConnection.commit()

        return self.procedureProtocol

    # def removeEntry(self, Id):
    #     pass
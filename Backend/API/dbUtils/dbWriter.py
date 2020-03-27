from dbUtils.dbConnector import dbConnector
from dbUtils.dbReader import dbReader
from datetime import datetime

class dbWriter:

    def __init__(self):
        print("HELLO!")
        self.dbConnection = dbConnector()

    # https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dbConnection.close_connection()
        return

    def getCurrentSqlTimestamp(self):
        return str(datetime.utcnow())

    def insertDataIntoTable(self, tableName, valueDict): # ToDo: put this in module to be referred from other pieces of code efficiently
        print("Value Dict: ")
        print(valueDict)
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
    def ensureEntryInTable(self, tableName, valueDict, userId='1'):
        print("ensure value Dict:")
        print(valueDict)
        with dbReader(self.dbConnection) as db_reader:
            entryId = db_reader.getIdOfDataInTable(tableName, valueDict)
            if entryId == -1:
                tableId = db_reader.getIdOfDataInTable('existingTables', {'tableName': tableName})
                print("tableId: ")
                print(tableId)
                self.insertDataIntoTable(tableName, valueDict)
                entryId = db_reader.getIdOfDataInTable(tableName, valueDict)
                self.insertDataIntoTable('editHistory', {'date': self.getCurrentSqlTimestamp(), 'userId':  userId, 'tableId': tableId, 'rowId': entryId, 'description': 'Added'})
                protocolEntry = 'Successfully added entry: ' + str(valueDict)
            else:
                protocolEntry = 'Entry existed already: ' + str(valueDict)
        return {'entryId' : entryId, 'protocolEntry' : protocolEntry}

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
        
        procedureProtocol = dict()
        procedureProtocol['databaseTableStatuses'] = dict()

        # Add content
        dataDictToAdd = {'title' : title, 'path' : path}
        insertionOutput = self.ensureEntryInTable('contents', dataDictToAdd)
        contentId = insertionOutput['entryId']
        procedureProtocol['databaseTableStatuses']['contents'] = insertionOutput['protocolEntry']

        # Add user
        dataDictToAdd = {'username': username}
        insertionOutput = self.ensureEntryInTable('users', dataDictToAdd)
        userId = insertionOutput['entryId']
        procedureProtocol['databaseTableStatuses']['users'] = insertionOutput['protocolEntry']
        
        # Add information type and information if not already existing
        informationTypeIds = list()
        informationIds = list()
        creationDateProvided = False
        if len(informationTypeList) != len(informationList):
            print("Error! informationList and informationTypeList must be of same length!")
            procedureProtocol['databaseTableStatuses']['informationType'] = 'Error! informationList and informationTypeList must be of same length!'
            procedureProtocol['databaseTableStatuses']['information'] = 'Error! informationList and informationTypeList must be of same length!'
        else:
            procedureProtocol['databaseTableStatuses']['informationType'] = dict()
            procedureProtocol['databaseTableStatuses']['information'] = dict()
        for i in range(0, len(informationTypeList)):
            if informationTypeList[i] == 'creationDate':
                creationDateProvided = True
        if not creationDateProvided:
            dataDictToAdd= {'type' : 'creationDate'}
            insertionOutput = self.ensureEntryInTable('informationType', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['informationType']['0'] = insertionOutput['protocolEntry']
            informationTypeIds.append(insertionOutput['entryId'])

            dataDictToAdd = {'information' : self.getCurrentSqlTimestamp(), 'informationTypeId' : insertionOutput['entryId']}
            insertionOutput = self.ensureEntryInTable('information', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['information']['0'] = insertionOutput['protocolEntry']
            informationIds.append(insertionOutput['entryId'])
        for i in range(0 if creationDateProvided else 1, len(informationTypeList)):
            dataDictToAdd = {'type' : informationTypeList[i]}
            insertionOutput = self.ensureEntryInTable('informationType', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['informationType'][str(i)] = insertionOutput['protocolEntry']
            informationTypeIds.append(insertionOutput['entryId'])

            dataDictToAdd = {'information' : informationList[i], 'informationTypeId' : insertionOutput['entryId']}
            insertionOutput = self.ensureEntryInTable('information', dataDictToAdd)
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
            procedureProtocol['databaseTableStatuses']['packageRoption'] = dict()
            for i in range(0, len(packageList)):
                procedureProtocol['databaseTableStatuses']['packageRoption'][str(i)] = dict()
                dataDictToAdd = {'package' : packageList[i]}
                insertionOutput = self.ensureEntryInTable('packages', dataDictToAdd)
                procedureProtocol['databaseTableStatuses']['packages'][str(i)] = insertionOutput['protocolEntry']
                packageIds.append(insertionOutput['entryId'])

                procedureProtocol['databaseTableStatuses']['packageOptions'][str(i)] = dict()
                packageOptionIds.append(list())

                for j in range(0, len(packageOptionsList[i])):
                    dataDictToAdd = {'option' : packageOptionsList[i][j]}
                    insertionOutput = self.ensureEntryInTable('packageOptions', dataDictToAdd)
                    procedureProtocol['databaseTableStatuses']['packageOptions'][str(i)] = insertionOutput['protocolEntry']
                    packageOptionIds[i].append(insertionOutput['entryId'])

                    # Add relation from package to package option
                    dataDictToAdd = {'packageId' : packageIds[i], 'optionId' : insertionOutput['entryId']}
                    insertionOutput = self.ensureEntryInTable('packageRoption', dataDictToAdd)
                    procedureProtocol['databaseTableStatuses']['packageRoption'][str(i)][str(j)] = insertionOutput['protocolEntry']

        # Add file paths if not already existing
        fileIds = list()
        procedureProtocol['databaseTableStatuses']['files'] = dict()
        for i in range(0, len(filePathList)):
            dataDictToAdd = {'path' : filePathList[i]}
            insertionOutput = self.ensureEntryInTable('files', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['files'][str(i)] = insertionOutput['protocolEntry']
            fileIds.append(insertionOutput['entryId'])

        # Add contentRuser, contentRfile, contentRinformation and contentRpackages entry
        procedureProtocol['databaseTableStatuses']['contentRuser'] = dict()
        dataDictToAdd = {'contentId' : contentId, 'userId' : userId}
        insertionOutput = self.ensureEntryInTable('contentRuser', dataDictToAdd)
        procedureProtocol['databaseTableStatuses']['contentRuser']['protocolEntry'] = insertionOutput['protocolEntry']

        procedureProtocol['databaseTableStatuses']['contentRfile'] = dict()
        for i in range(0, len(fileIds)):
            dataDictToAdd = {'contentId' : contentId, 'fileId' : fileIds[i]}
            insertionOutput = self.ensureEntryInTable('contentRfile', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRfile'][str(i)] = insertionOutput['protocolEntry']
        
        procedureProtocol['databaseTableStatuses']['contentRinformation'] = dict()
        for i in range(0, len(informationIds)):
            dataDictToAdd = {'contentId' : contentId, 'informationId' : informationIds[i]}
            insertionOutput = self.ensureEntryInTable('contentRinformation', dataDictToAdd)
            procedureProtocol['databaseTableStatuses']['contentRinformation'][str(i)] = insertionOutput['protocolEntry']

        procedureProtocol['databaseTableStatuses']['contentRpackage'] = dict()
        for i in range(0, len(packageIds)):
            dataDictToAdd = {'contentId' : contentId, 'packageId' : packageIds[i]}
            with dbReader() as db_reader:
                if db_reader.getIdOfDataInTable('contentRpackage', dataDictToAdd) == -1:
                    insertionOutput = self.ensureEntryInTable('contentRpackage', dataDictToAdd)
                    procedureProtocol['databaseTableStatuses']['contentRpackage'][str(i)] = insertionOutput['protocolEntry']
                else:
                    procedureProtocol['databaseTableStatuses']['contentRpackage'][str(i)] = insertionOutput['protocolEntry']

        self.dbConnection.commit()

        return procedureProtocol

    # def removeEntry(self, Id):
    #     pass
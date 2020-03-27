from dbUtils.dbConnector import dbConnector

class dbReader:

    def __init__(self, dbConnection = None):
        if dbConnection != None:
            print("I got a dbConnection sponsored, cool!")
            self.dbConnection = dbConnection
            self.connection_registered = False
        else:
            self.dbConnection = dbConnector()
            self.connection_registered = True

    # https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection_registered:
            self.dbConnection.close_connection()
        return

    '''
        tableName is a string
        valueDict is a dictionary containing the column names as keys and the values as values.
    '''
    def getIdOfDataInTable(self, tableName, valueDict):
        command = "SELECT * FROM `" + tableName + "`"
        initialCommandLength = len(command)
        for key in valueDict:
            command += " AND " if len(command) > initialCommandLength else " WHERE "
            command += "`" + key + "` = '" + str(valueDict[key]) + "'"
        command += ";"
        result = self.dbConnection.execute_read_query(command)
        if result != -1:
            return result[0][0]
        return -1

    '''
        MySQL command for retrieval of a specific entry given a value of a specific column in a given table
    '''
    def getRowsByValue(self, tableName, key, value):
        command = "SELECT * from `" + tableName + "` WHERE `" + key + "` = '" + str(value) + "'"
        return self.dbConnection.execute_read_query(command)

    def getFirstRowByValue(self, tableName, key, value):
        rows = self.getRowsByValue(tableName, key, value)
        return rows[0] if rows != -1 else -1

    def getRowsByValues(self, tableName, key, valueList):
        rows = list()
        for value in valueList:
            rows.extend(self.getRowsByValue(tableName, key, value))
        return rows

    '''
        Get rows inside a table using a where clause matching different values in different columns, specified by keyAndValueDict
    '''
    def getRowsByKeysAndValues(self, tableName, keyAndValueDict):
        command = "SELECT * from `" + tableName + "`"
        firstIteration = True
        for key, value in keyAndValueDict.items():
            if firstIteration:
                command += " WHERE "
                firstIteration = False
            else:
                command += " AND "
            command += "`" + key + "` = '" + str(value) + "'"
        return self.dbConnection.execute_read_query(command)

    def getFirstRowByKeysAndValues(self, tableName, keyAndValueDict):
        rows = self.getRowsByKeysAndValues(tableName, keyAndValueDict)
        return rows[0] if rows != -1 else -1

    def getAllRows(self, tableName):
        return self.getRowsByKeysAndValues(tableName, {})

    def getTableHeaders(self, tableName):
        command = "DESCRIBE " + tableName + ";"
        return self.dbConnection.execute_read_query(command)

    '''
        Retrive a list of values given a list of rows of a table and the specific column header
    '''
    def getValuesByKey(self, rows, header):
        pass

    '''
        Get all available information types
    '''
    def getInformationTypes(self):

        informationTypes = list()

        rows = self.getAllRows('informationType')
        if rows != -1:
            for row in rows:
                informationTypes.append(row[1])

        return informationTypes

    '''
        Return an entry if existing, -1 else.
        contentId: number
    '''
    def getTexDocumentEntry(self, contentId):

        texDocumentEntry = dict()
        texDocumentEntry['contentId'] = contentId

        rows = self.getRowsByValue('contents', 'id', contentId)
        if rows == -1:
            return -1
        row = rows[0]
        texDocumentEntry['title'] = row[1]
        texDocumentEntry['path'] = row[2]

        # todo: get the user who created the content entry via editHistory table
        index = self.getRowsByValue('contentRuser', 'contentId', contentId)
        if index == -1:
            return -2 # entry exists, but mandatory value is missing!
        texDocumentEntry['username'] = self.getFirstRowByValue('users', 'id', index[0][2])[1]

        indices = list()
        rows = self.getRowsByValue('contentRfile', 'contentId', contentId)
        if rows != -1:
            for row in rows:
                indices.append(row[2])
            texDocumentEntry['filePaths'] = dict()
            for i in range(0, len(indices)):
                texDocumentEntry['filePaths'][str(i)] = self.getFirstRowByValue('files', 'id', indices[i])[1]

        # get information
        texDocumentEntry['information'] = dict()
        informationCount = 0
        indices = list()
        rows = self.getRowsByValue('contentRinformation', 'contentId', contentId)
        if rows != -1:
            for row in rows:
                indices.append(row[2])
            rows = self.getRowsByValues('information', 'id', indices)
            informationCount = len(rows)
            for i in range(0, informationCount):
                texDocumentEntry['information'][str(i)] = dict()
                texDocumentEntry['information'][str(i)]['information'] = rows[i][1]
                texDocumentEntry['information'][str(i)]['type'] = self.getFirstRowByValue('informationType', 'id', rows[i][2])[1]
        texDocumentEntry['informationCount'] = informationCount

        # get packages
        texDocumentEntry['packages'] = dict()
        packagesCount = 0
        indices = list() # indices will hold the indices of packages belonging to the content
        rows = self.getRowsByValue('contentRpackage', 'contentId', contentId)
        if rows != -1:
            for row in rows:
                indices.append(row[2])
            rows = self.getRowsByValues('packages', 'id', indices)
            packagesCount = len(rows)
            for i in range(0, packagesCount):
                texDocumentEntry['packages'][str(i)] = dict()
                texDocumentEntry['packages'][str(i)]['package'] = rows[i][1]
                relationRows = self.getRowsByValue('packageRoption', 'packageId', rows[i][0])
                texDocumentEntry['packages'][str(i)]['options'] = dict()
                optionsCount = len(relationRows)
                texDocumentEntry['packages'][str(i)]['optionsCount'] = optionsCount
                for j in range(0, optionsCount):
                    texDocumentEntry['packages'][str(i)]['options'][str(j)] = self.getFirstRowByValue('packageOptions', 'id', relationRows[j][2])[1]
        texDocumentEntry['packagesCount'] = packagesCount

        # Get creation date
        foundCreationDate = False # flag to ensure a value for creation date!
        row = self.getFirstRowByValue('informationType', 'type', 'creationDate')
        if row != -1:
            creationDateInformationTypeId = row[0]
            anotherRow = self.getFirstRowByValue('contentRinformation', 'contentId', contentId)
            if anotherRow != -1:
                informationId = anotherRow[2]
                keyAndValueDict = {
                    'id': informationId,
                    'informationTypeId': creationDateInformationTypeId
                }
                yetAnotherRow = self.getFirstRowByKeysAndValues('information', keyAndValueDict)
                if yetAnotherRow != -1:
                    texDocumentEntry['creationDate'] = yetAnotherRow[1]
                    foundCreationDate = True
        if not foundCreationDate:
            contentTableId = self.getFirstRowByValue('existingTables', 'tableName', 'contents')[0]
            texDocumentEntry['creationDate'] = self.getFirstRowByValue('editHistory', 'tableId', contentTableId)[1]

        # Get keywords
        # row = getRowsByValue('contentRinformation', 'contentId', contentId)
        # if row != -1:
        #     informationIds = []
            # todo

        row = self.getFirstRowByValue('informationType', 'type', 'keyword')
        if row != -1:
            keywordInformationTypeId = row[0]
            anotherRow = self.getFirstRowByValue('contentRinformation', 'contentId', 'contentId')
            if anotherRow != -1:
                informationId = anotherRow[2]
                keyAndValueDict = {
                    'id': informationId,
                    'informationTypeId': keywordInformationTypeId
                }
                yetAnotherRow = self.getFirstRowByKeysAndValues('information', keyAndValueDict)
                if yetAnotherRow != -1:
                    texDocumentEntry['key']

        self.dbConnection.commit()

        return texDocumentEntry

    '''
        Return JSON-object containing the information of a TexDocument.
        Indicator is the contents table,
        extract the rows (and the corresponding data of the other tables)
        beginning from index startAt up to maxResults.
        startAt: number
        maxResults: number
    '''
    def getTexDocumentEntries(self, startAt, maxResults):
        texDocumentEntries = dict()
        totalResultCount = 0
        for i in range(startAt, startAt + maxResults):
            candidate = self.getTexDocumentEntry(i)
            if candidate != -1 and candidate != -2: # there exist several error codes! -1, -2
                texDocumentEntries[str(i)] = candidate
                totalResultCount += 1
            else:
                break
        texDocumentEntries['totalResultCount'] = totalResultCount
        return texDocumentEntries
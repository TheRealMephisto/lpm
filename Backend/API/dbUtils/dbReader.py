from dbUtils.dbConnector import dbConnector

class dbReader:

    def __init__(self, dbConnection = None):
        if dbConnection != None:
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
        rawRows = self.dbConnection.execute_read_query(command)
        if type(rawRows) != list:
            return -1

        headers = self.getTableHeaders(tableName)
        if type(headers) != list:
            return -1
            
        rows = list()

        for index_raw in range(0, len(rawRows)):
            row = dict()
            for index_header in range(0, len(headers)):
                row[headers[index_header]] = rawRows[index_raw][index_header]
            rows.append(row)
        return rows

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
        result = self.dbConnection.execute_read_query(command)
        if type(result) == list:
            headers = list()
            for i in range(0, len(result)):
                headers.append(result[i][0])
            return headers
        return -1

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

        row = self.getFirstRowByValue('contents', 'id', contentId)
        if type(row) != dict:
            return -1
        texDocumentEntry['title'] = row['title']
        texDocumentEntry['path'] = row['path']

        # todo: get the user who created the content entry via editHistory table # proceeded here, check if finished!
        userRow = self.getFirstRowByValue('contentRuser', 'contentId', contentId)
        if type(userRow) != dict:
            return -2 # entry exists, but mandatory value is missing!

        userInfoRow = self.getFirstRowByValue('users', 'id', userRow['userId'])
        if type(userInfoRow) != dict:
            return -1
        texDocumentEntry['username'] = userInfoRow['username']

        # todo: comment this
        indices = list()
        rows = self.getRowsByValue('contentRfile', 'contentId', contentId)
        if type(rows) == list:
            for row in rows:
                indices.append(row['fileId'])
            texDocumentEntry['filePaths'] = dict()
            for i in range(0, len(indices)):
                fileRow = self.getFirstRowByValue('files', 'id', indices[i])
                if type(fileRow) == list:
                    texDocumentEntry['filePaths'][str(i)] = fileRow['path']

        # get information
        texDocumentEntry['information'] = dict()
        informationCount = 0
        indices = list()
        rows = self.getRowsByValue('contentRinformation', 'contentId', contentId)
        if type(rows) == list:
            for row in rows:
                indices.append(row['informationId'])
            informationRows = self.getRowsByValues('information', 'id', indices)
            if type(informationRows) == list:
                informationCount = len(informationRows)
                for i in range(0, informationCount):
                    texDocumentEntry['information'][str(i)] = dict()
                    texDocumentEntry['information'][str(i)]['information'] = informationRows[i]['information']
                    informationTypeRow = self.getFirstRowByValue('informationType', 'id', informationRows[i]['informationTypeId'])
                    if type(informationTypeRow) == list:
                        texDocumentEntry['information'][str(i)]['type'] = informationTypeRow['informationType']
        texDocumentEntry['informationCount'] = informationCount

        # get packages
        texDocumentEntry['packages'] = dict()
        packagesCount = 0
        indices = list() # indices will hold the indices of packages belonging to the content
        rows = self.getRowsByValue('contentRpackage', 'contentId', contentId)
        if type(rows) == list:
            for row in rows:
                indices.append(row['packageId'])
            packageRows = self.getRowsByValues('packages', 'id', indices)
            if type(packageRows) == list:
                packagesCount = len(packageRows)
                for i in range(0, packagesCount):
                    texDocumentEntry['packages'][str(i)] = dict()
                    texDocumentEntry['packages'][str(i)]['package'] = packageRows[i]['package']
                    relationRows = self.getRowsByValue('packageRoption', 'packageId', packageRows[i]['id'])
                    if type(relationRows) == list:
                        texDocumentEntry['packages'][str(i)]['options'] = dict()
                        optionsCount = len(relationRows)
                        texDocumentEntry['packages'][str(i)]['optionsCount'] = optionsCount
                        for j in range(0, optionsCount):
                            packageOptionRow = self.getFirstRowByValue('packageOptions', 'id', relationRows[j]['optionId'])
                            if type(packageOptionRow) == list:
                                texDocumentEntry['packages'][str(i)]['options'][str(j)] = packageOptionRow['option']
        texDocumentEntry['packagesCount'] = packagesCount

        # Get creation date
        foundCreationDate = False # flag to ensure a value for creation date!
        row = self.getFirstRowByValue('informationType', 'type', 'creationDate')
        if type(row) == dict:
            anotherRow = self.getFirstRowByValue('contentRinformation', 'contentId', contentId)
            if type(anotherRow) == dict():
                keyAndValueDict = {
                    'id': anotherRow['informationId'],
                    'informationTypeId': row['id']
                }
                yetAnotherRow = self.getFirstRowByKeysAndValues('information', keyAndValueDict)
                if type(yetAnotherRow) == dict:
                    texDocumentEntry['creationDate'] = yetAnotherRow['information']
                    foundCreationDate = True
        if not foundCreationDate:
            existingTableRow = self.getFirstRowByValue('existingTables', 'tableName', 'contents')
            if type(existingTableRow) == dict:
                editHistoryRow = self.getFirstRowByValue('editHistory', 'tableId', existingTableRow['id'])
                if type(editHistoryRow) == dict:
                    texDocumentEntry['creationDate'] = editHistoryRow['date']

        # Get keywords
        # row = getRowsByValue('contentRinformation', 'contentId', contentId)
        # if row != -1:
        #     informationIds = []
            # todo

        # row = self.getFirstRowByValue('informationType', 'type', 'keyword')
        # if type(row) == dict:
        #     keywordInformationTypeId = row['id']
        #     anotherRow = self.getFirstRowByValue('contentRinformation', 'contentId', contentId)
        #     if type(anotherRow) == dict:
        #         informationId = anotherRow[2]
        #         keyAndValueDict = {
        #             'id': informationId,
        #             'informationTypeId': keywordInformationTypeId
        #         }
        #         yetAnotherRow = self.getFirstRowByKeysAndValues('information', keyAndValueDict)
        #         if yetAnotherRow != -1:
        #             texDocumentEntry['key']

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
                texDocumentEntries[str(i)] = candidate # debugging purposes!
                # break
        texDocumentEntries['totalResultCount'] = totalResultCount
        return texDocumentEntries
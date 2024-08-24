import dbUtils
from dbUtils.dbConnector import dbConnector
import json

class dbReader:

    def __init__(self, dbConnection = None):
        if dbConnection != None:
            self.dbConnection = dbConnection
            self.connection_registered = False
        else:
            self.dbConnection = dbConnector()
            self.connection_registered = True

    # ToDo: check on the following comment, document it somewhere if needed, remove afterwards
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
        result = self.getDbEntryIfPresent(tableName, valueDict)
        if result != -1:
            return result['id']
        return -1

    def getMatchingDbEntryIfPresent(self, tableName, valueDict):
        '''
            Check a table with given tableName for the existence of a row,
            matching the given key-value-pairs in the valueDict.
            Return the first matched entry if existing,
            return -1 if not existing
        '''
        return self.getDbEntryIfPresent(tableName, valueDict, True)
    
    def getDbEntryIfPresent(self, tableName, valueDict, matchMode = False):
        '''
            Check a table with given tableName for the existence of a row,
            matching the given key-value-pairs in the valueDict.
            If matchMode is False, the valueDict should contain exact information about
            all headers in the table as well as the corresponding values.
            If matchMode is True, a subset of the headers can be specified.
        '''
        command = "SELECT * FROM `{t}`".format(t=tableName)
        initialCommandLength = len(command)
        argsList = list()
        for key in valueDict:
            command += " AND " if len(command) > initialCommandLength else " WHERE "
            command += "{k} = %s".format(k=key)
            argsList.append(valueDict[key])
        command += ";"
        result = self.dbConnection.execute_read_query(command, argsList)
        if result != -1:
            headers = self.getTableHeaders(tableName)
            if not matchMode and self._match_specifier_count(headers) != len(valueDict.keys()):
                raise Exception("getDbEntryIfPresent with matchMode=False needs values for all columns in the table.")
            entry = dict()
            for i in range(0, len(headers)):
                entry[headers[i]] = result[0][i]
            return entry
        return -1

    def _match_specifier_count(self, headers):
        return len(headers) - 1

    def getRowsByValue(self, tableName, key, value):
        '''
            MySQL command for retrieval of a specific entry given a value of a specific column in a given table
        '''
        command = "SELECT * from `{t}` WHERE {k} = %s".format(t=tableName, k=key)
        tmpRows = self.rawRowsToRows(tableName, self.dbConnection.execute_read_query(command, [value]))
        rows = list()
        if tmpRows != -1:
            for row in tmpRows:
                if tableName == 'existingTables' or row['markedForRemoval'] == 0:
                    rows.append(row)
        return rows if len(rows) > 0 else -1

    def getFirstRowByValue(self, tableName, key, value):
        rows = self.getRowsByValue(tableName, key, value)
        return rows[0] if rows != -1 else -1

    def getRowsByValues(self, tableName, key, valueList):
        rows = list()
        for value in valueList:
            moreRows = self.getRowsByValue(tableName, key, value)
            if type(moreRows) is list:
                for row in moreRows:
                    if not row in rows:
                        rows.append(row)
        return rows

    def rawRowsToRows(self, tableName, rawRows):
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

    '''
        Get rows inside a table using a where clause matching different values in different columns, specified by keyAndValueDict
    '''
    def getRowsByKeysAndValues(self, tableName, keyAndValueDict):
        command = "SELECT * from `{t}`".format(t=tableName)
        firstIteration = True
        argsList = list()
        for key, value in keyAndValueDict.items():
            if firstIteration:
                command += " WHERE "
                firstIteration = False
            else:
                command += " AND "
            command += "{k} = %s".format(k=key)
            argsList.append(str(value))
        return self.rawRowsToRows(tableName, self.dbConnection.execute_read_query(command, argsList))

    def getFirstRowByKeysAndValues(self, tableName, keyAndValueDict):
        rows = self.getRowsByKeysAndValues(tableName, keyAndValueDict)
        return rows[0] if rows != -1 else -1

    def getAllRows(self, tableName):
        return self.getRowsByKeysAndValues(tableName, {})

    '''
        Return all information rows connected to the given contentId
    '''
    def getInformationRows(self, contentId, verbosity = 0):
        informationRelationRows = self.getRowsByValue('contentRinformation', 'contentId', contentId)
        if type(informationRelationRows) is not list:
            return -1

        informationIds = list()
        for i in range(0, len(informationRelationRows)):
            if informationRelationRows[i]['informationId'] not in informationIds:
                informationIds.append(informationRelationRows[i]['informationId'])
        
        informationRows = self.getRowsByValues('information', 'id', informationIds)
        if type(informationRows) is not list:
            return -1
        if verbosity == 0:
            return [informationRows]
        if verbosity == 1:
            return [informationRows, informationRelationRows]

    def getTableHeaders(self, tableName):
        command = "DESCRIBE {t};".format(t=tableName)
        result = self.dbConnection.execute_read_query(command)
        if type(result) == list:
            headers = list()
            for i in range(0, len(result)):
                headers.append(result[i][0])
            return headers
        return -1

    def getInformationTypeMap(self, className = 'TexDocument'):
        informationTypeMap = dict()

        rows = self.getRowsByKeysAndValues('specifications', {'className': className})
        if type(rows) != list:
            return -1
        for row in rows:
            informationTypeMap[row['id']] = dict()
            informationTypeMap[row['id']]['label'] = row['label']
            informationTypeMap[row['id']]['dataType'] = self.getSpecification(row['dataType'])

        return informationTypeMap

    def getSpecification(self, className):
        
        if className in dbUtils._basic_data_types:
            return className
        
        specification = dict()
        specification['specifications'] = dict()
        if '[]' == className[-2:]:
            specification['as_list'] = True
            specification['dataType'] = className[:-2]
        else:
            specification['as_list'] = False
            specification['dataType'] = className

        rows = self.getRowsByKeysAndValues('specifications', {'className': specification['dataType']})
        if type(rows) != list:
            return -1
        for row in rows:
            row_id = str(row['id'])
            specification['specifications'][row_id] = dict()
            specification['specifications'][row_id]['label'] = row['label']
            specification['specifications'][row_id]['dataType'] = self.getSpecification(row['dataType'])
            specification['specifications'][row_id]['mandatory'] = row['mandatory']
            specification["specifications"][row_id]["array"] = row["array"]
        return specification

    def get_filtered_tex_document_ids(self, filterValue):
        results = self.dbConnection.execute_read_query(dbUtils._get_filtered_content_ids_of_tex_documents_command, [filterValue])
        contentIDs = list()
        if results != -1:
            for result in results:
                contentIDs.append(result[0])
        return contentIDs

    def getTexDocumentEntries(self, startAt, maxResults, verbosity = 0, filterValue = ""):
        '''
            Return an entry if existing and not marked for removal, -1 else.
            contentId: number
            verbosity: 0 - standard value, do not return info about relation tables 1 - do return this info
        '''
        json_result = dict()
        results = list()
        
        if len(filterValue) > 0:
            filterValue = "%" + filterValue + "%"
            contentIDs = self.get_filtered_tex_document_ids(filterValue)
            json_result["totalTableContentCount"] = len(contentIDs)
            if json_result["totalTableContentCount"] > 0:
                if json_result["totalTableContentCount"] > maxResults:
                    contentIDs = contentIDs[startAt-1:startAt-1+maxResults]
                
                get_filtered_tex_document_data_command = dbUtils._get_filtered_tex_document_data_command
                for index in range(0, len(contentIDs)-1):
                    get_filtered_tex_document_data_command += ", %s"
                get_filtered_tex_document_data_command += ");"

                results = self.dbConnection.execute_read_query(get_filtered_tex_document_data_command, contentIDs)
        else:
            json_result["totalTableContentCount"] = self.getTotalTableContentCount("contents", True)
        
            results = self.dbConnection.execute_read_query(dbUtils._get_basic_tex_document_data_command, [startAt-1, startAt-1 + maxResults])
        
        counter = 0

        if type(results) != list:
            raise Exception("Problem while retrieving results!")
        else:
            for result in results:
                counter += 1
                json_result[str(counter)] = json.loads(result[0])
                json_result[str(counter)]["packages"] = dict()
                json_result[str(counter)]["packagesCount"] = 0
                if verbosity == 1:
                    header_information = ["contentRinformation", "contentRfile", "contentRpackage", "contentRuser"]
                    for i in range(0, len(header_information)):
                        json_result[str(counter)][header_information[i]] = list()
                if verbosity == 0:
                    information_results = self.dbConnection.execute_read_query(dbUtils._get_available_tex_document_information_command, [json_result[str(counter)]["contentId"]])
                else:
                    information_results = self.dbConnection.execute_read_query(dbUtils._get_available_tex_document_information_verbose_command, [json_result[str(counter)]["contentId"]])
                json_result[str(counter)]["available_information"] = dict()
                json_result[str(counter)]["mandatory_information"] = list()


                for information_result in information_results:
                    json_information_result = json.loads(information_result[0])

                    if json_information_result["IsMandatory"]:
                        json_result[str(counter)]["mandatory_information"].append(json_information_result["InformationType"])
                    
                    json_result[str(counter)]["available_information"][json_information_result["InformationType"]] = {
                        "Value": json_information_result["InformationContent"],
                        "DataType": json_information_result["DataType"],
                        "Id": json_information_result["Id"],
                        "mandatory": json_information_result["IsMandatory"] == 1,
                        "array": json_information_result["IsArray"] == 1
                    }

                    if "[]" in json_information_result["DataType"]:
                        json_result[str(counter)]["available_information"][json_information_result["InformationType"]]["Value"] = list()
                        if "Keywords" in json_information_result["DataType"]:
                            keywords = json_information_result["InformationContent"].split(",")
                            for keyword in keywords:
                                json_result[str(counter)]["available_information"][json_information_result["InformationType"]].append(keyword)        
                    
                    if verbosity == 1:
                        header_information = ["contentRinformation", "contentRfile", "contentRpackages", "contentRuser"]
                        for i in range(1, len(information_result)):
                            json_result[str(counter)][header_information[i-1]].append(json.loads(information_result[i]))
        json_result["totalResultCount"] = counter
        return json_result

    def getTexDocumentEntry_deprecated(self, contentId, verbosity = 0, filterValue = ""):
        '''
            DEPRECATED - still work in progress to fully replace, still used in editTexDocument functionality of dbWriter
            Return an entry if existing and not marked for removal, -1 else.
            contentId: number
            verbosity: 0 - standard value, do not return info about relation tables 1 - do return this info
        '''

        texDocumentEntry = dict()
        texDocumentEntry['contentId'] = contentId

        if verbosity == 1:
            texDocumentEntry['contentRfile'] = list()
            texDocumentEntry['contentRinformation'] = list()
            texDocumentEntry['contentRpackage'] = list()
            texDocumentEntry['contentRuser'] = list()
            texDocumentEntry['packageRoption'] = list()

        row = self.getFirstRowByValue('contents', 'id', contentId)
        if type(row) != dict:
            return -1
        if not filterValue in row['title']:
            return -1
        texDocumentEntry['title'] = row['title']
        mainFileRefId = row['mainFileRefId']
        pathrow = self.getFirstRowByValue('files', 'id', row['mainFileRefId'])
        if type(pathrow) != dict:
            return -1
        texDocumentEntry['Dateipfad'] = pathrow['path']

        # ToDo: get the user who created the content entry via editHistory table # proceeded here, check if finished!
        userRow = self.getFirstRowByValue('contentRuser', 'contentId', contentId)
        if type(userRow) != dict:
            return -2 # entry exists, but mandatory value is missing!
        if verbosity == 1:
            texDocumentEntry['contentRuser'] = [userRow]

        userInfoRow = self.getFirstRowByValue('users', 'id', userRow['userId'])
        if type(userInfoRow) != dict:
            return -1
        texDocumentEntry['username'] = userInfoRow['username']

        indices = list()
        rows = self.getRowsByValue('contentRfile', 'contentId', contentId)
        if type(rows) == list:
            if verbosity == 1:
                texDocumentEntry['contentRfile'] = rows
            for row in rows:
                indices.append(row['fileId'])
            texDocumentEntry['filePaths'] = dict()
            for i in range(0, len(indices)):
                fileRow = self.getFirstRowByValue('files', 'id', indices[i])
                if type(fileRow) == list:
                    texDocumentEntry['filePaths'][str(i)] = fileRow['path']

        # get information
        # get all information entries with one request, sort them afterwards
        tempResult = self.getInformationRows(contentId, verbosity)
        informationRows = tempResult[0]
        if verbosity == 1:
            informationRelationRows = tempResult[1]
            if type(informationRelationRows) == list:
                texDocumentEntry['contentRinformation'] = informationRelationRows

        typeMap = self.getInformationTypeMap()
        

        availableInformation = dict()
        if type(informationRows) is list:
            typeIds = list()
            n = 0
            for i in range(0, len(informationRows)): # ToDo: increase efficiency!
                typeIdentifier = typeMap[informationRows[i]['informationTypeId']]['name']
                if typeIdentifier not in availableInformation.keys():
                    availableInformation[typeIdentifier] = dict()
                # ToDo: split informationRows into subsets regarding their types, iterate over those subsets!
                k = len(availableInformation[typeIdentifier].keys())
                availableInformation[typeIdentifier][str(k)] = informationRows[i]['information']
                availableInformation[typeIdentifier + 'Count'] = str(k+1)
            
        # Get creation date
        if 'Datum der Erstellung' in availableInformation.keys():
            if len(availableInformation['Datum der Erstellung'].keys()) == 1:
                availableInformation['Datum der Erstellung'] = availableInformation['Datum der Erstellung'] # should be only one value, not another dict!
            else:
                availableInformation['Datum der Erstellung'] = "DB Inconsistency: Error! Exactly one creation date should refer to that entry"
        else: 
            existingTableRow = self.getFirstRowByValue('existingTables', 'tableName', 'contents')
            if type(existingTableRow) == dict:
                editHistoryRow = self.getFirstRowByValue('editHistory', 'tableId', existingTableRow['id'])
                if type(editHistoryRow) == dict:
                    availableInformation['Datum der Erstellung'] = editHistoryRow['date']

        # merge dicts
        # texDocumentEntry = {**texDocumentEntry, **availableInformation}
        texDocumentEntry['available_information'] = availableInformation
        
        # get packages
        texDocumentEntry['packages'] = dict()
        packagesCount = 0
        indices = list() # indices will hold the indices of packages belonging to the content
        rows = self.getRowsByValue('contentRpackage', 'contentId', contentId)
        if type(rows) == list:
            if verbosity == 1:
                texDocumentEntry['contentRpackage'] = rows
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
                        if verbosity == 1:
                            texDocumentEntry['packageRoption'] = relationRows
                        texDocumentEntry['packages'][str(i)]['options'] = dict()
                        optionsCount = len(relationRows)
                        texDocumentEntry['packages'][str(i)]['optionsCount'] = optionsCount
                        for j in range(0, optionsCount):
                            packageOptionRow = self.getFirstRowByValue('packageOptions', 'id', relationRows[j]['optionId'])
                            if type(packageOptionRow) == dict:
                                texDocumentEntry['packages'][str(i)]['options'][str(j)] = packageOptionRow['option']
        texDocumentEntry['packagesCount'] = packagesCount

        self.dbConnection.commit()

        return texDocumentEntry

    def getTotalTableContentCount(self, tableName, includeMarkedForRemoval = False):
        if includeMarkedForRemoval:
            results = self.dbConnection.execute_read_query('SELECT COUNT(*) FROM `{t}`;'.format(t=tableName))
        else:
            results = self.dbConnection.execute_read_query('SELECT COUNT(*) FROM `{t}` WHERE `markedForRemoval` = "0";'.format(t=tableName))
        if type(results) == list:
            return results[0][0]
        return -1

    def getTotalTableContentCount_deprecated(self, tableName, includeMarkedForRemoval = False, filterValue = ""):
        '''
            to be deprecated, still used in editTexDocument functionality of dbWriter
        '''
        if not filterValue:
            if includeMarkedForRemoval:
                command = 'SELECT COUNT(*) FROM `{t}`;'.format(t=tableName)
            else:
                command = 'SELECT COUNT(*) FROM `{t}` WHERE `markedForRemoval` = "0";'.format(t=tableName)
            result = self.dbConnection.execute_read_query(command)
        else:
            if includeMarkedForRemoval:
                command = 'SELECT COUNT(*) FROM `{t}` WHERE `title` LIKE %s;'.format(t=tableName)
            else:
                command = 'SELECT COUNT(*) FROM `{t}` WHERE `markedForRemoval` = "0" AND WHERE `title` LIKE %s;'.format(t=tableName)
            result = self.dbConnection.execute_read_query(command, [filterValue])
        if type(result) == list:
            return result[0][0]
        return -1

    def getTableOffset(self, tableName, index):
        '''
            to be deprecated, still used in editTexDocument functionality of dbWriter
            Get the number of entries with markedForRemoval flag set before the specified index
        '''
        command = 'SELECT COUNT(*) FROM `{t}` WHERE `markedForRemoval` = "1" AND `id` <= {i};'.format(t=tableName, i=index)
        result = self.dbConnection.execute_read_query(command)
        if type(result) == list:
            return result[0][0]
        return -1

    def texDocumentsList(self, startAt = 1, filterValue = ""):
        '''
            to be deprecated, still used in editTexDocument functionality of dbWriter
        '''
        for i in range(startAt, self.getTotalTableContentCount_deprecated('contents', True)):
            # ToDo: the following filters only the title. This is to be replaced by more advanced filtering
            entry = self.getTexDocumentEntry_deprecated(i, 0, filterValue)
            if entry != -1 and entry != -2:
                yield entry

    # ToDo: remove this and replace it's usage
    def getTexDocumentEntries_deprecated(self, startAt, maxResults, filterValue = ""):
        '''
            to be deprecated, still used in editTexDocument functionality of dbWriter
            Return JSON-object containing the information of a TexDocument.
            Indicator is the contents table,
            extract the rows (and the corresponding data of the other tables)
            beginning from index startAt up to maxResults.
            startAt: number
            maxResults: number
        '''
        texDocumentEntries = dict()
        totalResultCount = 0
        totalTableContentCount = self.getTotalTableContentCount_deprecated('contents', False, filterValue)

        for entry in self.texDocumentsList(startAt, filterValue):
            if totalResultCount < maxResults:
                texDocumentEntries[str(totalResultCount+1)] = entry
                totalResultCount += 1
            else:
                break
        
        texDocumentEntries['totalResultCount'] = totalResultCount
        texDocumentEntries['totalTableContentCount'] = totalTableContentCount
        return texDocumentEntries

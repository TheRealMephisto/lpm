from flask import Flask, request

import sys
pathToLibraries = '/etc/lpm/libraries/'
sys.path.append(pathToLibraries)

from GeneralUtils import utility as util
from dbUtils import dbReader
from dbUtils import dbWriter

app = Flask(__name__)

@app.route("/")
def indexRoot():
    return ("Hello World!")

@app.route("/api")
def index():
    return ("Hello World!")

@app.route("/api/getInformationTypeMap", methods=['POST', 'GET'])
def getInformationTypeMap():
    if request.method == 'POST':
        pass
    else:
        with dbReader.dbReader() as db_reader:
            informationTypeMap = db_reader.getInformationTypeMap()
            totalResultCount = len(informationTypeMap.keys())
        return {
            'entries': informationTypeMap,
            'totalResultCount': totalResultCount
        }

@app.route("/api/getTexDocumentEntries_deprecated", methods=['POST', 'GET'])
def getTexDocumentEntries_deprecated():
    if request.method == 'POST':
        pass
    else:
        startAt = int(request.args.get('startAt'))
        maxResults = int(request.args.get('maxResults'))
        filterValue = request.args.get('filterValue')
        if not type(filterValue) == str:
            filterValue = ""
        with dbReader.dbReader() as db_reader:
            entries = db_reader.getTexDocumentEntries_deprecated(startAt, maxResults, filterValue)
        return {'entries' : entries}

@app.route("/api/getTexDocumentEntries", methods=['POST', 'GET'])
def getTexDocumentEntries():
    if request.method == 'POST':
        pass
    else:
        startAt = int(request.args.get('startAt'))
        maxResults = int(request.args.get('maxResults'))
        filterValue = request.args.get('filterValue')
        if not type(filterValue) == str:
            filterValue = ""
        with dbReader.dbReader() as db_reader:
            entries = db_reader.getTexDocumentEntries(startAt, maxResults, 0, filterValue)
        return {'entries' : entries}

@app.route("/api/addContentObject", methods=['POST'])
def addContentObject():
    if request.method == 'POST':
        data = request.get_json()
        with dbWriter.dbWriter() as db_writer:
            procedureProtocol = db_writer.addContentEntry(util.formDataToContentEntry(data["formData"], data["type"], data["user"]))
    success = 1
    if type(procedureProtocol) != dict:
        success = -1
    return {'output': 'New content entry!', 'procedureProtocol': procedureProtocol, "success": success}

@app.route('/api/editContentObject', methods=['POST'])
def editContentObject():
    if request.method == 'POST':
        with dbWriter.dbWriter() as db_writer:
            data = request.get_json()
            procedureProtocol = db_writer.editContentEntry(util.formDataToContentEntry(data["formData"], data["type"], data["user"]), data["Id"])
            return {'output': 'Edited Entry!', 'procedureProtocol': procedureProtocol, "success": True}
        return {'output': 'Failed editing entry!', "success": False}
    return {"Output": "Method get not allowed!", "success": False}

    
@app.route('/api/getContentObjectSpecification', methods=['POST'])
def getContentObjectSpecifications():
    specs = []
    with dbReader.dbReader() as db_reader:
        req_json = request.get_json()
        if req_json is None:
            return {"ErrorMessage": "Necessary information is missing!"}
        content_object_type = req_json["content_object_type"]
        specs = db_reader.getSpecification(content_object_type)
        if specs != -1:
            return specs
    return {}


@app.route("/api/addTexDocumentEntry", methods=['POST', 'GET'])
def addTexDocumentEntry():
    if request.method == 'POST':
        with dbWriter.dbWriter() as db_writer:
            procedureProtocol = db_writer.addTexDocumentEntryJSON(request.get_json())
    else:
        entry = request.args.get('entry')

        title = str(request.args.get('title'))
        path = str(request.args.get('path'))
        author = str(request.args.get())
        username = str(request.args.get('username'))
        filePathListRaw = str(request.args.get('filePathList')) # ToDo: document or improve readability, old comment: Lists will be strings with , as separator
        informationListRaw = str(request.args.get('informationList'))
        informationTypeListRaw = str(request.args.get('informationTypeList'))
        packageListRaw = str(request.args.get('packageList'))
        packageOptionsListRaw = str(request.args.get('packageOptionsList'))
        
        filePathList = util.stringToList(filePathListRaw)
        informationList = util.stringToList(informationListRaw)
        informationTypeList = util.stringToList(informationTypeListRaw)
        packageList = util.stringToList(packageListRaw)
        packageOptionsList = list()
        tmpPackageOptionsList = util.stringToList(packageOptionsListRaw, ';')
        for packageOptionsRaw in tmpPackageOptionsList:
            packageOptionsList.append(util.stringToList(packageOptionsRaw))

        with dbWriter.dbWriter() as db_writer:
            procedureProtocol = db_writer.addTexDocumentEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList)
    return {'output': 'New Entry!', 'procedureProtocol': procedureProtocol}

@app.route('/api/editTexDocumentEntry', methods=['POST'])
def editTexDocumentEntry():
    with dbWriter.dbWriter() as db_writer:
        procedureProtocol = db_writer.editTexDocumentEntryJSON(request.get_json())
        return {'output': 'Edited Entry!', 'procedureProtocol': procedureProtocol}
    return {'output': 'Failed editing entry!'}

@app.route('/api/getTexDocumentSpecifications', methods=['GET', 'POST']) # ToDo: forbid GET method
def getTexDocumentSpecifications(): # ToDo: rename to getSpecifications and require className parameter
    specs = []
    with dbReader.dbReader() as db_reader:
        specs = db_reader.getInformationTypeMap('TexDocument')
        return specs
    return {}

if __name__ == '__main__':
    # ToDo: check if the following configuration can be used in a secure way, replace / improve otherwise
    app.run(host='0.0.0.0', port="1337", debug=True)

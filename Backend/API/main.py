from flask import Flask, request
from flask_cors import CORS
import dbUtils
import argumentHelper as argUtil

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) # intermediate, adjust for production! Just needed for development on local machine.

@app.route("/")
def index():
    return ("Hello World")

@app.route("/api/getInformationTypes", methods=['POST', 'GET'])
def getInformationTypes():
    if request.method == 'POST':
        pass
    else:
        informationTypes = dbUtils.getInformationTypes()
        totalResultCount = len(informationTypes)
        return {
            'entries': informationTypes,
            'totalResultCount': totalResultCount
        }

@app.route("/api/getTexDocumentEntries", methods=['POST', 'GET'])
def getTexDocumentEntries():
    if request.method == 'POST':
        pass
    else:
        startAt = int(request.args.get('startAt'))
        maxResults = int(request.args.get('maxResults'))
        entries = dbUtils.getTexDocumentEntries(startAt, maxResults)

        return {'sumOfArguments' : startAt + maxResults, 'entries' : entries}

@app.route("/api/addTexDocumentEntry", methods=['POST', 'GET'])
def addTexDocumentEntry():
    entry = ""
    if request.method == 'POST':
        print(request.get_json())
        procedureProtocol = dbUtils.addTexDocumentEntryJSON(request.get_json())
        return {'output': 'New Entry!', 'procedureProtocol': procedureProtocol}
    else:
        entry = request.args.get('entry')

        title = str(request.args.get('title'))
        path = str(request.args.get('path'))
        username = str(request.args.get('username'))
        filePathListRaw = str(request.args.get('filePathList')) # Lists will be strings with , as separator
        informationListRaw = str(request.args.get('informationList'))
        informationTypeListRaw = str(request.args.get('informationTypeList'))
        packageListRaw = str(request.args.get('packageList'))
        packageOptionsListRaw = str(request.args.get('packageOptionsList'))
        
        filePathList = argUtil.stringToList(filePathListRaw)
        informationList = argUtil.stringToList(informationListRaw)
        informationTypeList = argUtil.stringToList(informationTypeListRaw)
        packageList = argUtil.stringToList(packageListRaw)
        packageOptionsList = list()
        tmpPackageOptionsList = argUtil.stringToList(packageOptionsListRaw, ';')
        for packageOptionsRaw in tmpPackageOptionsList:
            packageOptionsList.append(argUtil.stringToList(packageOptionsRaw))


        procedureProtocol = dbUtils.addTexDocumentEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList)
    return {'output': 'New Entry!', 'procedureProtocol': procedureProtocol}

if __name__ == '__main__':
    app.run(port="1337", debug=True)
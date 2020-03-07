from flask import Flask, request
from flask_cors import CORS
import modifyDB as dbUtil
import argumentHelper as argUtil

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) # intermediate, adjust for production! Just needed for development on local machine.

@app.route("/")
def index():
    return ("Hello World")

@app.route("/api/getTexDocumentEntries", methods=['POST', 'GET'])
def getTexDocumentEntries():
    if request.method == 'POST':
        pass
    else:
        startAt = int(request.args.get('startAt'))
        maxResults = int(request.args.get('maxResults'))

        return {'sumOfArguments' : startAt + maxResults, 'entries' : dbUtil.getTexDocumentEntries(startAt, maxResults)}

@app.route("/api/addTexDocumentEntry", methods=['POST', 'GET'])
def addTexDocumentEntry():
    entry = ""
    if request.method == 'POST':
        entry = request.form['entry']
        print(entry)
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


        procedureProtocol = dbUtil.addTexDocumentEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList)
    return {'output': 'New Entry!', 'procedureProtocol': procedureProtocol}

if __name__ == '__main__':
    app.run(port="1337", debug=True)
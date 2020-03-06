from flask import Flask, request
from flask_cors import CORS
import modifyDB as dbUtil
import argumentHelper as argUtil

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) # intermediate, adjust for production! Just needed for development on local machine.

@app.route("/")
def index():
    return ("Hello World")

@app.route("/api/addEntry", methods=['POST', 'GET'])
def addEntry():
    entry = ""
    if request.method == 'POST':
        entry = request.form['entry']
        print(entry)
    else:
        entry = request.args.get('entry')

        title = request.args.get('title')
        path = request.args.get('path')
        username = request.args.get('username')
        filePathListRaw = request.args.get('filePathList') # Lists will be strings with , as separator
        informationListRaw = request.args.get('informationList')
        informationTypeListRaw = request.args.get('informationTypeList')
        packageListRaw = request.args.get('packageList')
        packageOptionsListRaw = request.args.get('packageOptionsList')
        
        filePathList = argUtil.stringToList(filePathListRaw)
        informationList = argUtil.stringToList(informationListRaw)
        informationTypeList = argUtil.stringToList(informationTypeListRaw)
        packageList = argUtil.stringToList(packageListRaw)
        packageOptionsList = list()
        tmpPackageOptionsList = argUtil.stringToList(packageOptionsListRaw, ';')
        for packageOptionsRaw in tmpPackageOptionsList:
            packageOptionsList.append(argUtil.stringToList(packageOptionsRaw))


        procedureProtocol = dbUtil.addEntry(title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList)
    return {'output': 'New Entry!', 'procedureProtocol': procedureProtocol}

if __name__ == '__main__':
    app.run(port="1337", debug=True)

'''
    Provide an interface for TeXDocuments,
    which can be used to check for missing information and also to directly write the TeXDocument into the database.
'''
class TeXDocument:

    # for the dev as information, from dbWriterclass ToDo: remove this before pushing to origin
    #def addTexDocumentEntry(self, title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):

    def __init__(self, title = "", filepath = "", author = "", filePathList = list(), informationList = list(), informationTypeList = list(), packageList = list(), packageOptionsList = list()):
        self.title = title
        self.filepath = filepath
        self.author = author
        self.filePathList = filePathList
        self.informationList = informationList
        self.informationTypeList = informationTypeList
        self.packageList = packageList
        self.packageOptionsList = packageOptionsList

        self.ensureMainFileinFilePathList()

        return

    def __del__(self): # If I don't do this, the old lists will (strangely) be kept and just be appended later on
        while len(self.filePathList) > 0:
            self.filePathList.pop()
        while len(self.informationList) > 0:
            self.informationList.pop()
        while len(self.informationTypeList) > 0:
            self.informationTypeList.pop()
        while len(self.packageList) > 0:
            self.packageList.pop()
        while len(self.packageOptionsList) > 0:
            self.packageOptionsList.pop()

    def ensureMainFileinFilePathList(self):
        if not self.filepath in self.filePathList:
            self.filePathList.append(self.filepath)
        pass

    def isWritableToDatabase(self):
        return True
        
    '''
        Try to write to database, checking if writable before.
        If writing fails, print information about that in a log file.
        If it succeeds, also print information inside a log file.
    '''    
    def writeToDatabase(self):
        if self.isWritableToDatabase():
            pass
        pass
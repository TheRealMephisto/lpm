
'''
    Provide an interface for TeXDocuments,
    which can be used to check for missing information and also to directly write the TeXDocument into the database.
'''
class TeXDocument:

    # for the dev as information, from dbWriterclass ToDo: remove this before pushing to origin
    #def addTexDocumentEntry(self, title, path, username, filePathList, informationList, informationTypeList, packageList, packageOptionsList):

    def __init__(self, title = "", filepath = "", filecontent = "", author = "", filePathList = list(), informationList = list(), informationTypeList = list(), packageList = list(), packageOptionsList = list()):
        self.title = title
        self.filepath = filepath
        self.filecontent = filecontent
        self.author = author
        self.filePathList = filePathList
        self.informationList = informationList
        self.informationTypeList = informationTypeList
        self.packageList = packageList
        self.packageOptionsList = packageOptionsList

        self.ensureMainFileinFilePathList()

        return


    def ensureMainFileinFilePathList(self):
        if not self.filepath in self.filePathList:
            self.filePathList.append(self.filepath)
        pass

    def isWritableToDatabase(self):
        return true
        
    '''
        Try to write to database, checking if writable before.
        If writing fails, print information about that in a log file.
        If it succeeds, also print information inside a log file.
    '''    
    def writeToDatabase(self):
        if self.isWritableToDatabase():
            pass
        pass
import sys
sys.path.append("/etc/lpm/libraries")

from dbUtils import dbWriter
from configUtils import ConfigReader

class TexDocument:
    '''
        Provide an interface for TeXDocuments,
        which can be used to check for missing information and also to directly write the TeXDocument into the database.
    '''

    def __init__(self, title = "", filepath = "", author = "", filePathList = list(), informationList = list(), informationTypeList = list(), packageList = list(), packageOptionsList = list()):
        self.entry = {
            "className": "TexDocument",
            "user": "admin",
            "information": list()
        }

        # ToDo: check on the following commented out code
        # self.config_dict = self.get_config()

        # for config in config_dict["mandatory"]:
        #     self.entry["information"].append(
        #         {
        #             "value": 
        #             "label":,
        #             "dataType":,
        #             "mandatory":,
        #         }
        #     )
        #     pass

        # for config in config_dict["optional"]:
        #     pass

        
        
        # self.title = title
        # self.filepath = filepath
        # self.author = author
        # self.filePathList = filePathList
        # self.informationList = informationList
        # self.informationTypeList = informationTypeList
        # self.packageList = packageList
        # self.packageOptionsList = packageOptionsList

        # self.ensureMainFileinFilePathList()

        return

    def get_config(self):
        with ConfigReader.ConfigReader() as configReader:
            content_config = configReader.get_content_config()
            return content_config["TexDocument"]

    def __del__(self): # If this is not done, the old lists will be kept and just be appended later on
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
            with dbWriter.dbWriter() as db_writer:
                # ToDo: check if procedureProtocol is still used
                # procedureProtocol = db_writer.addTexDocumentEntry(
                #                                                     self.title,
                #                                                     self.filepath,
                #                                                     self.author,
                #                                                     self.filePathList,
                #                                                     self.informationList,
                #                                                     self.informationTypeList,
                #                                                     self.packageList,
                #                                                     self.packageOptionsList
                #                                                 )
                # print(procedureProtocol)
                db_writer.addContentEntry(self.entry)
        pass

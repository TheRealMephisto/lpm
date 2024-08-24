import atexit
import mysql.connector
import dbUtils

class dbConnector:

    def __init__(self):
        self.Host = dbUtils.config['host']
        self.user = dbUtils.config['user']
        self.password = dbUtils.config['password']
        self.database = dbUtils.config['database']
        self.dbConnector = mysql.connector.connect(
                                host = self.Host,
                                database = self.database,
                                user = self.user,
                                passwd = self.password
                            )
        self.dbCursor = self.dbConnector.cursor(prepared=True)
        atexit.register(self.close_connection)

    # https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    # http://www.algorithm.co.il/blogs/programming/python-gotchas-1-__del__-is-not-the-opposite-of-__init__/
    # def __del__(self):
    #     self.close_connection()
    #     pass

    def commit(self):
        self.dbConnector.commit()

    def close_connection(self):
        self.dbConnector.close()

    def execute_read_query(self, query, argsList = None):
        if type(argsList) == list or type(argsList) == tuple:
            for arg in argsList:
                if type(arg) in [object, dict, list]:
                    raise Exception("Tried to write a value of incompatible type for into table column!")
            self.dbCursor.execute(query, argsList)
        else:
            self.dbCursor.execute(query)
        results = self.dbCursor.fetchall()
        if len(results) > 0:
            decoded_results = list()
            for result in results:
                decoded_result = list()
                for column_entry in result:
                    if type(column_entry) == bytearray:
                        decoded_result.append(column_entry.decode())
                    else:
                        decoded_result.append(column_entry)
                decoded_results.append(tuple(decoded_result))
            return decoded_results
        return -1

    def append_write_query(self, query, argsList=0):
        if type(argsList) == list or type(argsList) == tuple:
            for arg in argsList:
                if type(arg) in [object, dict, list]:
                    raise Exception("Tried to write a value of incompatible type for into table column!")
            self.dbCursor.execute(query, argsList)
        else:
            self.dbCursor.execute(query)
        self.commit()
        self.dbCursor.execute("SELECT LAST_INSERT_ID();")
        result = self.dbCursor.fetchall()
        return result[0][0]

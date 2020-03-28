import atexit
import mysql.connector

class dbConnector:

    def __init__(self):
        self.Host = "localhost"
        self.user = ""
        self.password = ""
        self.database = "LPMdb"
        self.dbConnector = mysql.connector.connect (
                                host = self.Host,
                                database = self.database,
                                user = self.user,
                                passwd = self.password
                            )
        self.dbCursor = self.dbConnector.cursor()
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

    def execute_read_query(self, query):
        self.dbCursor.execute(query)
        results = self.dbCursor.fetchall()
        if len(results) > 0:
            return results
        return -1

    def append_write_query(self, query):
        self.dbCursor.execute(query)
        return

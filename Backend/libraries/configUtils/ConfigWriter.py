from configparser import ConfigParser

import configUtils

class ConfigWriter:

    def __init__(self):
        return

    def set_database_config(self): # ToDo: ask user for input; to be executed during installation
        self.db_config = ConfigParser()
        self.db_config["Database"] = {
            "host": "localhost",
            "user": "LPMdbUSER",
            "password": "bitteersetzemichdurcheinbessererspasswort",
            "database": "LPMdb"
        }
        return 0
    
    def write_database_config(self):
        self.set_database_config()
        with open(configUtils.db_config_file, 'w') as conf:
            self.db_config.write(conf)
            return 0
        return -1

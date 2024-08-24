from configparser import ConfigParser
import configUtils

class ConfigReader:

    def __init__(self):
        self.db_config = ConfigParser()
        self.__read_db_config()
        self.content_config = ConfigParser()
        self.__read_content_config()
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def __read_db_config(self):
        self.db_config.read(configUtils.db_config_file)
    
    def get_db_config(self):
        return {s:dict(self.db_config.items(s)) for s in self.db_config.sections()}

    def __read_content_config(self):
        self.content_config.read(configUtils.content_config_file)

    def get_content_config(self):
        self.content_config.read(configUtils.content_config_file)
        config_dict = {s:dict(self.content_config.items(s)) for s in self.content_config.sections()}
        for section in config_dict:
            for key in config_dict[section].keys():
                properties_string = config_dict[section][key]
                config_dict[section][key] = self.__propertyString_to_propertyDict(properties_string)
        return config_dict

    def __propertyString_to_propertyDict(self, properties_string):
            properties_dict = dict()
            properties_array = properties_string.split('\n')
            for p in properties_array:
                if p != "":
                    property_info = p.split(':')
                    if len(property_info) != 3:
                        raise Exception("Error while reading config file, at property {property}".format(property=p))
                    properties_dict[property_info[0]] = {
                        "dataType": property_info[1],
                        "array": True if property_info[2] == "array" else False
                    }
            return properties_dict
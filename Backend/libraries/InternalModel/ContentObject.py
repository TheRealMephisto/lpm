import sys
sys.path.append("/etc/lpm/libraries")

from dbUtils import dbWriter
from configUtils import ConfigReader

class ContentObject:
    '''
        Provide a generic interface for content objects,
        which can be used to check against the config files for correctness
        and also to directly write the TeXDocument into the database.
    '''

    def __init__(self, contentType, user, information, db_reader):

        self.contentType = contentType

        self.get_config(contentType)

        self.entry = self._sanitise_entry({
            "className": contentType,
            "user": user,
            "information": information
        },
        db_reader)
        
        self.entry = self._remove_placeholder_information(self.entry)
        self.entry["title"] = self._get_title(self.entry)

        return

    def __del__(self): 
        pass

    def get_config(self, contentType):
        with ConfigReader.ConfigReader() as configReader:
            content_config = configReader.get_content_config()
            self.config_dict = content_config[contentType]

    def _get_title(self, entry):
        '''
            Workaround function, until I solved the problem with the title column
        '''
        for info in self.entry["information"]:
            if info["label"] == "Titel":
                return info["value"]

    def _remove_placeholder_information(self, entry):
        indices_to_remove = list()
        for index in range(0, len(entry["information"])):
            information = entry["information"][index]
            if type(information["value"]) == object:
                information["value"] = self._remove_placeholder_information(information["value"])
            elif information["value"] == [] or information["value"] == None:
                indices_to_remove.insert(0, index)
        for index in indices_to_remove:
            del entry["information"][index]
        return entry

    def _sanitise_entry(self, entry, db_reader):
        '''
            Check if the structure of the entry is valid.
            Used by function addContentEntry().
            It will add information about the checked specifications to the entry.
            If executed again on the same entry,
            it will consider the entry as insane,
            so make sure to only call this function once per entry!
        '''
        keys = entry.keys()

        if not len(keys) == 3 or not set(["className", "user", "information"]) == set(keys):
            raise Exception("Entry could not be sanitised!")

        information_entry_labels_marked_as_mandatory = list()
        
        for index in range(0, len(entry["information"])):
            information = entry["information"][index]
            keys = information.keys()

            if not len(keys) == 6 or not set(["value", "label", "dataType", "mandatory", "array", "Id"]) == set(keys):
                raise Exception("Entry could not be sanitised!")
            
            specEntry = db_reader.getMatchingDbEntryIfPresent("specifications", {
                    "className": entry["className"],
                    "label": information["label"],
                    "dataType": information["dataType"],
                    "mandatory": 1 if information["mandatory"] else 0
                },
            )

            if specEntry == -1:
                raise Exception("Entry could not be sanitised!")
            else:
                entry["information"][index]["specId"] = specEntry["id"]
                if information["mandatory"]:
                    information_entry_labels_marked_as_mandatory.append(information["label"])
            
            if type(information["value"]) in [dict, object]:
                entry["information"][index]["value"] = ContentObject(information["value"]["className"], information["value"]["title"], information["value"]["user"], information["value"]["information"], db_reader).entry
            
            if type(information["value"]) == list:
                for i in range(0, len(information["value"])):
                    if type(information["value"][i]) in [dict, object]:
                        entry["information"][index]["value"][i] = ContentObject(information["value"][i]["className"], information["value"][i]["title"], information["value"][i]["user"], information["value"][i]["information"], db_reader).entry

        specs = db_reader.getSpecification(entry["className"])
        for index in range(1, len(specs["specifications"])+1):
            spec = specs["specifications"][str(index)]
            if spec["mandatory"] and spec["label"] not in information_entry_labels_marked_as_mandatory:
                raise Exception("Missing mandatory information!")
        
        return entry
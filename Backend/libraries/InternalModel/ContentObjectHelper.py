class ContentObjectHelper:
    def __init__(self):
        pass

    def __del__(self): 
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return
    
    def calculate_updates(self, updatedObject, currentObject):

        information_updates = list()
        new_information = list()
        information_ids_to_keep = list()
        information_ids_to_unlink = list()

        for updatedInfo in updatedObject.entry["information"]:
            
            if not type(updatedInfo["Id"]) == int:
                new_information.append(updatedInfo)
            else:
                notFound = True
                for currentInfo in currentObject["available_information"].values():
                    if updatedInfo["Id"] == currentInfo["Id"]:
                        notFound = False
                        information_ids_to_keep.append(updatedInfo["Id"])
                        if updatedInfo["value"] != currentInfo["Value"]:
                            information_updates.append(updatedInfo)
                        break
                if notFound:
                    raise Exception("Found an id in updated entry, which does not exist!")

        for currentInfo in currentObject["available_information"].values():
            if currentInfo["Id"] not in information_ids_to_keep:
                information_ids_to_unlink.append(currentInfo["Id"])

        return {
            "information_updates": information_updates,
            "new_information": new_information,
            "information_ids_to_unlink": information_ids_to_unlink
        }
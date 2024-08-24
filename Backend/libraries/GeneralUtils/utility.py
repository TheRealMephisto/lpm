def stringToList(inputString, separator=','):
    returnList = list()
    substringStart = 0
    currentPosition = 0
    length = len(inputString)
    while (currentPosition < length):
        if inputString[currentPosition] == separator:
            returnList.append(inputString[substringStart:currentPosition])
            substringStart = currentPosition + 1
        currentPosition += 1
    if substringStart < length - 1:
        returnList.append(inputString[substringStart:currentPosition])
    return returnList

def listToString(inputList, separator=','):
    concatenatedString = ""
    for element in inputList:
        concatenatedString += str(element) + separator
    return concatenatedString[:-len(separator)]

def dateFormat(angularDate):
    return angularDate[:10]

def formDataToContentEntry(formData, contentObjectType, user):
    entry = {
        "className": contentObjectType,
        "user": user,
        "information": list()
    }
    for info in formData["mandatory"]:
        value = info["value"]
        if value == "nan":
            continue
        if info["dataType"] == "date":
            value = dateFormat(info["value"])
        entry["information"].append({
            "value": value,
            "label": info["label"],
            "dataType": info["dataType"],
            "mandatory": True,
            "array": info["array"],
            "Id": info["Id"] if type(info["Id"]) is int else None
        })
    for info in formData["optional"]:
        value = info["value"]
        if value == "nan":
            continue
        if info["dataType"] == "date":
            value = dateFormat(info["value"])
        if 0 == 1: # ToDo: implement the array handling
            continue
        # if info["array"] == True:
        #     for val in value:
        #         if val == "nan":
        #             continue
        #         entry["information"].append({
        #             "value": val,
        #             "label": info["label"],
        #             "dataType": info["dataType"],
        #             "mandatory": False,
        #             "array": info["array"],
        #             "Id": None
        #         })
        else:
            entry["information"].append({
                "value": value,
                "label": info["label"],
                "dataType": info["dataType"],
                "mandatory": False,
                "array": info["array"],
                "Id": info["Id"] if type(info["Id"]) is int else None
            })
    return entry

if __name__ == "__main__":
    pass

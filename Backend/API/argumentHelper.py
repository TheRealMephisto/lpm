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

if __name__ == "__main__":
    pass
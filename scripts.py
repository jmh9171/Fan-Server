import json

#/ Scripts.readfile -- Read json and return in a get request.
#Used to read the Json files.
def readFile(file):
    with open(file) as reader:
            data = reader.read()
            reader.close()
            return data


def handlePut(PATH, newJson):
    with open(PATH + '.json', 'w+') as outfile:
        json.dump(newJson, outfile)
    outfile.close() 


def getJsonData(file):
        with open('data.json', 'r') as JFile:
            # load the json file into a variable for later reference
            info = json.load(JFile)
            JFile.close
            return info
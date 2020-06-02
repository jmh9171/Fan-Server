import json
import threading

threadlock = threading.Lock()
#/ Scripts.readfile -- Read json and return in a get request.
#Used to read the Json files.
def readFile(file):
    threadlock.acquire()
    if(file == ''):
        file = 'index.html'
    with open(file) as reader:
            data = reader.read()
            reader.close()
    threadlock.release()
    return data


def handlePut(PATH, newJson):
    threadlock.acquire()
    with open(PATH + '.json', 'w+') as outfile:
        json.dump(newJson, outfile)
    outfile.close() 
    threadlock.release()


def getJsonData(file):
        threadlock.acquire()
        with open('data.json', 'r') as JFile:
            # load the json file into a variable for later reference
            info = json.load(JFile)
            JFile.close
        threadlock.release()
        return info
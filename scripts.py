import json
import threading

threadlock = threading.Lock()
#/ Scripts.readfile -- Read json and return in a get request.
#Used to read the Json files.
def readFile(file):
    threadlock.acquire()
    if(file == ''):
        file = 'index.html'
    try:
        with open(file) as reader:
            data = reader.read()
            reader.close()
    except FileNotFoundError as err:
        file = '/home/pi/FanServer/index.html'
        with open(file) as reader:
            data = reader.read()
            reader.close()
    threadlock.release()
    return data


def handlePut(PATH, newJson):
    threadlock.acquire()
    with open('/home/pi/FanServer/' +PATH + '.json', 'w+') as outfile:
        json.dump(newJson, outfile)
    outfile.close() 
    threadlock.release()


def getJsonData(file):
        threadlock.acquire()
        with open('/home/pi/FanServer/data.json', 'r') as JFile:
            # load the json file into a variable for later reference
            info = json.load(JFile)
            JFile.close
        threadlock.release()
        return info
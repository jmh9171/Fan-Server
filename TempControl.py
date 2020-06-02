import threading
import scripts
import time


class myThread (threading.Thread):
    
    exitFlag = 0
    temp = 0

    def getTemp(self):
        # This function will have access to the temp sensors and be able to see the real-time temp
        self.temp = self.temp + 2
        return self.temp

    def callFlag(self):
        self.exitFlag = 1

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        # monitor for the temp. 
        print ("Starting " + self.name)
        while(self.exitFlag != 1):
            time.sleep(2)
            info = scripts.getJsonData('data.json')
            info['currentTemp'] = str(self.getTemp())
            scripts.handlePut('data',info)
                


        


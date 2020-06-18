import threading
import scripts
import time
import RPi.GPIO as gpio
import board
import adafruit_dht
import os
import signal
import sys


class myThread (threading.Thread):
    
    exitFlag = 0
    temp = 0
    tempDiff = 0
    auto = False
    dhtDevice = adafruit_dht.DHT22(board.D14)

        
        
    def getTemp(self):
        # This function will have access to the temp sensors and be able to see the real-time temp
        try:
            self.temp = format(self.dhtDevice.temperature * (9/5) + 32,"2.1f")
            print("Temp: " + self.temp)
        except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
            if error.args[0] == "Timed out waiting for PulseIn message. Make sure libgpiod is installed.":
                print("Timed Out Error")
                self.reInitDHTDevice()
            
        return self.temp
        

    def callFlag(self):
        self.exitFlag = 1

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def reInitDHTDevice(self):
        self.killSigs()
        print("--> Restarting")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable, 'Server.py'] + sys.argv)
        
        
        
    def killSigs(self):
        for line in os.popen("pgrep libgpiod_pulsei"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)

        
    def run(self):
        # monitor for the temp.
        info = scripts.getJsonData('data.json')
        self.auto = info['auto']  
        print ("Starting " + self.name)
        while(self.exitFlag != 1):
            if self.auto == 'on':
                self.autoOn()
            else:
                time.sleep(2)
                info = scripts.getJsonData('data.json')
                info['currentTemp'] = str(self.getTemp())
                self.auto = info['auto']
                print("Auto: " + self.auto)
                scripts.handlePut('data',info)
        
    def autoOn(self):
        while(self.auto == 'on'):
            time.sleep(2)
            itemp = self.getTemp()
            info = scripts.getJsonData('data.json')
            info['currentTemp'] = str(self.temp)
            self.auto = info['auto']
            scripts.handlePut('data',info)
            if self.temp % 2 != 0:
               gpio.output(19, gpio.LOW)
            else:
                gpio.output(19, gpio.HIGH)
                

            


        


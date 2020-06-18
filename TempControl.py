import threading
import scripts
import time
import RPi.GPIO as gpio
import board
import adafruit_dht
import os
import signal
import sys
import http.client
import xml.etree.ElementTree as ET


class myThread (threading.Thread):
    
    exitFlag = 0
    temp = 0
    tempDiff = 0
    auto = False
    dhtDevice = adafruit_dht.DHT22(board.D14)

        
        
    def getTemp(self):
        try:
            self.temp = format(self.dhtDevice.temperature * (9/5) + 32,"2.1f")
            print("Temp: " + self.temp)
        except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
            if error.args[0] == "Timed out waiting for PulseIn message. Make sure libgpiod is installed.":
                print("Timed Out Error")
                self.reStart()
        return self.temp
        

    def callFlag(self):
        self.exitFlag = 1

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def reStart(self):
        for line in os.popen("pgrep libgpiod_pulsei"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
        print("--> Restarting")
        os.execv(sys.executable, [sys.executable, 'Server.py'] + sys.argv)
        
    def getAPITemp(self):
        conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "07af810bbbmsh617ce2e002ce378p1cbdbcjsnac1c945c0cba"
            }

        conn.request("GET", "/weather?lat=41.133511&lon=-77.456291&id=2172797&units=%2522metric%2522%20or%20%2522imperial%2522&mode=xml", headers=headers)
        res = conn.getresponse()
        data = res.read()

        weather = data.decode("utf-8")
        root = ET.fromstring(weather)
        temp = root.find("temperature")
        print((float(temp.get("value")) - 273.15) * 9/5 + 32)
        

    def run(self):
        # monitor for the temp.
        info = scripts.getJsonData('data.json')
        self.auto = info['auto']  
        print ("Starting " + self.name)
        while(self.exitFlag != 1):
            if self.auto == 'on':
                time.sleep(2)
                itemp = self.getTemp()
                info = scripts.getJsonData('data.json')
                info['currentTemp'] = str(itemp)
                self.auto = info['auto']
                print("Auto: " + self.auto)
                scripts.handlePut('data',info)
                self.getAPITemp()
                time.sleep(10)
            else:
                time.sleep(2)
                info = scripts.getJsonData('data.json')
                info['currentTemp'] = str(self.getTemp())
                self.auto = info['auto']
                print("Auto: " + self.auto)
                scripts.handlePut('data',info)
        

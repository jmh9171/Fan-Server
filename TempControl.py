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
    
    
    info = scripts.getJsonData('data.json')
    exitFlag = 0
    insideTemp = info['indoor']
    outsideTemp = info['outdoor']
    auto = False
    dhtDevice = adafruit_dht.DHT22(board.D14)
    apiCounter = 0

        
    
    def getTemp(self):
        try:
            self.insideTemp = format(self.dhtDevice.temperature * (9/5) + 32,"2.1f")
        except RuntimeError as error:
        # Because errors happen on startup, kill the processes 
            if error.args[0] == "Timed out waiting for PulseIn message. Make sure libgpiod is installed.":
                print("Timed Out Error")
                self.reStart()
        

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
        if (self.apiCounter % 180) == 0:
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
            self.outsideTemp = format((float(temp.get("value")) - 273.15) * 9/5 + 32,"2.1f")
            self.apiCounter = 0
        self.apiCounter = self.apiCounter + 1
        
        
    def regulatePower(self):
        info = scripts.getJsonData('data.json')
        tempDiff = float(self.insideTemp) - float(self.outsideTemp)
        if tempDiff >= 0 and info['power'] == 'off':
            info['power'] = 'on'
            print('Power on')
            gpio.output(19, gpio.HIGH)
        elif tempDiff < 0 and info['power'] == 'on':
            info['power'] = 'off'
            gpio.output(19, gpio.LOW)
            print('Power off')
        scripts.handlePut('data',info)

    def run(self):
        # monitor for the temp.
        info = scripts.getJsonData('data.json')
        self.auto = info['auto']
        
        print ("Starting " + self.name)
        while(self.exitFlag != 1):
            time.sleep(2)
            self.getTemp()
            if self.auto == 'on':
                self.getAPITemp()
                self.regulatePower()
            info = scripts.getJsonData('data.json')
            info['indoor'] = str(self.insideTemp)
            info['outdoor'] = str(self.outsideTemp)
            self.auto = info['auto']
            scripts.handlePut('data',info)

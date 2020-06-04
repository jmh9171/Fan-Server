import threading
import scripts
import time
import http.client


class myThread (threading.Thread):
    
    exitFlag = 0
    temp = 0

    def getTemp(self):
        # This function will have access to the temp sensors and be able to see the real-time temp


        conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "07af810bbbmsh617ce2e002ce378p1cbdbcjsnac1c945c0cba"
            }

        conn.request("GET", "/weather?callback=test&id=2172797&units=%2522metric%2522%20or%20%2522imperial%2522&mode=xml%252C%20html&q=Lockhaven", headers=headers)
        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

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
            


                


        


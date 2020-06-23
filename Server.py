import http.server
import socketserver
import scripts
import TempControl
import threading
import RPi.GPIO as gpio

PORT = 8000

threadLock = threading.Lock()

gpio.setup(26, gpio.OUT)
gpio.output(26, gpio.LOW)
gpio.setup(19, gpio.OUT)


# inherited handler class where adjustments and if() will go
class MyTCPHandler(http.server.SimpleHTTPRequestHandler):

    def send_headers(self, headerType='null'):
        self.send_response(200)
        if headerType == '':
            self.send_header('Content-type','text/html')
        else:
            self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
        self.end_headers()

    def send_put_resonse(self, newData):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Content-type','data/json')
        self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
        self.end_headers()
        self.wfile.write(newData.encode())

    #handles put requests
    def do_PUT(self):
        request = self.path.lower()[1::]
        info = scripts.getJsonData('data.json')
        if request == 'power':
            if info[request] == 'on':
                info[request] = 'off'
                gpio.output(19, gpio.LOW)
                print(request +': '+info[request])
            elif info[request] == 'off':
                info[request] = 'on'
                gpio.output(19, gpio.HIGH)
                print(request +': '+info[request])
        else:
            if info[request] == 'on':
                info[request] = 'off'
                print(request +': '+info[request])
            elif info[request] == 'off':
                info[request] = 'on'
                print(request +': '+info[request])
                
        #overwrites the json file with the new json data
        scripts.handlePut('data',info)
        #reads the newly overwritten file to send it as a response
        data = scripts.readFile('data.json')
        self.send_put_resonse(data)


    def do_GET(self):
        request = self.path.lower()[1::]
        data = scripts.readFile(request)
        self.send_headers(request)
        self.wfile.write(data.encode())

        # overridden TCPServer class, this is where the server loop is
class MyTCPServer(socketserver.TCPServer):

    def server_activate(self):
        # call the super class
        super().server_activate()
        print('In server_activate')
        Tthread = TempControl.myThread(2,'tempControl')
        Tthread.start()

httpd = MyTCPServer(("", PORT), MyTCPHandler)
print("serving at port", PORT)
httpd.serve_forever()

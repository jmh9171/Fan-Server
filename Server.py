# import these to be able to create the server and set it to a port
import http.server
import socketserver
import time
import scripts
import TempControl
import threading

# the port number can be any port number above whatever the cutoff is
PORT = 8000
threadLock = threading.Lock()

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
        info = scripts.getJsonData('data.json')
        request = self.path.lower()[1::]
        if info[request] == 'on':
            info[request] = 'off'
        elif info[request] == 'off':
            info[request] = 'on'
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

with MyTCPServer(("", PORT), MyTCPHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
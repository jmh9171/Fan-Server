# import these to be able to create the server and set it to a port
import http.server
import socketserver
import json
import time
import scripts
# the port number can be any port number above whatever the cutoff is
PORT = 8000

# inherited handler class where adjustments and if() will go
class MyTCPHandler(http.server.SimpleHTTPRequestHandler):

    def send_headers(self, headerType='null'):
        self.send_response(200)
        if headerType == 'html':
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
        print("URL: {}".format(self.path))

        #self.path == the URL sent with the put request
        if self.path.lower() == '/change_power':
            # gets the json data from the file and returns it in a json object 
            info = scripts.getJsonData('data.json')
            if info['power'] == 'off':
                info['power'] = 'on'
            elif info['power'] == 'on':
                info['power'] = 'off'
            #overwrites the json file with the new json data
            scripts.handlePut('data',info)
            #reads the newly overwritten file to send it as a response
            data = scripts.readFile('data.json')
            self.send_put_resonse(data)

                   

        elif self.path.lower() == '/change_auto':
            print('change_auto request called')
            info = scripts.getJsonData('data.json')
            if info['auto'] == 'true':
                info['auto'] = 'false'
            elif info['auto'] == 'false':
                info['auto'] = 'true'
            # open the json file
            scripts.handlePut('data',info)
            #reads the newly overwritten file to send it as a response
            data = scripts.readFile('data.json')
            self.send_put_resonse(data)


    def do_GET(self):
        # print the path which holds the URL
        print("URL: {}".format(self.path))
        #if URL is for the json data
        if self.path.lower() == '/data.json':
            jData = scripts.readFile('data.json')
            self.send_headers()
            self.wfile.write(jData.encode())
        #if not return the web page
        else:
            print('getting index.html')
            stri = scripts.readFile('index.html')
            self.send_headers('html')
            self.wfile.write(stri.encode())


        # overridden TCPServer class, this is where the server loop is
class MyTCPServer(socketserver.TCPServer):

    def server_activate(self):
        # call the super class
        super().server_activate()
        print('In server_activate')


with MyTCPServer(("", PORT), MyTCPHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
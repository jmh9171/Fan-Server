## TODO - All of my comments are preceded by a #/ - use them to identify mine from yours.
# import these to be able to create the server and set it to a port
import http.server
import socketserver
import json
import time

# the port number can be any port number above whatever the cutoff is
PORT = 32323
#/ Make this something more reasonable. (E.G. 8080).


# Json stuff for interface between server and javascript code

# TODO - Make this a file and load it on init.
# HTTP puts should overwrite this file with the new data.

# inherited handler class where adjustments and if() will go
class MyTCPHandler(http.server.SimpleHTTPRequestHandler):

    #/ This function makes no sens to me.
    # function to log any accesses to the server
    def accLog(self, msg):
        # opens the log file to append
        with open('Log.txt', 'a') as log:

            # get the time
            localtime = time.asctime(time.localtime(time.time()))

            # write a formatted message to the file
            log.write('Accessed: {} By: {} to {}\n'.format(
                localtime, self.address_string(), msg))

            # open the json file
            with open('data.json', 'r') as jf:

                # load the json data
                jsn = json.load(jf)

                #/ Hard-coding on start-up is bad!

                # write to the log file again with the json data formatted
                log.write('\tFan Status:  auto: {}, Power: {}, Last turned on: {}\n'.format(
                    jsn['auto'], jsn['power'], jsn['Turned on Last']))

                jf.close
            log.close

    /# See my example sendheader.
    # function will set the header info for each response
    def sendWHeader(self, response, content_type, data):

        # send the response number ex. 200
        self.send_response(response)

        # set the other parts of the header in the header buffer
        self.send_header("Content-type", content_type)

        # sends a blank line to end the header part of the response
        self.end_headers()

        # Write the encoded version of the string that contains the file text to the socket
        self.wfile.write(data.encode())

    def do_PUT(self):
        # if '/change_power' is the GET request

        #/ Make this a script. You can export the scripts to another python file, and import them at the top.
        #/ See the additional file for a better example of how to handle put requests.
        #/ This is a pretty terribly inneficient way of sending data back and forth, btw. Everything should be a json file that gets sent back and forth
        #/ between server and browser.
        if self.path.lower() == '/change_power':

            print('change_power request called')

            # open this for reading
            with open('data.json', 'r') as JFile:

                # load the json file into a variable for later reference
                info = json.load(JFile)

                # close the file
                JFile.close

                print('Power:  ' + info['power'])

                # if the power is set to 'off'
                if info['power'] == 'off':

                    # change info['power']
                    info['power'] = 'on'

                # else if the power is set to 'on'
                elif info['power'] == 'on':

                    # change info['power']
                    info['power'] = 'off'

                # set newData variable to info
                newData = info

                # open the json file
                with open('data.json', 'w') as outfile:

                    # and dump the new data into it to update the fans
                    json.dump(newData, outfile)

                    # close the file
                    outfile.close

                # open the file to send the data
                with open('data.json', 'r') as sendF:

                    # read it in
                    sf = sendF.read()

                    # set header info
                    self.sendWHeader(200, 'text/json', sf)

                    self.accLog('Change Power')

                    # close file
                    sendF.close

        elif self.path.lower() == '/change_auto':

            print('in change auto')

            with open('data.json', 'r') as JFile:

                # load the json file into a variable for later reference
                info = json.load(JFile)

                # close the file
                JFile.close

                print('auto:  ' + info['auto'])

                # if the auto is set to 'true'
                if info['auto'] == 'true':

                    # change it to false
                    info['auto'] = 'false'

                # if the auto is set to 'false'
                elif info['auto'] == 'false':

                    # change it to 'true'
                    info['auto'] = 'true'

                # set new data to info
                newData = info
                # open the json file
                with open('data.json', 'w') as outfile:

                    # and dump the new data into it to update the fans
                    json.dump(newData, outfile)

                    # close the file
                    outfile.close
                # open the data file for reading
                with open('data.json', 'r') as j:

                    # read it in
                    jData = j.read()

                    # send data
                    self.sendWHeader(200, 'data/json', jData)

                    self.accLog('Change auto Setting')

                    # close file
                    j.close

    #####for when there is a GET request#####

    def do_GET(self):
        print("In do_GET")

        # print the path which holds the URL
        print("URL: {}".format(self.path))
        # if the request is for the Json data
        if self.path.lower() == '/data.json':

            print('getting data.json')

            # open the data file for reading
            with open('data.json', 'r') as j:

                # read it in
                jData = j.read()

                # send data
                self.sendWHeader(200, 'data/json', jData)

                self.accLog('Get Json File')

                # close file
                j.close

        else:

            print('getting index.html')

            # open the file that we are trying to send
            with open('index.html', 'r') as f:

                # read the file
                stri = f.read()

                # close file
                f.close

            # send the file
            self.sendWHeader(200, 'text/html', stri)

            self.accLog('Get HTML Page')

        print('do_GET end')


# overridden TCPServer class, this is where the server loop is
class MyTCPServer(socketserver.TCPServer):

    def server_activate(self):

        # call the super class
        super().server_activate()

        print('In server_activate')


# In this case, 'socketserver.TCPServer' refers to a class constructor
# 'as httpd' is what were calling the object and server_forever is a function that will get called.
# this syntax is used because it will automatically call the __enter__() and __exit__() functions
# for the setup and closing of whatever code you're trying to run.
with MyTCPServer(("", PORT), MyTCPHandler) as httpd:

    print("serving at port", PORT)

    httpd.serve_forever()

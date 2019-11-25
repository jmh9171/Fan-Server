    def send_headers(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
        self.end_headers()
    def send_put_resonse(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
        self.wfile.write("PUT response")
    def do_GET(self):
        path = self.path.rstrip("/")
        data = scripts.readFile( '<filepath>' + ".json")
        self.send_headers()
        self.wfile.write(data)
        return
    def do_GET(self):
        if None != re.search('<filepath>', self.path):
            data = scripts.readFile(DIR + '<filePath>')
            self.send_headers()
            self.wfile.write(data)
            return
    def do_PUT(self):
        if None != re.search('<filepath>', self.path):
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            self.send_put_resonse()
            data = json.loads(self.data_string)
            scripts.handlePut('<filepath>', data)
            return



#/ Scripts.readfile -- Read json and return in a get request.
#Used to read the Json files.
def readFile(file):
        with open(file) as reader:
                data = reader.read()
        reader.close()
        return data


def handlePut(PATH, newJson):
    with open(PATH + '.json', 'w+') as outfile:
        json.dump(newJson, outfile)
        outfile.close()
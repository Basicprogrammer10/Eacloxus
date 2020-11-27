############ VARS ############
hostName = "localhost"
serverPort = 1234
serverVersion = "0.1"

database = "data/data.json"
authFile = "data/auth.json"

toImport = {"base64": "", "json": "", "urllib.parse": "urlparse",
            "time": "", "http.server": "BaseHTTPRequestHandler, HTTPServer", "datetime": "datetime"}
########### SETUP ###########
for i in toImport:
    defult = False if toImport[i] != "" else True
    exec(str("from " if defult == False else "import ") + str(i) +
         str(" import " + toImport[i] if defult == False else ""))


def colored(text, color):
    ColorCodes = {"black": "30", "red": "31", "yellow": "33", "green": "32", "blue": "34",
                  "cyan": "36", "magenta": "35", "white": "37", "gray": "90", "reset": "0"}
    return "\033[" + ColorCodes[str(color).lower()] + "m" + str(text) + "\033[0m"
######### FUNCTIONS #########


class MyServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        urlp = urlparse(self.path)
        urlps = urlp.path.split("/")
        if urlps[1] == "login":
            try:
                for i in self.path.split("?")[1].split("&"):
                    if i.split("=")[0].lower() == "version":
                        if self.client_address[0] in getVersionIp(i.split("=")[1], authFile):
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(bytes(createJsonResponce(
                                [['serverVersion', serverVersion], ['auth', 'success']]), "utf-8"))
                            databaseWrite(database, createJsonResponce(
                                [['ip', self.client_address[0]], ['date', datetime.now().strftime("%d/%m/%Y %H:%M:%S")], ['auth', 'success']]))
                        else:
                            self.send_response(401)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(bytes(createJsonResponce(
                                [['serverVersion', serverVersion], ['auth', 'denied']]), "utf-8"))
                            databaseWrite(database, createJsonResponce(
                                [['ip', self.client_address[0]], ['date', datetime.now().strftime("%d/%m/%Y %H:%M:%S")], ['auth', 'denied']]))
            except:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(createJsonResponce(
                    [['serverVersion', serverVersion], ['auth', 'invalidRequest']]), "utf-8"))
                databaseWrite(database, createJsonResponce(
                    [['ip', self.client_address[0]], ['date', datetime.now().strftime("%d/%m/%Y %H:%M:%S")], ['auth', 'invalid Request']]))


def createJsonResponce(jsonData):
    data = {}
    for i in jsonData:
        data[i[0]] = i[1]
    return json.dumps(data)


def getVersionIp(version, auth):
    try:
        auth = json.loads(open(auth, 'r').read())
        return auth['version'][version]
    except KeyError:
        return []


def databaseRead(file):
    file = open(file, "r", encoding="utf-8")
    data = json.loads(file.read())
    return data


def databaseWrite(file, data):
    working = open(file, "r+", encoding="utf-8").read()
    comma = "," if working != "[]" else ""
    open(
        file, "w", encoding="utf-8").write(working[:-1] + comma + "\n" + data + "]")


def startupChecks():
    try:
        working = open(database, "r").read()
        if working == "":
            open(database, "w").write("[]")
    except:
        open(database, "x")
        startupChecks()


def startServer(hostName, serverPort):
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(colored("Server started http://%s:%s" %
                  (hostName, serverPort), "green"))
    try:
        webServer.serve_forever()
    except:
        pass
    webServer.server_close()
    print(colored("Server stopped", "red"))


####### MAIN FUNCTION #######


def main():
    startupChecks()
    startServer(hostName, serverPort)


if __name__ == "__main__":
    main()

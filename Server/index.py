############ VARS ############
hostName = "0.0.0.0"
serverPort = 8080
database = "data.json"

toImport = {"base64": "", "json": "", "urllib.parse": "urlparse",
            "time": "", "http.server": "BaseHTTPRequestHandler, HTTPServer"}
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
    def do_GET(self):
        urlp = urlparse(self.path)
        urlps = urlp.path.split("/")
        if urlps[1] == "r" and len(urlps) > 2 and urlps[2] != "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes(
                    formatReadResponce(
                        responceFile,
                        databaseRead(database)[urlps[2]]["url"]),
                    "utf-8",
                ))
        elif urlps[1] == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(formatReadResponce(
                responceFile, "/create/"), "utf-8"))
        elif urlps[1] == "create":
            try:
                if urlps[2] == "api":
                    pram = urlparse(self.path).query.split("?")
                    working = []
                    for i in pram:
                        working.append(i.split("=", 1))
                    if inDatabase(str(
                            base64.b64decode(working[1][1]).decode())):
                        self.send_response(409)
                        self.end_headers()
                    else:
                        self.send_response(201)
                        self.end_headers()
                        databaseWrite(database, '"' + str(base64.b64decode(working[1][1]).decode(
                        )) + '":{"url":"' + str(base64.b64decode(working[0][1]).decode()) + '"}}',)
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        bytes(fileRead("assets/create.html"), "utf-8"))
            except ImportError:
                pass
        else:
            if urlps[1].lower() in files:
                self.send_response(200)
                self.wfile.write(fileReadB("assets/" + urlps[1]))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(fileRead("assets/404.html"), "utf-8"))


def inDatabase(data):
    if data in databaseRead(database):
        return True
    else:
        return False


def fileRead(file):
    return open(file, "r").read()


def fileReadB(file):
    return open(file, "br").read()


def formatReadResponce(file, url):
    file = open(file, "r", encoding="utf-8")
    data = file.read().format(url=url)
    return data


def databaseRead(file):
    file = open(file, "r", encoding="utf-8")
    data = json.loads(file.read())
    return data


def databaseWrite(file, data):
    working = open(file, "r+", encoding="utf-8").read()
    comma = "," if working != "{}" else ""
    open(file, "w", encoding="utf-8").write(working[:-1] + comma + "\n" + data)


def startupChecks():
    try:
        working = open(database, "r").read()
        if working == "":
            open(database, "w").write("{}")
    except:
        open(database, "x")
        startupChecks()


def startServer(hostName, serverPort):
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(
        colored("Server started http://%s:%s" % (hostName, serverPort),
                "green"))
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

from flask import Flask
############ VARS ############
app = Flask(__name__)

initialise = {}
toImport = {}
########### SETUP ###########
for i in toImport:
    defult = False if toImport[i] != '' else True
    exec(str('from ' if defult == False else 'import ')+str(i) +
         str(' import ' + toImport[i] if defult == False else ''))


def colored(text, color):
    ColorCodes = {'black': '30', 'red': '31', 'yellow': '33', 'green': '32', 'blue': '34',
                  'cyan': '36', 'magenta': '35', 'white': '37', 'gray': '90', 'reset': '0'}
    return '\033[' + ColorCodes[str(color).lower()] + 'm' + str(text) + "\033[0m"


for i in initialise:
    exec(i + '=' + initialise[i])
######### FUNCTIONS #########


def function():
    pass
####### MAIN FUNCTION #######


def main():
    @app.route('/')
    def hello_world():
        return 'Hello World'

    app.run()


if __name__ == "__main__":
    main()

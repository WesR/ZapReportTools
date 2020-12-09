from reportLatex import *
import sys


'''
TODO dedupe and such
'''

#######################

def parseZAPJson(siteRegex = Null):
    pass

def renderZAPJson(scanJSON):
    pass

#######################
def init():
    pass

def destroy():
    pass

if __name__ == "__main__":
    #We run on whatever file is passed in
    with open(sys.argv[0]) as data:
        scan = json.load(data)

    document = str()
    document += preamble("Webservice Report", "Wes Ring", scan["@generated"])#could use scan["site"][0]["@host"]
    document += abstract([scan["site"][0]["@host"]])
    for x in scan["site"]:
        document += site(x)
    document += endDoc()

    text_file = open("./report.tex", "w")
    text_file.write(document)
    text_file.close()

    os.system("pdflatex report.tex")
    res = os.system("pdflatex report.tex")#sometimes you just need 2 passes
    print(res)
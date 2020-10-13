import json

def latexClean(input):
    return input.replace("\\", "\\").replace("&", "\&").replace("_", "{\_}").replace("#", "\#").replace("%", "\%").replace("<", "$<$").replace(">", "$>$")

def latexURL(input):
    return "\\url{" + input + "}"

def pStrip(input):
    return input.replace("<p>", "").replace("</p>", "")

def preamble(website = str(), author = "GIS", date = "2020"):
    output = str()
    output += "\\documentclass[10pt]{article}"
    output += "\n\\usepackage[utf8]{inputenc}"
    output += "\n\\usepackage[margin=1in]{geometry}"
    output += "\n\\usepackage[small]{titlesec}"
    output += "\n\\usepackage{setspace}"
    output += "\n\\usepackage{hyperref}"

    output += "\n%opening"
    output += "\n\\title{ZAP Scan report of " + website + "}"
    output += "\n\\author{" + author + "}"
    output += "\n\\date{" + date + "}"
    
    output += "\n\\hbadness=99999"
    
    #Title
    output += "\n\\begin{document}"
    output += "\n\\null  % Empty line"
    output += "\n\\nointerlineskip  % No skip for prev line"
    output += "\n\\vfill"
    output += "\n\\let\\snewpage \\newpage"
    output += "\n\\let\\newpage \\relax"
    output += "\n\\maketitle"
    output += "\n\\let \\newpage \\snewpage"
    output += "\n\\vfill "
    output += "\n\\newpage"
    
    #Table of contents
    output += "\n\n{\\hypersetup{linktoc=all,hidelinks}"
    output += "\n\\tableofcontents"
    output += "\n}\n"
    output += "\n\\newpage"
    return output

def abstract(websites = list()):
    output =  str()
    output += "\n\\begin{abstract}"
    output += "\nThis is a scan of "
    for site in websites:
        output += site + ", "
    
    output = output[0:-2]#Remove extra .space
    output += "\n. This is blah blah blah boiler plate stuff."
    output += "\n\\end{abstract}"
    return output

def instances(scan, index):
    output = str()
    
    output += "\n\\item[] " + str(index)
    output += "\n\\begin{tabular}{| l | p{14cm}}"

    for key,value in scan.items():
        output += "\n" + latexClean(key) + " & " + latexClean(value) + " \\\\"
    
    output += "\n\\end{tabular}"
    return output

def refrences(input):
    output = str()
    if ("<p>" in input):
        if (len(pStrip(input)) == 0):
            return output

        output += "\n\\begin{itemize}"

        for x in input.split("<p>"):
            if (pStrip(x) != ""):
                output += "\n\\item " + latexURL(latexClean(pStrip(x)))

        output += "\n\\end{itemize}"
    return output

def alert(scan):
    output = str()
    output += "\n\\subsubsection{" + latexClean(scan["name"]) + "}"
    output += "\n\\begin{itemize}"
    #if ("name" in scan):
    #    output += "\n\\item[] \\textbf{Name} : " + latexClean(scan["name"])
    if ("confidence" in scan):
        output += "\n\\item[] \\textbf{Confidence} : " + scan["confidence"]
    if ("desc" in scan):
        output += "\n\\item[] \\textbf{Description} : " + latexClean(pStrip(scan["desc"]))
    if ("solution" in scan):
        output += "\n\\item[] \\textbf{Solution} :  " + latexClean(pStrip(scan["solution"]))
    if ("instances" in scan):
        output += "\n\\item[] \\textbf{Instances}"
        output += "\n\\begin{enumerate}"
        index = 0
        for x in scan["instances"]:
            output += instances(x, index)
            index += 1
        output += "\n\\end{enumerate}"
    if ("reference" in scan):
        output += "\n\\item[] \\textbf{Reference} : " + refrences(scan["reference"])
    output += "\n\\end{itemize}"
    return output

def site(scan):
    output = str()

    output += "\n\\section{Findings for " + scan["@host"] + "}"
    output += "\nScan of " + scan["@host"] + " was done over port "+scan["@port"]+" and with SSL "+scan["@ssl"]+"."

    #sort alerts
    high = list()#3
    med = list()#2
    low = list()#1
    info = list()#0
    for x in scan["alerts"]:
        if (x["riskcode"] == "0"):
            info.append(x)
        elif (x["riskcode"] == "1"):
            low.append(x)
        elif (x["riskcode"] == "2"):
            med.append(x)
        else:#Default to high, just in case
            high.append(x)

    if (len(high) != 0):
        output += "\n\\subsection{High}"
        for x in high:
            output += alert(x)
    if (len(med) != 0):
        output += "\n\\subsection{Medium}"
        for x in med:
            output += alert(x)
    if (len(low) != 0):
        output += "\n\\subsection{Low}"
        for x in low:
            output += alert(x)
    if (len(info) != 0):
        output += "\n\\subsection{Informational}"
        for x in info:
            output += alert(x)
    
    return output

def endDoc():
    return "\n\\end{document}"

if __name__ == "__main__":
    with open('./testData/dvwa.json') as data:    
        scan = json.load(data)

    document = str()
    document += preamble(scan["site"][0]["@host"], "Wes Ring", scan["@generated"])
    document += abstract([scan["site"][0]["@host"]])
    for x in scan["site"]:
        document += site(x)
    document += endDoc()

    text_file = open("./outputTest/Output.tex", "w")
    text_file.write(document)
    text_file.close()
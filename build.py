#!/usr/bin/python3
import subprocess
import os
from os.path import isfile, join
import sys
import pprint
import fileinput

SECTION_LIST= "00_include_file_list.adoc"

def buildAll():
    print("Building all")
    print("Building sections")
    buildSections()
    print("Writing table of contents")
    writeToc()
    # print("Adding TOC to index.adoc")
    # makeIndex()
    print("Writing HTML index file")
    subprocess.run(["asciidoctor", "-a", "stylesheet=../css/theta.css",
                    "--verbose",
                    "--destination-dir", "html",
                    "src/index.adoc"])

def makeIndex():
    try:
        indexSrc = open('src/index.adoc', 'w')
        tocHtml = fileinput.input('html/toc.html')
        indexSrc.write("++++ \n")
        for line in tocHtml:
            indexSrc.write(line)
        indexSrc.write("++++")
    except IOError:
        print("Can't open files")

def listSrc():
    srcFiles = os.listdir("src")
    for file in srcFiles:
        print(file)

def buildSections():
    """Build HTML for each section 2 src file"""
    print("Building section files")
    srcFiles = os.listdir("src")
    for file in srcFiles:
        if file != "index.adoc" and file != SECTION_LIST:
            subprocess.run(["asciidoctor",
                            "-a", "stylesheet=../css/theta.css",
                            "--verbose",
                            "--destination-dir", "html",
                            "src/" + file ])

def getTitles():
    """get section titles for eache section 2 src file"""
    print("Extracting section headings")
    titleDict = {}
    srcFiles = os.listdir("src")
    for file in srcFiles:
        try:
            fileAdoc = open("src/" + file)
            for lineNum in range (3):
                line = fileAdoc.readline()
                if "==" in line:
                    if "===" not in line:
                        tempLine = line.split("=="[:1])
                        title = tempLine[2].strip()
                        titleDict[file] = title
            fileAdoc.close()
        except IOError:
            pass
    return(titleDict)

def tocList():
    """Build table of contents"""
    print("Building table of contents")
    try:
        sectionsFile = open("src/" + SECTION_LIST)
        filesList = []
        for line in sectionsFile:
            if line.strip() != '':
                filename = line.strip()
                filename = filename.split("::")[1:][0]
                baseFile = filename.split(".")[:1][0]
                filesList.append(baseFile)
        sectionsFile.close()
    except IOError:
        pass
    return filesList

def buildToc():
    tocIndex = ""
    baseNames = tocList()
    tocDictionary = getTitles()
    tocIndex = "<ol> \n"
    for filename in baseNames:
        title = tocDictionary[filename + ".adoc"]
        section = "<li><a href='" + filename + ".html'" + ">" + title + "</a></li> \n"
        tocIndex = tocIndex + section
    tocIndex = tocIndex + "</ol>"
    return tocIndex

def writeToc():
    tocHtml = buildToc()
    try:
        tocFile = open("html/toc.html", 'w')
        tocFile.write(tocHtml)
        tocFile.close()
    except IOError:
        print("Can't write to toc.html")

args = sys.argv

if len(args) == 2:
    if args[1] == "all":
        buildAll()
    elif args[1] == "list":
        listSrc()
    elif args[1] == "sections":
        buildSections()
    elif args[1] == "toc":
        writeToc()
    elif args[1] == "titles":
        getTitles()

else:
    print("\nUsage: build.py COMMAND \n" +
        "    all \t\t build all source files into single file \n" +
        "    list \t\t list all source files \n" +
        "    sections \t\t build sections as separate HTML files \n" +
        "    toc \t\t creation table of contents (toc) \n" +
        "    titles \t\t create titles \n")

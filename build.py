#!/usr/bin/python3
import subprocess
import os
from os.path import isfile, join
import sys

def buildAll():
    print("Building all")
    subprocess.run(["asciidoctor", "-a", "stylesheet=../css/theta.css",
                    "--verbose",
                    "--destination-dir", "html",
                    "src/index.adoc"])

def listSrc():
    srcFiles = os.listdir("src")
    for file in srcFiles:
        print(file)

def buildSections():
    """Build HTML for each section 2 src file"""
    print("Building section files")
    srcFiles = os.listdir("src")
    for file in srcFiles:
        if file != "index.adoc":
            subprocess.run(["asciidoctor",
                            "-a", "stylesheet=../css/theta.css",
                            "--verbose",
                            "--destination-dir", "html",
                            "src/" + file ])

args = sys.argv

if len(args) == 2:
    if args[1] == "all":
        buildAll()
    elif args[1] == "list":
        listSrc()
    elif args[1] == "sections":
        buildSections()

else:
    print("\nUsage: build.py COMMAND \n" +
        "    all \t\t build all source files into single file \n" +
        "    list \t\t list all source files \n" +
        "    sections \t\t build sections as separate HTML files \n")

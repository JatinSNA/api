#!/usr/bin/python3
import subprocess

subprocess.run(["asciidoctor", "-a", "stylesheet=../css/theta.css", "-v",
                "-o", "html/index.html", "src/index.adoc"])

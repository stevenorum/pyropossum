#!/usr/bin/env python3

# The eventual goal is to have an array of arduinos behind a webserver on the machine so that it's easier to connect to them from multiple different locations.
# Could be used for local applications, or to connect from other machines on the local network.
# Not much written yet.

from flask import Flask

from pyropossum.arduino import core as ardcore

app = Flask(__name__)

ard = ardcore.sopen()

@app.route("/get_arduinos")
def hello():
    return "Hello World!"
    

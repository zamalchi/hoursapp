#!/usr/bin/python

import argparse

from bottle import run

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)
parser.add_argument('-m', help = "Mailing address", action="store", dest="m", required = True)
parser.add_argument('-d', help = "Dev mode", action="store", dest="d", required = True) # True|1 / False|0
args = parser.parse_args()

from hoursSrc import *

port = args.p
email = args.m
dev = args.d

smtpInit(email)
setDevMode(dev)


labelsInit("labels.txt")


if dev == "True":
    # reloader: restart on module file change
    run(reloader=True, host='localhost', port=port, debug=True)
else:
    run(host='localhost', port=port, debug=True)
#!/usr/bin/python

import argparse

from src.bottle import run

from src.hoursSrc import *

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)

parser.add_argument('-s', help = "Sender address", action="store", dest="s", required = False)
parser.add_argument('-m', help = "Receiver address", action="store", dest="m", required = False)

parser.add_argument('-l', help = "Logging server address", action="store", dest="l", required = False)

parser.add_argument('-d', help = "Dev mode", action="store", dest="d", required = False) # True|1 / False|0

args = parser.parse_args()

port = args.p
mailFrom = args.s
mailTo = args.m
loggingServer = args.l

dev = args.d

smtpInit(mailTo, mailFrom)

loggingServerInit(loggingServer)

labelsInit("../config/labels.txt")


if dev == "True":
    # reloader: restart on module file change
    run(reloader=True, host='localhost', port=port, debug=True)
else:
    run(host='localhost', port=port, debug=True)
#!/usr/bin/python

import argparse

from bottle import run

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)

parser.add_argument('-s', help = "Sender address", action="store", dest="s", required = False)
parser.add_argument('-m', help = "Receiver address", action="store", dest="m", required = False)

parser.add_argument('-d', help = "Dev mode", action="store", dest="d", required = False) # True|1 / False|0

args = parser.parse_args()

from hoursSrc import *

port = args.p
mailFrom = args.s
mailTo = args.m
dev = args.d

smtpInit(mailTo, mailFrom)

labelsInit("labels.txt")


if dev == "True":
    # reloader: restart on module file change
    run(reloader=True, host='localhost', port=port, debug=True)
else:
    run(host='localhost', port=port, debug=True)
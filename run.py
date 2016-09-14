#!/usr/bin/python

import os
import argparse

from src.bottle import run

from src.hoursSrc import *

from config.dirs import ROOT_DIR

ROOT_DIR = os.path.dirname(os.path.abspath('.'))
# argparse
parser = argparse.ArgumentParser()

parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)
#parser.add_argument('-r', help = "Remote logging server address", action="store", dest="r", required = False)

args = parser.parse_args()

port = args.p
#loggingServer = args.r

###########################################################################################

# keys
address_key = "loggingServerAddress"
port_key = "loggingServerPort"
sender_key = "sender"
receivers_key = "receivers"

try:
    f = open(os.path.join(ROOT_DIR, 'config/settings'))
    r = filter(None, f.read().split("\n"))

    d = {}
    for each in r:
        key, val = each.split("=")
        d[key.strip()] = val.strip()

    # logging server
    if address_key in d.keys() and port_key in d.keys():
        loggingServerInit(d[address_key], d[port_key])

    # smtp
    if sender_key in d.keys() and receivers_key in d.keys():
        smtpInit(list(d[receivers_key].split(",")), d[sender_key])

except IOError:
    print("***\nERROR: config/settings file not found. Some features may not work.\n***")

###########################################################################################


labelsInit(os.path.join(ROOT_DIR, "config/labels.txt"))

run(host='localhost', port=port, debug=True)

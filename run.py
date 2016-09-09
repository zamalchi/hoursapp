#!/usr/bin/python

import os
import argparse

from src.bottle import run

from src.hoursSrc import *

from config.dirs import ROOT_DIR

# argparse
parser = argparse.ArgumentParser()

parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)
parser.add_argument('-r', help = "Remote logging server address", action="store", dest="r", required = False)

args = parser.parse_args()

port = args.p
loggingServer = args.r

loggingServerInit(loggingServer)

labelsInit(os.path.join(ROOT_DIR, "config/labels.txt"))

run(host='localhost', port=port, debug=True)
#!/usr/bin/env python

"""
Module for printing in color
"""

import functools

#### COLOR CODES AND ALIASES

PURPLE = HEADER = '\033[95m'
GREEN = OK = OKGREEN = '\033[92m'
BLUE = OKBLUE = '\033[94m'
YELLOW = WARNING = '\033[93m'
RED = FAIL = ERROR = '\033[91m'

BOLD = STRONG = '\033[1m'
UNDERLINE = '\033[4m'

END = '\033[0m'

#### FUNCTIONS

"""
Prints a message in a specified color
@:param color: one of the defined color codes
@:param message: the message to be printed
"""
def printColor(color, message):
    print("{start}{msg}{end}".format(start=color, msg=message, end=END))

"""
Returns a partial function with the color locked
@:param color: color which the returned function will use
@:return: function (message) => printColor(color, message)
"""
def printColorPartial(color):
    return functools.partial(printColor, color)

#### DEFINED PARTIAL FUNCTIONS

printHeader = printColorPartial(HEADER)
printOk = printOK = printColorPartial(GREEN)
printWarn = printColorPartial(YELLOW)
printFail = printColorPartial(RED)
printBold = printColorPartial(BOLD)

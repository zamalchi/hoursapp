#!/usr/bin/python

import os

ROOT_DIR = "/".join(os.path.abspath(__file__).split("/")[0:-2])
#ROOT_DIR = os.path.dirname(os.path.abspath('.'))

if __name__ == "__main__":
    print(ROOT_DIR)


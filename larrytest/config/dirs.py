#!/usr/bin/python

import os
import sys

if sys.platform.startswith('win'):
    ROOT_DIR = os.path.abspath('.')+"\\"
elif sys.plataform.startswith('linux'):
    ROOT_DIR = "/".join(os.path.abspath(__file__).split("/")[0:-2])
    
#ROOT_DIR = "/".join(os.path.abspath(__file__).split("/")[0:-2])
#ROOT_DIR = os.path.dirname(os.path.abspath('.'))
#ROOT_DIR = os.path.abspath('.')+"\\"
if __name__ == "__main__":
    print(ROOT_DIR)


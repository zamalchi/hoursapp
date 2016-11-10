#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

cd $parent_path

export PYTHONPATH=$parent_path/src/packages:PYTHONPATH

python2.7 ./run.py -p 8080

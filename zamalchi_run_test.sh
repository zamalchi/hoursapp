#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

cd $parent_path

./hours.py -p 8080 -s zamalchi@intranet.techsquare.com -m zamalchi@techsquare.com

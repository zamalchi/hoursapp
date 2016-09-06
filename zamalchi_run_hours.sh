#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

cd $parent_path

./hours.py -p 8080 -s zamalchi@intranet.techsquare.com -m sb@techsquare.com -l 172.16.1.254:40000

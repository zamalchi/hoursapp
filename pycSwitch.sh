#!/bin/bash

CENTOS=bottle.pyc.centos;
UBUNTU=bottle.pyc.ubuntu;

# run on CentOS
if [ -f ./${UBUNTU} ]; then
	mv bottle.pyc ${CENTOS};
	mv ${UBUNTU} bottle.pyc;
# run on Ubuntu
elif [ -f ./${CENTOS} ]; then
	mv bottle.pyc ${UBUNTU};
	mv ${CENTOS} bottle.pyc;
fi

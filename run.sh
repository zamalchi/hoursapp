#!/bin/bash

if [ -z ${1} ]; then
	let PORT=8080;
else
	let PORT=${1};
fi

/usr/bin/env python app.py -p ${PORT}
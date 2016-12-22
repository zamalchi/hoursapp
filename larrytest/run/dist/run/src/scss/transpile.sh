#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

scss_file="base.scss"
css_file="hours.css"

cd $parent_path

sass --watch ./${scss_file}:../../static/css/${css_file}
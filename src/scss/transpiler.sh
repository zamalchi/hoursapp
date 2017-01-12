#!/bin/bash

SCSS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=${SCSS_DIR}"/../.."

scss_file="${SCSS_DIR}/base.scss"
css_file="${ROOT_DIR}/static/css/main.css"

sass ${1} ${scss_file}:${css_file}
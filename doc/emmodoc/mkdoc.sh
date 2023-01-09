#!/bin/sh
# Bash script for generating documentation
set -e
set -x

python3 mkfigs.py

ontodoc --template=emmo.md --format=html emmo-inferred emmo.html
ontodoc --template=emmo.md emmo-inferred emmo.pdf

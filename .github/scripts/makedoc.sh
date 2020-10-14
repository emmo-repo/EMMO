#!/bin/sh

# Usage: makedoc.sh inferred version outdir
#
# Generates EMMO html and pdf documentation.
#
# Arguments:
#   - inferred: path to inferred ontology
#   - version: version to generate documentation for
#   - outdir: output directory
set -e

rootdir="$(git rev-parse --show-toplevel)"
scriptsdir="$rootdir/.github/scripts"

inferred=$1
version=$2
outdir=$3
[ $# -ne 3 ] && echo "Usage: makedoc.sh inferred version outdir" && exit 1

emmodir=$(python -c 'import os, emmo; print(os.path.dirname(emmo.__file__))')
[ -d "$emmodir/examples" ] && ex="$emmodir/examples" || \
        ex="$emmodir/../examples"
cd "$ex/emmodoc"


set -x
ontodoc --template=emmo.md --format=html -p variable=version:$version \
        "$inferred" "$outdir/emmo.html"

ontodoc --template=emmo.md -p variable=version:$version \
        "$inferred" "$outdir/emmo.pdf"

#!/bin/sh

# Usage: update_pages.sh [-N NAME] [-V VERSION] [-n -l -v]
#
# This is the main script that updates GitHub Pages.
#
# Options:
#   -N  Recreate version with given name.
#   -V  Recreate given version.
#   -n  Just update local copy of GitHub Pages, do not add and commit
#       changes.
#   -l  Just work on local copy of GitHub Pages.  Do not push changes.
#   -v  Verbose.  Print commands as they are executed.
set -e

rootdir="$(git rev-parse --show-toplevel)"
pagesdir="$rootdir/.github/pages"
scriptsdir="$rootdir/.github/scripts"

# Parse options
noadd=false
local=false
verbose=false
mvargs=
while getopts "N:V:nlv" arg; do
    case $arg in
        N)  mvargs="$mvargs -N $OPTARG";;
        V)  mvargs="$mvargs -V $OPTARG";;
        n)  noadd=true;;
        l)  local=true;;
        v)  verbose=true;;
    esac
done

# If verbose, print commands as they are executed
args=""
if $verbose; then
    args="-v"
    set -x
fi


# Initiate local GitHub Pages
"$scriptsdir/init_pages.sh"


# Make version sub-directories on GitHub Pages
"$scriptsdir/makeversions.sh" $args $mvargs


# Create index.html on GitHub Pages
"$scriptsdir/makeindex.sh" $args


# Commit changes and push to GitHub Pages
if ! $noadd; then
    echo
    cd "$pagesdir"
    git add --all
    [ -n "$(git status --porcelain -uno)" ] && \
        git commit -m 'Updated releasetable' && \
        git pull && \
        git push
    if ! $local; then
        git pull origin master && \
        git push origin master
    fi
fi

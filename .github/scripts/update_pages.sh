#!/bin/sh

# Usage: update_pages.sh [-g -l -v]
#
# This is the main script that updates GitHub Pages.
#
# Options:
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
while getopts "nlv" arg; do
    case $arg in
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
"$scriptsdir/makeversions.sh" $args


# Create index.html on GitHub Pages
"$scriptsdir/makeindex.sh"


# Commit changes and push to GitHub Pages
if ! $noadd; then
    echo
    cd "$pagesdir"
    git add --all
    git commit -m 'Update github pages'
        [ -n "$(git status --porcelain -uno)" ] && git commit -m 'Updated releasetable' && git push

    if ! $local; then
        git push origin master
    fi
fi

#!/bin/sh

# Usage: init_pages.sh
#
# Check out github pages under .github/pages if the directory does not
# already exists.
set -e

rootdir="$(git rev-parse --show-toplevel)"
pagesdir="$rootdir/.github/pages"
pagesurl=git@github.com:emmo-repo/emmo-repo.github.io.git

if [ ! -d "$pagesdir" ]; then
    set -x
    git clone $pagesurl "$pagesdir"
fi

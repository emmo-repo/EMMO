#!/bin/sh

# Usage: get_releases.sh
# Writes releases in directory '.github/releases' to stdout.

rootdir="$(git rev-parse --show-toplevel)"  # git root dir
releasesdir=$rootdir/.github/releases

[ -d $releasesdir/latest ] && echo latest
for tag in $(git tag); do
    [ -d $releasesdir/$tag ] && echo $tag
done

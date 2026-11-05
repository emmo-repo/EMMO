#!/bin/sh

# Make master branch on GitHub Pages an orphan branch
#
# This will save space.

set -e

rootdir="$(git rev-parse --show-toplevel)"

cd $rootdir/.github/pages
git checkout master
git pull origin master

# New orphan branch based on master
git checkout --orphan temp_orphan_branch
git commit -m "Make branch an orphan with current file state"

# Delete the old local branch pointer
git branch -D master

# Rename the temporary orphan branch to your original branch name
git branch -m master

git push origin master --force

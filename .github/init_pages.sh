#!/bin/sh

# Usage: init_pages.sh PAGES_DIR VERSION
# Initialise directory for given version on GitHub Pages.
#
# Arguments
#     PAGES_DIR: git root directory for GitHub Pages
#     VERSION: version number to initialise
#
# This script should be run from the checked out EMMO root directory.
#
set -e
set -x

pagesdir="$1"
version="$2"

versiondir="$pagesdir/versions/$version"
pagesurl=git@github.com:emmo-repo/emmo-repo.github.io.git


# Add directory for current version if it does not exists
if [ ! -d "$versiondir" ]; then
    mkdir -p "$versiondir"
fi

# Add/update README and LICENSE files
cp -f README.md LICENSE.md "$versiondir/."
cd "$versiondir"
git add README.md LICENSE.md
if [ -n "$(git status --porcelain -uno)" ]; then
    git commit -m 'Added README and LICENSE files'
    git push
fi
cd -

# Check for inferred ontology
if [ ! -f "$versiondir/emmo-inferred.owl" ]; then
    echo "Missing inferred ontology for EMMO $version."
    echo "Please do the following:"
    echo "  1. Clone $pagesurl"
    echo "  2. Open http://emmo.info/emmo/$version in Protege"
    echo "  3. Save inferred ontology to in the cloned GitHub Pages repo as:"
    echo "     versions/$version/emmo-inferred.owl"
    echo "  4. Add, commit and push inferred ontology to GitHub Pages"
    echo ""
    exit 1
fi

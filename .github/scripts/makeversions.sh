#!/bin/sh

# Usage: makeversions.sh [-r -v]
#
# Creates versions sub-directories in local copy of GitHub Pages.
#
# Options:
#   -r  Recreate existing sub-directories and their content.
#   -v  Verbose.  Print commands as they are executed.
set -e

rootdir="$(git rev-parse --show-toplevel)"
ghdir="$rootdir/.github"
pagesdir="$ghdir/pages"
scriptsdir="$ghdir/scripts"

$scriptsdir/init_pages.sh

# Parse options
recreate=false
verbose=false
while getopts "rv" arg; do
    case $arg in
        r)  recreate=true;;
        v)  verbose=true;;
    esac
done

# If verbose, print commands as they are executed
if $verbose; then
    set -x
fi

# Initiate local GitHub Pages
"$scriptsdir/init_pages.sh"


# Parse versions.sh and save html table rows in tmpfile
while read version name; do
    cd "$rootdir"
    $verbose && echo
    d="$pagesdir/versions/$version"
    if $recreate || [ ! -d "$d" ]; then
        mkdir -p "$d"
        cd "$rootdir"
        cp -f README.md LICENSE.md "$d/."
    fi

    # Generate one-file EMMO in turtle and owl (rfdxml) formats
    if $recreate || [ ! -d "$d/emmo.owl" ]; then
        echo "Converting EMMO from turtle to rdfxml"
        python "$scriptsdir/ontoconvert.py" -s "$rootdir/emmo.ttl" "$d/emmo.owl"
        python "$scriptsdir/ontoconvert.py" -s "$rootdir/emmo.ttl" "$d/emmo.ttl"
    fi

    # Generate inferred ontology
    if $recreate || [ ! -f "$d/emmo-inferred.owl" ]; then
        echo "Generate inferred ontology"
        "$scriptsdir/reason.sh" "$d/emmo.owl" "$d/emmo-inferred.owl"
        "$scriptsdir/fixinferred.sh" "$d/emmo-inferred.owl" $version
    fi

    # Generate documentation
    if $recreate || [ ! -f "$d/emmo.html" ]; then
        echo "Generate documentation"
        "$scriptsdir/makedoc.sh" "$d/emmo-inferred.owl" $version "$d"
    fi

    # Create symlinks
    cd "$pagesdir"
    if [ ! -z "$name" ]; then
        rm -f $name
        ln -sf versions/$version $name
    fi
done < "$ghdir/versions.txt"


# Make sure that we exit with non-zero
exit 0

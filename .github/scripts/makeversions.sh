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
remote=$(git remote -v | awk '{print $2; exit}')
ghdir="$rootdir/.github"
pagesdir="$ghdir/pages"
scriptsdir="$ghdir/scripts"
tmpdir=""

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


# Parse versions.sh and save html table rows in versions.txt
while read version name; do
    cd "$rootdir"
    $verbose && echo
    d="$pagesdir/versions/$version"
    if $recreate || [ ! -d "$d" ]; then
        mkdir -p "$d"
        cd "$rootdir"
        cp -f README.md LICENSE.md "$d/."
    fi

    # Generate single-file EMMO in turtle and owl (rfdxml) formats
    if $recreate || [ ! -f "$d/emmo.owl" ]; then
        echo "Generate single-file EMMO in turtle and owl (rfdxml) formats"
        if [ ! -d "$tmpdir" ]; then
            tmpdir="$(mktemp -d)"
            echo "tmpdir=$tmpdir"
            git clone $remote "$tmpdir"
        fi
        cd "$tmpdir"
        git fetch origin $version
        git checkout $version
        cd -
        if [ -f "$tmpdir/emmo.ttl" ]; then
            src="$tmpdir/emmo.ttl"
        elif [ -f "$tmpdir/emmo.owl" ]; then
            src="$tmpdir/emmo.owl"
        elif [ -f "$tmpdir/emmo/emmo.owl" ]; then
            src="$tmpdir/emmo/emmo.owl"
        else
            echo "missing source in EMMO $version" >&2; exit 1
        fi
        python "$scriptsdir/ontoconvert.py" -s "$src" "$d/emmo.owl"
        python "$scriptsdir/ontoconvert.py" -s "$src" "$d/emmo.ttl"
    fi

    # Generate inferred ontology
    if $recreate || [ ! -f "$d/emmo-inferred.owl" ]; then
        echo "Generate inferred ontology"
        "$scriptsdir/reason.sh" "$d/emmo.owl" "$d/emmo-inferred.owl"
        "$scriptsdir/fixinferred.sh" "$d/emmo-inferred.owl" $version
    fi
    if $recreate || [ ! -f "$d/emmo-inferred.ttl" ]; then
        if [ ! -d "$tmpdir" ]; then
            tmpdir="$(mktemp -d)"
        fi
        python "$scriptsdir/ontoconvert.py" -s \
               "$d/emmo-inferred.owl" "$tmpdir/emmo-inferred.ttl"
        # Hmm, for some reason floats are written like "1.0E-09.0" - strip
        # off the final ".0"
        sed 's/\([0-9][eE][+-][0-9]*\)\.[0-9]*\(.*\)/\1\2/' \
            "$tmpdir/emmo-inferred.ttl" > "$d/emmo-inferred.ttl"
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


# Clean up temporary directory
if [ -d "$tmpdir" ]; then
    rm -rf "$tmpdir"
fi


# Make sure that we exit with non-zero
exit 0

#!/bin/sh

# Usage: makeversions.sh [-N NAME] [-V VERSION] [-r -v]
#
# Creates versions sub-directories in local copy of GitHub Pages.
#
# Options:
#   -N  Recreate version with given name.
#   -V  Recreate given version.
#   -r  Recreate all existing sub-directories and their content.
#   -v  Verbose.  Print commands as they are executed.
#
# If the `version` argument is given,
set -e

rootdir="$(git rev-parse --show-toplevel)"
remote=$(git remote -v | awk '{print $2; exit}')
ghdir="$rootdir/.github"
pagesdir="$ghdir/pages"
scriptsdir="$ghdir/scripts"
tmpdir=""

$scriptsdir/init_pages.sh

# Parse options
recreate_version=""
recreate_name=""
recreate=false
verbose=false
while getopts "N:V:rv" arg; do
    case $arg in
        N)  recreate_name="$OPTARG";;
        V)  recreate_version="$OPTARG";;
        r)  recreate=true;;
        v)  verbose=true;;
    esac
done
shift $(($OPTIND -1))

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
    remake=$recreate
    [ -n "$recreate_version" ] && [ "$recreate_version" = "$version" ] && \
        remake=true
    [ -n "$recreate_name" ] && [ "$recreate_name" = "$name" ] && \
        remake=true
    if $remake || [ ! -d "$d" ]; then
        mkdir -p "$d"
        cd "$rootdir"
        cp -f README.md LICENSE.md "$d/."
    fi

    # Generate single-file EMMO in turtle and owl (rfdxml) formats
    if $remake || [ ! -f "$d/emmo.owl" ]; then
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
        ontoconvert "$src" "$d/emmo.owl" -s -a
        ontoconvert "$src" "$d/emmo.ttl" -s -a
    fi

    # Generate inferred ontology
    if $remake || [ ! -f "$d/emmo-inferred.owl" ]; then
        echo "Generate inferred ontology"
        ontoconvert "$d/emmo.owl" "$d/emmo-inferred.owl" \
                    -i -b http://emmo.info/emmo-inferred
    fi
    if $remake || [ ! -f "$d/emmo-inferred.ttl" ]; then
        ontoconvert "$d/emmo-inferred.owl" "$d/emmo-inferred.ttl"
    fi

    # Generate renamed ontology
    if $remake || [ ! -f "$d/emmo-renamed.owl" ]; then
        echo "Generate renamed ontology"
        ontoconvert "$d/emmo-inferred.owl" "$d/emmo-renamed.owl" \
                    -s -a -R -b http://emmo.info/emmo-renamed || true
    fi
    if $remake || [ ! -f "$d/emmo-renamed.ttl" ]; then
        ontoconvert "$d/emmo-inferred.owl" "$d/emmo-renamed.ttl" \
                    -s -a -R -b http://emmo.info/emmo-renamed || true
    fi

    # Generate documentation
    if $remake || [ ! -f "$d/emmo.html" ]; then
        echo "Generate documentation"
        "$scriptsdir/makedoc.sh" "$d/emmo-inferred.owl" $version "$d" \
            || true
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

#!/bin/sh

# Usage: makeindex.sh
#
# Parse $rootdir/.github/versions.txt and generate index.html file on
# github pages.
#
# Options:
#   -v  Verbose.  Print commands as they are executed.
set -e


# Configurations
pages_url="https://emmo-repo.github.io"
pages_versions_url="$pages_url/versions"
emmo_url="http://emmo.info/emmo"

rootdir="$(git rev-parse --show-toplevel)"
ghdir="$rootdir/.github"
tmpdir="$ghdir/tmp"
pagesdir="$ghdir/pages"

versionsfile="$ghdir/versions.txt"
tmpfile="$tmpdir/versions_html_table.txt"

# Parse options
while getopts "rv" arg; do
    case $arg in
        v)  set -x;;
    esac
done

[ -d "$tmpdir" ] || mkdir -p "$tmpdir"

# Initiate github pages
"$rootdir/.github/scripts/init_pages.sh"


# Parse versions.sh and save html table rows in tmpfile
tdlink() {
    href=$1
    cell=$2
    checkfile=$3
    echo "*** checkfile=$checkfile" >&2
    if [ -z "$checkfile" -o -f "$checkfile" ]; then
        echo "    <td><a href=\"$href\" target=\"_blank\">$cell</a></td>"
    else
        echo "    <td><a href=\"$href\" target=\"_blank\"></a></td>"
    fi
}
rm -rf "$tmpfile"
while read version name; do
    [ -z "$name" ] && name=$version
    iri=$emmo_url/$version
    d=$pages_url/versions/$version
    l=$pagesdir/versions/$version
    echo "  <tr>" >> "$tmpfile"
    echo "    <td>$name</td>" >> "$tmpfile"
    tdlink $iri                 $iri                          >> "$tmpfile"
    tdlink $d/emmo.owl          $version $l/emmo.owl          >> "$tmpfile"
    tdlink $d/emmo.ttl          $version $l/emmo.ttl          >> "$tmpfile"
    tdlink $d/emmo-inferred.owl $version $l/emmo-inferred.owl >> "$tmpfile"
    tdlink $d/emmo-inferred.ttl $version $l/emmo-inferred.ttl >> "$tmpfile"
    tdlink $d/emmo-renamed.owl  $version $l/emmo-renamed.owl  >> "$tmpfile"
    tdlink $d/emmo-renamed.ttl  $version $l/emmo-renamed.ttl  >> "$tmpfile"
    tdlink $d/emmo.html         $version $l/emmo.html         >> "$tmpfile"
    tdlink $d/emmo.pdf          $version $l/emmo.pdf          >> "$tmpfile"
    echo "  </tr>" >> "$tmpfile"
done < "$versionsfile"


# Generate index.html
sed -e "/\${versions}/ r $tmpfile" \
    -e 's/\${versions}//' \
    -e "s|\${date}|$(date +%F)|" \
    "$ghdir/pages-index.html.in" > "$pagesdir/index.html"

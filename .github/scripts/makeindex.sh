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
    echo "    <td><a href=\"$1\" target=\"_blank\">$2</a></td>"
}
rm -rf "$tmpfile"
while read version name; do
    [ -z "$name" ] && name=$version
    iri=$emmo_url/$version
    d=$pages_url/versions/$version
    inferred=$pages_url/versions/$version/emmo-inferred.owl
    inferred_iri=$iri/emmo-inferred
    html=$pages_url/versions/$version/emmo.html
    pdf=$pages_url/versions/$version/emmo.pdf
    echo "  <tr>" >> "$tmpfile"
    echo "    <td>$name</td>" >> "$tmpfile"
    tdlink $iri $iri >> "$tmpfile"
    tdlink $d/emmo.owl $version >> "$tmpfile"
    tdlink $d/emmo.ttl $version >> "$tmpfile"
    tdlink $inferred $inferred_iri >> "$tmpfile"
    tdlink $d/emmo-inferred.ttl $version >> "$tmpfile"
    tdlink $html $version >> "$tmpfile"
    tdlink $pdf $version >> "$tmpfile"
    echo "  </tr>" >> "$tmpfile"
done < "$versionsfile"


# Generate index.html
sed -e "/\${versions}/ r $tmpfile" \
    -e 's/\${versions}//' \
    -e "s|\${date}|$(date +%F)|" \
    "$ghdir/pages-index.html.in" > "$pagesdir/index.html"

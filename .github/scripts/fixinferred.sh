#!/bin/sh

# Usage: fixinferred.sh filename
#
# Fix inferred ontology modifying the target file in-place.
# It is safe to run this script multiple times on the same file.
set -e

rootdir="$(git rev-parse --show-toplevel)"
ghdir="$rootdir/.github"
tmpfile="$ghdir/tmp/fixinferred.owl"



filename=$1
[ $# -ne 1 ] && echo "Usage: fixinferred.sh filename" && exit 1


# Do nothing if filename is already fixed
grep -q "fixinferred.sh" "$filename" && exit 0


# Create temporary file
mkdir -p $(dirname "$tmpfile")
sed -e 's|</rdf:RDF>||p' "$filename" > "$tmpfile"
cat <<EOF >> "$tmpfile"

    <!-- Fixes by fixinferred.sh -->

EOF

# Add annotation superproperties
# The table below associates annotation property IRIs with their superproperties
while read iri superprop; do
    [ -z "$iri" ] && continue
    cat <<EOF >> "$tmpfile"
    <!-- $iri -->
    <owl:AnnotationProperty rdf:about="$iri">
        <rdfs:subPropertyOf rdf:resource="$superprop"/>
    </owl:AnnotationProperty>

EOF
done <<EOF
http://www.w3.org/2004/02/skos/core#prefLabel    http://www.w3.org/2000/01/rdf-schema#label
http://www.w3.org/2004/02/skos/core#altLabel     http://www.w3.org/2000/01/rdf-schema#label
http://www.w3.org/2004/02/skos/core#hiddenLabel  http://www.w3.org/2000/01/rdf-schema#label

http://emmo.info/emmo/top/annotations#EMMO_70fe84ff_99b6_4206_a9fc_9a8931836d84 http://www.w3.org/2000/01/rdf-schema#comment
http://emmo.info/emmo/top/annotations#EMMO_967080e5_2f42_4eb2_a3a9_c58143e835f9 http://www.w3.org/2000/01/rdf-schema#comment
http://emmo.info/emmo/top/annotations#EMMO_b432d2d5_25f4_4165_99c5_5935a7763c1a http://www.w3.org/2000/01/rdf-schema#comment
http://emmo.info/emmo/middle/isq#EMMO_de178b12_5d35_4bca_8efa_a4193162571d      http://www.w3.org/2000/01/rdf-schema#comment

http://emmo.info/emmo/top/annotations#EMMO_b306ae38_938e_48fe_83e9_6141e08b596f http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_6dd685dd_1895_46e4_b227_be9f7d643c25 http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_50c298c2_55a2_4068_b3ac_4e948c33181f http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_8de5d5bf_db1c_40ac_b698_095ba3b18578 http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_fe015383_afb3_44a6_ae86_043628697aa2 http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_e55f2d7c_9893_48cd_b4a4_fdf38253bd20 http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_1f1b164d_ec6a_4faa_8d5e_88bda62316cc http://www.w3.org/2000/01/rdf-schema#seeAlso
http://emmo.info/emmo/top/annotations#EMMO_c84c6752_6d64_48cc_9500_e54a3c34898d http://www.w3.org/2000/01/rdf-schema#seeAlso
EOF

echo "</rdf:RDF>" >> "$tmpfile"


# Overwrite filename
cat "$tmpfile" > "$filename"

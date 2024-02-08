#!/usr/bin/env bash

# Author: Otello M. Roscioni, Goldbeck Consulting LTD, UK.
# 8 February 2024

# Convert the IRI with the format EMMO_hex-hex-hex-hex-hex to the standard format EMMO_hex_hex_hex_hex_hex.
for i in $(find . -name "*ttl" -exec grep -il ':EMMO_[0-9a-f]*-[0-9a-f]*-[0-9a-f]*-[0-9a-f]*-[0-9a-f]*' '{}' \;); do
 sed -i -E 's/EMMO_([0-9a-f]+)-([0-9a-f]+)-([0-9a-f]+)-([0-9a-f]+)-([0-9a-f]+)/EMMO_\1_\2_\3_\4_\5/g' "$i";
done

# Convert the IRI without the leading prefix to the standard format EMMO_hex_hex_hex_hex_hex.
for i in $(find . -name "*ttl" -exec grep -il ':[0-9a-f]*_[0-9a-f]*_[0-9a-f]*_[0-9a-f]*_[0-9a-f]*' '{}' \;); do
 sed -i -E 's/:([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)/:EMMO_\1_\2_\3_\4_\5/g' "$i";
done

# Convert the IRI with the format <http://emmo.info/emmo#hex_hex_hex_hex_hex> to the standard format EMMO_hex_hex_hex_hex_hex.
for i in $(find . -name "*ttl" -exec grep -il '<http://emmo.info/emmo#[0-9a-f]*_[0-9a-f]*_[0-9a-f]*_[0-9a-f]*_[0-9a-f]*>' '{}' \;); do
 sed -i -E 's/<http:\/\/emmo.info\/emmo#([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)>/:EMMO_\1_\2_\3_\4_\5/g' "$i";
done

# Change triples double-quotes (""") to single ones (").
find . -name "*ttl" -exec sed -i 's/"""/"/g' '{}' \;

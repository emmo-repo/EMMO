for i in $(find . -name "*ttl");
do
  # Change triples double-quotes (""") to single ones (").
  sed -i 's/"""/"/g' "$i"
  # Convert the IRI with the format EMMO_hex-hex-hex-hex-hex.
  sed -i -E 's/EMMO_([0-9a-f]+)-([0-9a-f]+)-([0-9a-f]+)-([0-9a-f]+)-([0-9a-f]+)/EMMO_\1_\2_\3_\4_\5/g' "$i";
  # Convert the IRI without the EMMO_ prefix.
  sed -i -E 's/:([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)/:EMMO_\1_\2_\3_\4_\5/g' "$i";
  # Convert the IRI with the format <http://emmo.info/emmo#hex_hex_hex_hex_hex>.
  sed -i -E 's/<http:\/\/emmo.info\/emmo#([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)_([0-9a-f]+)>/:EMMO_\1_\2_\3_\4_\5/g' "$i";
done


#!/bin/sh

mkdir -p "$PWD/output"

src=$1
dest=$2
options=$3

# Make src and dest absolute
isabs() {
    case "$1" in
        /*)     true;;   # absolute
        *://*)  true;;   # url
        *)      false;;  # relative
    esac
}
isabs "$src" || src="$PWD/$src"
isabs "$dest" || dest="$PWD/$dest"


indir=$(dirname "$src")
outdir=$(dirname "$dest")/output

infile=$(basename "$src")
outfile=$(basename "$dest")

# Create temporary directory
tmp=$(mktemp -d)
mkdir -p $tmp

docker run \
       --rm \
       --mount "type=bind,src=$indir,dst=/mnt/input,readonly=true" \
       --mount "type=bind,src=$tmp,dst=/mnt/output,readonly=false" \
       --user $(id -u):$(id -g) \
       jesperfriis/totiplusplus:v0.1 \
       /home/user/totiplusplus/totiplusplus.sh \
       /mnt/input/"$infile" /mnt/output/"$outfile" $options

mv $tmp/$outfile $dest
rmdir $tmp

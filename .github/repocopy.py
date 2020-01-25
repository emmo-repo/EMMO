#!/usr/bin/env python3
"""Copies source directory tree to destination directory tree, while
updating links in all owl-files on the way.
"""
import os
import sys
import re
import shutil
import argparse


def copyowl(src, dest, name, base='http://emmo.info'):
    """Write content of owlfile `src` to `dest` with all occurences of
    `base` replaced with "`base`/`name`"."""
    with open(src, 'rt') as f:
        buf = f.read()
    with open(dest, 'wt') as f:
        f.write(buf.replace(base, base + '/' + name))


def walk(srcdir, destdir):
    """Copies `srcdir` to `destdir`, updating all owl-files on the way."""
    srcdir = os.path.abspath(srcdir)
    destdir = os.path.abspath(destdir)
    name = os.path.basename(destdir)
    for dirpath, dirnames, filenames in os.walk(srcdir):
        dirpath = os.path.relpath(dirpath, srcdir)
        if '.git' not in dirpath:
            fromdir = os.path.join(srcdir, dirpath)
            todir = os.path.join(destdir, dirpath)
            os.makedirs(todir, exist_ok=True)
            for filename in filenames:
                src = os.path.join(fromdir, filename)
                dest = os.path.join(todir, filename)
                if os.path.splitext(dest)[1] == '.owl':
                    copyowl(src, dest, name)
                elif not dest.endswith('~') and not filename.startswith('.'):
                    shutil.copy(src, dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('srcdir', help='Source directory.')
    parser.add_argument('destdir', help='Destination directory.')
    args = parser.parse_args()
    walk(args.srcdir, args.destdir)


if __name__ == '__main__':
    main()

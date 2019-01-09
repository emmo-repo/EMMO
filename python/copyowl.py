#!/usr/bin/env python
"""Copies owl files from root owl/ directory to the python/emmo/ directory.
Import paths are fixed on the way.
"""
import os
import shutil

thisdir = os.path.abspath(os.path.dirname(__file__))


def copyowl(destdir=None):
    """Copies owl files from root owl/ directory to the `destdir` directory.
    The default is "python/emmo/owl/".
    Import paths are fixed on the way."""
    rootdir = os.path.normpath(os.path.join(thisdir, '..'))
    #rootdir = os.path.dirname(thisdir)
    owldir = os.path.join(rootdir, 'owl')
    if destdir is None:
        destdir = os.path.join(rootdir, 'python', 'emmo', 'owl')

    print('Copying owl files from `owldir` to `destdir`:')
    print('  owldir:', owldir)
    print('  destdir:', destdir)

    # Make sure that destdir exists
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    # Copy (and fix) emmo.owl
    lines = []
    with open(os.path.join(owldir, 'emmo.owl'), 'r') as f:
        for line in f:
            if line.startswith('  <owl:imports rdf:resource='
                               '"http://emmc.info/emmo-material"/>'):
                lines.append(line.replace(
                    'http://emmc.info/emmo-material',
                    'file://' + destdir + os.sep + 'emmo-material.owl'))
            else:
                lines.append(line)

    with open(os.path.join(destdir, 'emmo.owl'), 'w') as f:
        f.writelines(lines)

    # Copy emmo-material.owl
    shutil.copy(os.path.join(owldir, 'emmo-material.owl'),
                os.path.join(destdir, 'emmo-material.owl'))

    # Copy emmo-usercase.owl
    shutil.copy(os.path.join(owldir, 'emmo-usercase.owl'),
                os.path.join(destdir, 'emmo-usercase.owl'))



if __name__ == '__main__':
    copyowl()

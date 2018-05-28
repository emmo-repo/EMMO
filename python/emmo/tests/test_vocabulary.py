#!/usr/bin/env python3
import sys
import os
import subprocess

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology


emmo = get_ontology('emmo.owl')
emmo.load()
#emmo.sync_reasoner()


# Vocabulary before reasoning
with open('emmo-noreason.html', 'w') as f:
    f.write(emmo.get_vocabulary())

emmo.sync_reasoner()

# Vocabulary after reasoning
with open('emmo.html', 'w') as f:
    f.write(emmo.get_vocabulary())

# Markdown vocabulary converted to html with pandoc
with open('emmodoc.md', 'w') as f:
    f.write(emmo.get_vocabulary(template='markdown') + '\n')
subprocess.call(['pandoc', '-s', '--toc', 'emmodoc.md', '-o', 'emmodoc.html'])

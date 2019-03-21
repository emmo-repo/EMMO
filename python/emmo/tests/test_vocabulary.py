#!/usr/bin/env python3
import sys
import os
import subprocess
import time

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology


emmo = get_ontology()
emmo.load()

#emmo.sync_reasoner()

# Vocabulary after reasoning
with open('emmo.html', 'w') as f:
    f.write(emmo.get_vocabulary())

# Markdown vocabulary converted to html with pandoc
with open('emmodoc.md', 'w') as f:
    f.write(emmo.get_vocabulary(template='markdown') + '\n')
subtitle = 'Generated from <a href="%s">%s</a>' % (emmo.base_iri, emmo.base_iri)
subprocess.call(['pandoc', 'emmodoc.md', 'emmodoc-meta.yaml',
                 '--standalone', '--self-contained', '--toc', '--toc-depth=2',
                 '--variable=date:%s' % time.strftime('%B %d, %Y'),
                 '--variable=subtitle:%s' % subtitle,
                 '--to=html5',
                 '--css=emmodoc.css',
                 '--template=emmodoc-template.html',
                 '--output=emmodoc.html'])


# Markdown vocabulary converted to pdf with pandoc
subtitle = r'Generated from \url{%s}' % (emmo.base_iri, )
subprocess.call(['pandoc', 'emmodoc.md', 'emmodoc-meta.yaml',
                 '--standalone', '--self-contained', '--toc', '--toc-depth=2',
                 '--variable=date:%s' % time.strftime('%B %d, %Y'),
                 '--variable=subtitle:%s' % subtitle,
                 '--variable=urlcolor:blue',
                 '--variable=toccolor:blue',
                 '--variable=geometry:margin=2cm',
                 '--variable=author:Europeean Materials Modelling Council',
                 '--from=markdown+auto_identifiers',
                 '--output=emmodoc.pdf'])

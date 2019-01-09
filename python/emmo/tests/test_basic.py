#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

emmo = get_ontology('emmo.owl')
emmo.load()
emmo.sync_reasoner()


H = emmo.atom(label='H')
e = emmo.electron(label='e')
p = emmo.proton(label='p')
v = emmo.vacuum(label='v')

H.has_spatial_direct_part = [e, p, v]


print()
print("atom")
print([s for s in dir(emmo.atom) if not s.startswith('_')])


print()
print("H")
print([s for s in dir(H) if not s.startswith('_')])



#from emmo import relations

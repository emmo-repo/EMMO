# -*- coding: utf-8 -*-
"""
Module that appends the directory containing the corrected version of EMMO to
the ontology search path.
"""
import os

import owlready2


thisdir = os.path.abspath(os.path.realpath((os.path.dirname(__file__))))
owldir = os.path.abspath(os.path.join(thisdir, '..', '..', 'emmo','rdfxml'))

if not os.path.exists(os.path.join(owldir, 'emmo.owl')):
    print('File does not exists: ', os.path.join(owldir, 'emmo.owl'))
    print('You should install it by running the `copyowl.py` script')
    print('in the python root directory.')
    exit(1)

owlready2.onto_path.append(owldir)

# -*- coding: utf-8 -*-


# Ensure correct Python version
import sys
if sys.version_info < (3, 4):
    raise RuntimeError('emmo requires Python 3.4 or later')


# Ensure emmo is imported before owlready2...
if 'owlready2' in sys.modules.keys():
    raise RuntimeError('emmo must be imported before owlready2')


# Import get_ontology(), which is our main entry point
from .ontology import get_ontology

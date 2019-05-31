#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 1 - Generate metadata from ontology
----------------------------------------
This step takes the ontology from the vertical case and generates
metadata from it.

Here we use DLite as metadata framework, which is a SOFT
implementation in C.  Other frameworks, like CUDS, could equally well
have been used, but the metadata structure would have been different.

This generator maps OWL classes to dlite metadata entities which are
placed into a collection.  OWL class properties are mapped into
relations between the entities in the collection. The only relations
that are treated especially are `has_property` and `is_property_for`,
that are mapped into properties of the generated metadata entities.

The generated  metadata is finally serialised into a JSON file.
"""
import os

from emmo import get_ontology
from emmo2meta import EMMO2Meta


# Load our ontology from the vertical case
ontopath = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'vertical', 'case_ontology.owl'))
onto = get_ontology(ontopath)
onto.load()


# hmm, the base iri has cnanged... - bug in owlready2?
onto.base_iri = 'http://www.emmc.info/emmc-csa/demo#'


# Generate metadata and store it in a JSON file
items = list(onto.classes()) + [onto['e-bonded_atom']]
e = EMMO2Meta(ontology=onto, classes=items, collid='case_ontology')
e.save('json', 'case_metadata.json', 'mode=w')

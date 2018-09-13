#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology


emmo = get_ontology('emmo.owl')
emmo.load()

graph = emmo.get_dot_graph(relations=True, style='uml')
graph.write_pdf('graph-noreason.pdf')

emmo.sync_reasoner()

graph = emmo.get_dot_graph(relations=True, style='uml')
graph.write_pdf('graph.pdf')

entity_graph = emmo.get_dot_graph('entity')
entity_graph.write_pdf('entity_graph.pdf')

property_graph = emmo.get_dot_graph('property')
property_graph.write_pdf('property_graph.pdf')

relations_graph = emmo.get_dot_relations_graph(relations=True)
relations_graph.write_pdf('relation_graph.pdf')

#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
import emmo


onto = emmo.get_ontology('emmo.owl')
onto.load()
onto.sync_reasoner()


entity_graph = onto.get_dot_graph('entity')
entity_graph.write_pdf('entity_graph.pdf')

property_graph = onto.get_dot_graph('property', rankdir='RL')
property_graph.write_pdf('property_graph.pdf')

relations_graph = onto.get_dot_relations_graph(rankdir='RL')
relations_graph.write_pdf('relation_graph.pdf')

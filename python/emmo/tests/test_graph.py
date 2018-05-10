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


abstract_graph = onto.get_dot_graph('abstract')
abstract_graph.write_pdf('abstract_graph.pdf')


if False:
    entity_graph = onto.get_dot_graph('entity')
    entity_graph.write_pdf('entity_graph.pdf')

    material_entity_graph = onto.get_dot_graph('material_entity', rankdir='RL')
    material_entity_graph.write_pdf('material_entity_graph.pdf')

    quality_graph = onto.get_dot_graph('quality', rankdir='RL')
    quality_graph.write_pdf('quality_graph.pdf')

    graph = onto.get_dot_graph('has_continuant_part', rankdir='RL')
    graph.write_pdf('has_continuant_part.pdf')


    relations_graph = onto.get_dot_relations_graph(rankdir='RL')
    relations_graph.write_pdf('relations.pdf')

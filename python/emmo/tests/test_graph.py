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
graph.write_svg('graph-noreason.svg')

emmo.sync_reasoner()

graph = emmo.get_dot_graph(relations=True, style='uml')
graph.write_pdf('graph.pdf')
graph.write_svg('graph.svg')

entity_graph = emmo.get_dot_graph('entity')
entity_graph.write_pdf('entity_graph.pdf')
entity_graph.write_svg('entity_graph.svg')

substrate_graph = emmo.get_dot_graph('substrate', relations=True,
                                     leafs=('spacetime'), parents='item',
                                     style='uml')
substrate_graph.write_pdf('substrate_graph.pdf')
substrate_graph.write_svg('substrate_graph.svg')

property_graph = emmo.get_dot_graph('property')
property_graph.write_pdf('property_graph.pdf')

#relations_graph = emmo.get_dot_relations_graph(relations=True)
#relations_graph.write_pdf('relation_graph.pdf')

relations_graph = emmo.get_dot_relations_graph()
relations_graph.write_pdf('relation_graph.pdf')



#material = get_ontology('emmo-material.owl')
#material.name = 'material'
#material.load()
#material.sync_reasoner()
#material_graph = material.get_dot_graph()
#material_graph.write_pdf('material.pdf')

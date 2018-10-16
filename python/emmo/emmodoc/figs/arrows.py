#!/usr/bin/env python3
import pydot

def plot(name, **kw):

    graph = pydot.Dot(graph_type='digraph', rankdir='LR',
                      bgcolor='transparent')

    A = pydot.Node('A', shape='point', width=0)
    B = pydot.Node('B', shape='point', width=0)
    graph.add_node(A)
    graph.add_node(B)

    E = pydot.Edge(A, B, **kw)
    graph.add_edge(E)

    graph.write_png(name + '.png')
    #graph.write_svg(name + '.svg')
    #graph.write_pdf(name + '.pdf')


#plot('arrow-normal.png')
#plot('arrow-composition.png', arrowtail='odiamond', dir='back')
#plot('arrow-aggregation.png', arrowtail='diamond', dir='back')
#plot('arrow-inheritance.png', arrowhead='empty')
#plot('arrow-dependency.png', style='dashed', arrowhead='vee')
#plot('arrow-association.png', arrowhead='none')


plot('arrow-is_a', arrowhead='empty')
plot('arrow-equivalent_to', color='green', arrowhead='none')
plot('arrow-disjoint_with', color='red', arrowhead='none')
plot('arrow-inverse_of', color='orange', arrowhead='none')
plot('arrow-relation', color='blue', arrowtail='diamond', dir='back')

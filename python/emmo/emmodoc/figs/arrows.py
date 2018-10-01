#!/usr/bin/env python3
import pydot

def plot(filename, **kw):

    graph = pydot.Dot(graph_type='digraph', rankdir='LR')

    A = pydot.Node('A', shape='point', width=0)
    B = pydot.Node('B', shape='point', width=0)
    graph.add_node(A)
    graph.add_node(B)

    E = pydot.Edge(A, B, **kw)
    graph.add_edge(E)

    graph.write_png(filename)


#plot('arrow-normal.png')
#plot('arrow-composition.png', arrowtail='odiamond', dir='back')
#plot('arrow-aggregation.png', arrowtail='diamond', dir='back')
#plot('arrow-inheritance.png', arrowhead='empty')
#plot('arrow-dependency.png', style='dashed', arrowhead='vee')
#plot('arrow-association.png', arrowhead='none')


plot('arrow-is_a.png', arrowhead='empty')
plot('arrow-equivalent_to.png', color='green', arrowhead='none')
plot('arrow-disjoint_with.png', color='red', arrowhead='none')
plot('arrow-inverse_of.png', color='orange', arrowhead='none')
plot('arrow-relation.png', color='blue', arrowtail='diamond', dir='back')

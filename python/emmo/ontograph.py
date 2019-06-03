# -*- coding: utf-8 -*-
"""
A module adding graphing functionality to emmo.ontology
"""
#
# This module was written before I had a good understanding of DL.
# Should be simplified and improved:
#   - Rewrite OntoGraph to be a standalone class instead of as an mixin
#     for Ontology.
#   - Make it possible to have different styles for different types of
#     relations (by default differentiate between is_a, has_part,
#     has_subdimension, has_sign and has_member).
#   - Factor out methods for finding node trees (may go into Ontology).
#   - Factor out methods to finding relation triplets ``(node1, relation,
#     node2)`` (may go into Ontology).
#   - Consider to switch to graphviz Python package since it seems to have
#     very useful interface to Jupyter Notebook and Qt Console integration,
#     see https://pypi.org/project/graphviz/.
#
import itertools
import warnings

import owlready2

from .utils import asstring
import emmo


class OntoGraph:
    """A mixin class used by emmo.ontology.Ontology that adds
    functionality for generating graph representations of the ontology.
    """
    _default_style = {
        'graph': {'graph_type': 'digraph', 'rankdir': 'RL', 'fontsize': 8,
                  #'fontname': 'Bitstream Vera Sans', 'splines': 'ortho',
                  #'engine': 'neato',
            },
        'class': {
            'style': 'filled',
            'fillcolor': '#ffffcc',
        },
        'defined_class': {
            'style': 'filled',
            'fillcolor': '#ffc880',
        },
        'individuals': {},
        'is_a': {'arrowhead': 'empty'},
        'equivalent_to': {'color': 'green3', },
        'disjoint_with': {'color': 'red', },
        'inverse_of': {'color': 'orange', },
        #'other': {'color': 'blue', },
        'relations': {
            'enclosing': {'color': 'red', 'arrowtail': 'diamond',
                          'dir': 'back'},
            'has_subdimension': {'color': 'red', 'arrowtail': 'diamond',
                                 'dir': 'back', 'style': 'dashed'},
            'has_sign': {'color': 'blue', 'style': 'dotted'},
            'has_property': {'color': 'blue'},
            'has_unit': {'color': 'magenta'},
            'has_type': {'color': 'forestgreen'},
        },
        'other': {'color': 'olivedrab'},
        }

    _uml_style = {
        'graph': {'graph_type': 'digraph', 'rankdir': 'RL', 'fontsize': 8,
              #'splines': 'ortho',
            },
        'class': {
            #'shape': 'record',
            'shape': 'box',
            'fontname': 'Bitstream Vera Sans',
            'style': 'filled',
            'fillcolor': '#ffffe0',
        },
        'defined_class': {
            #'shape': 'record',
            'shape': 'box',
            'fontname': 'Bitstream Vera Sans',
            'style': 'filled',
            'fillcolor': '#ffc880',
        },
        'individuals': {},
        'is_a': {'arrowhead': 'empty'},
        'equivalent_to': {'color': 'green3'},
        'disjoint_with': {'color': 'red', 'arrowhead': 'none'},
        'inverse_of': {'color': 'orange', 'arrowhead': 'none'},
        #'other': {'color': 'blue', 'arrowtail': 'diamond', 'dir': 'back'},
        'relations': {
            'enclosing': {'color': 'red', 'arrowtail': 'diamond',
                          'dir': 'back'},
            'has_subdimension': {'color': 'red', 'arrowtail': 'diamond',
                                 'dir': 'back', 'style': 'dashed'},
            'has_sign': {'color': 'blue', 'style': 'dotted'},
            'has_property': {'color': 'blue'},
            'has_unit': {'color': 'magenta'},
            'has_type': {'color': 'forestgreen'},
        },
        'other': {'color': 'blue'},
    }


    def get_dot_graph(self, root=None, graph=None, relations='is_a',
                      leafs=None, parents=False, style=None,
                      edgelabels=True, constraint=False):
        """Returns a pydot graph object for visualising the ontology.

        Parameters
        ----------
        root : None | string | owlready2.ThingClass instance
            Name or owlready2 entity of root node to plot subgraph
            below.  If `root` is None, all classes will be included in the
            subgraph.
        graph : None | pydot.Dot instance
            Pydot graph object to plot into.  If None, a new graph object
            is created using the keyword arguments.
        relations : True | str | sequence
            Sequence of relations to visualise.  If True, all relations are
            included.
        leafs : None | sequence
            A sequence of leaf node names for generating sub-graphs.
        parents : bool | str
            Whether to include parent nodes.  If `parents` is a string,
            only parent nodes down to the given name will included.
        style : None | dict | "uml"
            A dict mapping the name of the different graphical elements
            to dicts of pydot style settings. Supported graphical elements
            include:
              - graph : overall settings pydot graph
              - class : nodes for classes
              - individual : nodes for invididuals
              - is_a : edges for is_a relations
              - equivalent_to : edges for equivalent_to relations
              - disjoint_with : edges for disjoint_with relations
              - inverse_of : edges for inverse_of relations
              - relations : with relation names
                  XXX
              - other : edges for other relations and restrictions
            If style is None, a very simple default style is used.
            Some pre-defined styles can be selected by name (currently
            only "uml").
        edgelabels : bool | dict
            Whether to add labels to the edges of the generated graph.
            It is also possible to provide a dict mapping the
            full labels (with cardinality stripped off for restrictions)
            to some abbriviations.
        constraint : None | bool

        Note: This method requires pydot.
        """
        import pydot
        from .ontology import NoSuchLabelError

        if style is None or style == 'default':
            style = self._default_style
        elif style == 'uml':
            style = self._uml_style

        graph = self._get_dot_graph(root=root, graph=graph,
                                    relations=relations, leafs=leafs,
                                    style=style, edgelabels=edgelabels)

        # Add parents
        if parents and root:
            r = self.get_by_label(root) if isinstance(root, str) else root
            while True:
                parent = r.is_a.first()
                if (parent is None or parent is owlready2.Thing):
                    break
                label = parent.label.first()
                if self.is_defined(label):
                    node = pydot.Node(label, **style.get('defined_class', {}))
                    # If label contains a hyphen, the node name will
                    # be quoted (bug in pydot?).  To work around, set
                    # the name explicitly...
                    node.set_name(label)
                else:
                    node = pydot.Node(label, **style.get('class', {}))
                    node.set_name(label)
                graph.add_node(node)
                if relations is True or 'is_a' in relations:
                    kw = style.get('is_a', {}).copy()
                    if isinstance(edgelabels, dict):
                        kw['label'] = edgelabels.get('is_a', 'is_a')
                    elif edgelabels:
                        kw['label'] = 'is_a'
                    rootnode = graph.get_node(r.label.first())[0]
                    edge = pydot.Edge(rootnode, node, **kw)
                    graph.add_edge(edge)
                if (isinstance(parents, str) and label == parents):
                    break
                r = parent

        # Add edges
        for node in graph.get_nodes():
            try:
                entity = self.get_by_label(node.get_name())
            except (KeyError, NoSuchLabelError):
                continue
            # Add is_a edges
            targets = [e for e in entity.is_a if not isinstance(e, (
                owlready2.ThingClass, owlready2.ObjectPropertyClass,
                owlready2.PropertyClass))]

            self._get_dot_add_edges(
                graph, entity, targets, 'relations',
                relations,
                #style=style.get('relations', style.get('other', {})),
                style=style.get('other', {}),
                edgelabels=edgelabels,
                constraint=constraint,
            )

            # Add equivalent_to edges
            if relations is True or 'equivalent_to' in relations:
                self._get_dot_add_edges(
                    graph, entity, entity.equivalent_to, 'equivalent_to',
                    relations, style.get('equivalent_to', {}),
                    edgelabels=edgelabels,
                    constraint=constraint,
                )

            # disjoint_with
            if hasattr(entity, 'disjoints') and (
                    relations is True or 'disjoint_with' in relations):
                self._get_dot_add_edges(
                    graph, entity, entity.disjoints(), 'disjoint_with',
                    relations, style.get('disjoint_with', {}),
                    edgelabels=edgelabels,
                    constraint=constraint,
                )

            # Add inverse_of
            if (hasattr(entity, 'inverse_property') and
                (relations is True or 'inverse_of' in relations) and
                entity.inverse_property is not None):
                self._get_dot_add_edges(
                    graph, entity, [entity.inverse_property], 'inverse_of',
                    relations, style.get('inverse_of', {}),
                    edgelabels=edgelabels,
                    constraint=constraint,
                )

        return graph

    def _get_dot_add_edges(self, graph, entity, targets, relation,
                           relations, style, edgelabels=True,
                           constraint=None):
        """Adds edges to `graph` for relations between `entity` and all
        members in `targets`.  `style` is a dict with options to pydot.Edge().
        """
        import pydot

        nodes = graph.get_node(entity.label.first())
        if not nodes:
            return
        node = nodes[0]

        for e in targets:
            s = asstring(e)
            if isinstance(e, owlready2.ThingClass):
                pass
            elif isinstance(e, (owlready2.ObjectPropertyClass,
                                owlready2.PropertyClass)):
                label = e.label.first()
                nodes = graph.get_node(label)
                if nodes:
                    kw = style.copy()
                    if isinstance(edgelabels, dict):
                        kw['label'] = edgelabels.get(label, label)
                    elif edgelabels:
                        kw['label'] = label
                    edge = pydot.Edge(node, nodes[0], **kw)
                    if constraint is not None:
                        edge.set_constraint(constraint)
                    graph.add_edge(edge)
            elif isinstance(e, owlready2.Restriction):
                rname = e.property.label.first()
                rtype = owlready2.class_construct._restriction_type_2_label[
                    e.type]

                if relations is True or rname in relations:
                    if hasattr(e.value, 'label'):
                        vname = e.value.label.first()
                    else:
                        vname = repr(e.value)
                    others = graph.get_node(vname)

                    # Only proceede if there is only one node named `vname`
                    # and an edge to that node does not already exists
                    if (len(others) == 1 and
                        (node.get_name(), vname) not in
                        graph.obj_dict['edges'].keys()):
                        other = others[0]
                    else:
                        continue

                    if rtype in ('min', 'max', 'exactly'):
                        label = '%s %s %d' % (rname, rtype, e.cardinality)
                    else:
                        label = '%s %s' % (rname, rtype)

                    kw = style.copy()
                    if isinstance(edgelabels, dict):
                        slabel = '%s %s' % (rname, rtype)
                        kw['label'] = edgelabels.get(slabel, label) + '   '
                    elif edgelabels:
                        kw['label'] = label + '   '  # Add some extra space

                    edge = pydot.Edge(node, other, **kw)
                    if constraint is not None:
                        edge.set_constraint(constraint)
                    graph.add_edge(edge)

            elif hasattr(self, '_verbose') and self._verbose:
                print('* get_dot_graph() * Ignoring: '
                      '%s %s %s' % (node.get_name(), relation, s))



    def _get_dot_graph(self, root=None, graph=None, relations='is_a',
                       leafs=None, style=None, visited=None,
                       edgelabels=True):
        """Help method. See get_dot_graph(). `visited` is used to filter
        out circular dependencies.
        """
        import pydot

        if graph is None:
            graph = pydot.Dot(**style.get('graph', {}))

        if relations is True:
            relations = ['is_a'] + list(self.get_relations())
        elif isinstance(relations, str):
            relations = [relations]
        relations = set(r if isinstance(r, str) else
                        r.label.first() if len(r.label) == 1 else r.name
                        for r in relations)

        if visited is None:
            visited = set()

        if root is None:
            for root in self.get_root_classes():
                self._get_dot_graph(root=root, graph=graph,
                                    relations=relations, leafs=leafs,
                                    style=style, visited=visited,
                                    edgelabels=edgelabels)
            return graph
        elif isinstance(root, (list, tuple, set)):
            for r in root:
                self._get_dot_graph(root=r, graph=graph,
                                    relations=relations, leafs=leafs,
                                    style=style, visited=visited,
                                    edgelabels=edgelabels)
            return graph
        elif isinstance(root, str):
            root = self.get_by_label(root)

        if root in visited:
            if hasattr(self, '_verbose') and self._verbose:
                warnings.warn('Circular dependency of class %r' %
                              root.label.first())
            return graph
        visited.add(root)

        label = root.label.first() if len(root.label) == 1 else root.name
        nodes = graph.get_node(label)
        if nodes:
            node, = nodes
        else:
            if self.is_individual(label):
                node = pydot.Node(label, **style.get('individual', {}))
                node.set_name(label)
            elif self.is_defined(label):
                node = pydot.Node(label, **style.get('defined_class', {}))
                node.set_name(label)
            else:
                node = pydot.Node(label, **style.get('class', {}))
                node.set_name(label)
            graph.add_node(node)

        if leafs and label in leafs:
            return graph

        for sc in root.subclasses():
            label = sc.label.first() if len(sc.label) == 1 else sc.name
            if self.is_individual(label):
                subnode = pydot.Node(label, **style.get('individual', {}))
                subnode.set_name(label)
            elif self.is_defined(label):
                subnode = pydot.Node(label, **style.get('defined_class', {}))
                subnode.set_name(label)
            else:
                subnode = pydot.Node(label, **style.get('class', {}))
                subnode.set_name(label)
            graph.add_node(subnode)
            if relations is True or 'is_a' in relations:
                kw = style.get('is_a', {}).copy()
                if isinstance(edgelabels, dict):
                    kw['label'] = edgelabels.get('is_a', 'is_a')
                elif edgelabels:
                    kw['label'] = 'is_a'
                edge = pydot.Edge(subnode, node, **kw)
                graph.add_edge(edge)
            self._get_dot_graph(root=sc, graph=graph,
                                relations=relations, leafs=leafs,
                                style=style, visited=visited,
                                edgelabels=edgelabels)

        return graph

    def get_dot_relations_graph(self, graph=None, relations='is_a', style=None):
        """Returns a disjoined graph of all relations.

        This method simply calls get_dot_graph() with all root relations.
        All arguments are passed on.
        """
        rels = tuple(self.get_relations())
        roots = [relation for relation in rels
                 if not any([r in rels for r in relation.is_a])]
        return self.get_dot_graph(root=roots, graph=graph, relations=relations,
                                  style=style)

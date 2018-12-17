# -*- coding: utf-8 -*-
"""
A module adding graphing functionality to emmo.ontology
This addition (emmograph.py) includes:
  - Visualisation of taxonomy and ontology as graphs (using pydot).

"""
# TODO - Check comments containing FLB

import itertools
import warnings

import owlready2

import emmo

class EmmoGraph:
    """
    """


    def get_dot_graph(self, root=None, graph=None, relations='is_a',
                      leafs=None, parents=False, style=None,
                      abbreviations=None):
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
              - other : edges for other relations and restrictions
            If style is None, a very simple default style is used.
            Some pre-defined styles can be selected by name (currently
            only "uml").
        abbreviations : None | dict
            A dict mapping relation names to corresponding abbreviation.

        Note: This method requires pydot.
        """
        import pydot

        _default_style = {
            'graph': {'graph_type': 'digraph', 'rankdir': 'RL', 'fontsize': 8,
                #'fontname': 'Bitstream Vera Sans', 'splines': 'ortho',
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
            'equivalent_to': {'color': 'green', },
            'disjoint_with': {'color': 'red', },
            'inverse_of': {'color': 'orange', },
            'other': {'color': 'blue', },

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
            'equivalent_to': {'color': 'green', 'arrowhead': 'none'},
            'disjoint_with': {'color': 'red', 'arrowhead': 'none'},
            'inverse_of': {'color': 'orange', 'arrowhead': 'none'},
            'other': {'color': 'blue', 'arrowtail': 'diamond', 'dir': 'back'},
            }


        if style is None:
            style = _default_style
        elif style == 'uml':
            style = _uml_style

        graph = self._get_dot_graph(root=root, graph=graph,
                                    relations=relations, leafs=leafs,
                                    style=style)

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
                else:
                    node = pydot.Node(label, **style.get('class', {}))
                graph.add_node(node)
                if relations is True or 'is_a' in relations:
                    rootnode = graph.get_node(r.label.first())[0]
                    edge = pydot.Edge(rootnode, node, label='is_a',
                                      **style.get('is_a', {}))
                    graph.add_edge(edge)
                if (isinstance(parents, str) and label == parents):
                    break
                r = parent

        # Add edges
        for node in graph.get_nodes():
            try:
                entity = self.get_by_label(node.get_name())
            except KeyError:
                continue

            # Add is_a edges
            targets = [e for e in entity.is_a if not isinstance(e, (
                owlready2.ThingClass, owlready2.ObjectPropertyClass,
                owlready2.PropertyClass))]
            self._get_dot_add_edges(
                graph, entity, targets, 'is_a',
                relations, style.get('other', {}),
                abbreviations=abbreviations,
                constraint='false')

            # Add equivalent_to edges
            if relations is True or 'equivalent_to' in relations:
                self._get_dot_add_edges(
                    graph, entity, entity.equivalent_to, 'equivalent_to',
                    relations, style.get('equivalent_to', {}),
                    abbreviations=abbreviations,
                    constraint='false',
                )

            # disjoint_with
            if hasattr(entity, 'disjoints') and (
                    relations is True or 'disjoint_with' in relations):
                self._get_dot_add_edges(
                    graph, entity, entity.disjoints(), 'disjoint_with',
                    relations, style.get('disjoint_with', {}),
                    abbreviations=abbreviations,
                    constraint='false',
                )

            # Add inverse_of
            if hasattr(entity, 'inverse_property') and (
                    relations is True or 'inverse_of' in relations):
                self._get_dot_add_edges(
                    graph, entity, [entity.inverse_property], 'inverse_of',
                    relations, style.get('inverse_of', {}),
                    abbreviations=abbreviations,
                    constraint='false',
                )

        return graph

    def _get_dot_add_edges(self, graph, entity, targets, relation,
                           relations, style, abbreviations=None,
                           constraint=None):
        """Adds edges to `graph` for relations between `entity` and all
        members in `targets`.  `style` is a dict with options to pydot.Edge().
        """
        import pydot

        if abbreviations is None:
            abbreviations = {}

        nodes = graph.get_node(entity.label.first())
        if not nodes:
            return
        node = nodes[0]
        for e in targets:
            s = emmo.emmovocabulary.asstring(e) #FLB: put asstring in separate file?
            if isinstance(e, (owlready2.ThingClass,
                              owlready2.ObjectPropertyClass,
                              owlready2.PropertyClass)):
                label = e.label.first()
                elabel = abbreviations.get(label, label)
                nodes = graph.get_node(label)
                if nodes:
                    edge = pydot.Edge(node, nodes[0], label=elabel,
                                      **style)
                    if constraint is not None:
                        edge.set_constraint(constraint)
                    graph.add_edge(edge)
            elif isinstance(e, owlready2.Restriction):
                terms = s.split()
                if len(terms) == 3:
                    if relations is True or terms[0] in relations:
                        others = graph.get_node(terms[2])
                        if len(others) == 1:
                            other = others[0]
                        else:
                            continue
                        label = ' '.join(terms[:2])
                        elabel = abbreviations.get(label, label)
                        # Add some extra space to labels
                        edge = pydot.Edge(
                            node, other, label=elabel + '   ', **style)
                        if constraint is not None:
                            edge.set_constraint(constraint)
                        graph.add_edge(edge)
                else:
                    print('* get_dot_graph() * Ignoring: '
                          '%s %s' % (node.get_name(), s))
            else:
                print('* get_dot_graph() * Ignoring: '
                      '%s %s %s' % (node.get_name(), relation, s))



    def _get_dot_graph(self, root=None, graph=None, relations='is_a',
                       leafs=None, style=None, visited=None):
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
                                    style=style, visited=visited)
            return graph
        elif isinstance(root, (list, tuple, set)):
            for r in root:
                self._get_dot_graph(root=r, graph=graph,
                                    relations=relations, leafs=leafs,
                                    style=style, visited=visited)
            return graph
        elif isinstance(root, str):
            root = self.get_by_label(root)

        if root in visited:
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
            elif self.is_defined(label):
                node = pydot.Node(label, **style.get('defined_class', {}))
            else:
                node = pydot.Node(label, **style.get('class', {}))
            graph.add_node(node)

        if leafs and label in leafs:
            return graph

        for sc in root.subclasses():
            label = sc.label.first() if len(sc.label) == 1 else sc.name
            if self.is_individual(label):
                subnode = pydot.Node(label, **style.get('individual', {}))
            elif self.is_defined(label):
                subnode = pydot.Node(label, **style.get('defined_class', {}))
            else:
                subnode = pydot.Node(label, **style.get('class', {}))
            graph.add_node(subnode)
            if relations is True or 'is_a' in relations:
                edge = pydot.Edge(subnode, node, label='is_a',
                                  **style.get('is_a', {}))
                graph.add_edge(edge)
            self._get_dot_graph(root=sc, graph=graph,
                                relations=relations, leafs=leafs,
                                style=style, visited=visited)

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

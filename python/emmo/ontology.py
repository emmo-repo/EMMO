# -*- coding: utf-8 -*-
"""
A module adding additional functionality to owlready2. The main additions
includes:
  - Visualisation of taxonomy and ontology as graphs (using pydot).
  - Generation of a controlled vocabulary from an ontology.

If desireble some of this may be moved back into owlready2.
"""
# TODO - factor out generation of graphs and controlled vocabulary
# into own modules, keeping the Ontology class as a thin extension of
# owlready.Ontology.
import os
import re
import itertools
import warnings

import owlready2

from .entity import EntityClass, ThingClass, PropertyClass


thisdir = os.path.abspath(os.path.realpath((os.path.dirname(__file__))))
#owldir = os.path.abspath(os.path.join(thisdir, '..', '..', 'emmo', 'owl-old'))
owldir = os.path.abspath(os.path.join(thisdir, '..', '..', 'owl'))
owlready2.onto_path.append(owldir)


class NoSuchLabelError(LookupError):
    """Error raised when a label cannot be found."""
    pass


# owl types
categories = (
    'annotation_properties',
    'data_properties',
    'object_properties',
    'classes',
    'individuals',
    #'properties',
)


# Improve default rendering of entities
def render_func(entity):
    name = entity.label[0] if len(entity.label) == 1 else entity.name
    return "%s.%s" % (entity.namespace.name, name)
owlready2.set_render_func(render_func)


def get_ontology(base_iri):
    """Returns a new Ontology from `base_iri`."""
    #if thisdir not in owlready2.onto_path:
    #    owlready2.onto_path.append(thisdir)
    if (not base_iri.endswith('/')) and (not base_iri.endswith('#')):
        base_iri = '%s#' % base_iri
    if base_iri in owlready2.default_world.ontologies:
        return owlready2.default_world.ontologies[base_iri]
    else:
        return Ontology(owlready2.default_world, base_iri)


class Ontology(owlready2.Ontology):
    """A generic class extending owlready2.Ontology.
    """
    def __getitem__(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        attr = super().__getattr__(name)
        if not attr:
            attr = self.get_by_label(name)
        return attr

    def __dir__(self):
        """Include EMMO classes in dir() listing."""
        f = lambda s: s[s.rindex('.') + 1: ] if '.' in s else s
        s = set(object.__dir__(self))
        for onto in [get_ontology(uri) for uri in self._namespaces.keys()]:
            s.update([f(repr(cls)) for cls in onto.classes()])
        return sorted(s)

    def __objclass__(self):
        # Play nice with inspect...
        pass

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

        if style is None:
            style = self._default_style
        elif style == 'uml':
            style = self._uml_style

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
            s = asstring(e)
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

    def get_root_classes(self):
        """Returns a list or root classes."""
        return [cls for cls in self.classes()
                if not cls.ancestors().difference(set([cls, owlready2.Thing]))]

    def get_by_label(self, label):
        """Returns entity by label.

        If several entities have the same label, only the one which is
        found first is returned.  A KeyError is raised if `label`
        cannot be found.
        """
        # Check for name in all categories in self
        for category in categories:
            method = getattr(self, category)
            for entity in method():
                if label in entity.label:
                    return entity
        # Check for special names
        d = {
            'Nothing': owlready2.Nothing,
        }
        if label in d:
            return d[label]
        # Check imported ontologies
        for onto in self.imported_ontologies:
            onto.__class__ = self.__class__  # magically change type of onto
            try:
                return onto.get_by_label(label)
            except NoSuchLabelError:
                pass
        # Label cannot be found
        raise NoSuchLabelError('Ontology "%s" has no such label: %s' % (
            self.name, label))

    def get_by_label_all(self, label):
        """Like get_by_label(), but returns a list of all entities with
        matching labels.
        """
        return [entity for entity in
                itertools.chain(*(getattr(self, c)() for c in categories))
                if label in entity.label]

    def sync_reasoner(self):
        """Update current ontology by running the HermiT reasoner."""
        with self:
            owlready2.sync_reasoner()

    def get_relations(self):
        """Returns a generator for all relations."""
        return self.object_properties()

    def get_annotations(self, entity):
        """Returns a dict with annotations for `entity`.  Entity may be given
        either as a ThingClass object or as a label."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        d = {'comment': entity.comment}
        for a in self.annotation_properties():
            d[a.label.first()] = [
                o.strip('"') for s, p, o in
                self.get_triples(entity.storid, a.storid, None)]
        return d

    def get_branch(self, root, leafs=(), include_leafs=True):
        """Returns a list with all direct and indirect subclasses of `root`.
        Any subclass found in the sequence `leafs` will be included in
        the returned list, but its subclasses will not.

        If `include_leafs` is true, the leafs are included in the returned
        list, otherwise they are not.

        The elements of `leafs` may be ThingClass objects or labels.
        """
        def _branch(root, leafs):
            if root not in leafs:
                branch = [root]
                for c in root.subclasses():
                    branch.extend(_branch(c, leafs))
            else:
                branch = [root] if include_leafs else []
            return branch

        if isinstance(root, str):
            root = self.get_by_label(root)
        leafs = set(self.get_by_label(leaf) if isinstance(leaf, str)
                    else leaf for leaf in leafs)
        leafs.discard(root)
        return _branch(root, leafs)



    def is_individual(self, entity):
        """Returns true if entity is an individual."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return isinstance(type(entity), owlready2.ThingClass)

    def is_defined(self, entity):
        """Returns true if the entity is a derived class."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return hasattr(entity, 'equivalent_to') and bool(entity.equivalent_to)



    _markdown_template = dict(
        link='[{name}]({url})',
        point='  - {point}\n',
        points='\n\n{points}\n',
        annotation='**{key}:** {value}\n\n',
        item='### {label}\n\n{annotations}\n',
        section=('## {header} branch\n{ingress}\n\n{items}\n'),
        chapter=('# {header}\n{introduction}\n\n{content}\n'),
        document=('# Relations\n\n'
                  '{relations}\n'
                  '\n'
                  '# Entities\n\n'
                  '{entities}\n'
                  '\n'
                  '# Individuals\n\n'
                  '{individuals}'),
    )
    _html_template = dict(
        link='<a href="{url}">{name}</a>',
        point='      <li>{point}</li>\n',
        points='    <ul>\n      {points}\n    </ul>\n',
        annotation='  <dd><strong>{key}:</strong>\n{value}  </dd>\n',
        item='  <dt><dfn id="{label}">{label}</dfn></dt>\n{annotations}\n',
        section='<h2>{header}</h2>\n{ingress}\n<dl>\n{items}\n</dl>\n',
        chapter='<h1>{header}</h1>\n{introduction}\n{content}\n',
        document='\n'.join([
            '<h1>European Materials Modelling Ontology &#8210; '
            'Controlled Vocabulary</h1>',
            'Based on <a href="{ontology.base_iri}">{ontology.base_iri}</a>',
            '<h2>Relations</h2>',
            '{relations}',
            '<h2>Entities</h2>',
            '{entities}',
            '<h2>Individuals</h2>',
            '{individuals}']),
        substitutions=[(r'\n\n', r'<p>'),
                       (r'\n', r'<br>\n'),
                       (r'<p>', r'<p>\n\n'),
                       (r'\u2018([^\u2019]*)\u2019', r'<q>\1</q>'),
                       (r'\u2019', r"'"),
                       (r'\u2260', r"&ne;"),
                       (r'\u2264', r"&le;"),
                       (r'\u2265', r"&ge;"),
                       (r'\u226A', r"&x226A;"),
                       (r'\u226B', r"&x226B;"),
                       (r'"Y$', r""),  # strange noice added by owlready2
        ],
    )
    def get_vocabulary(self, items=None, sections=None, chapter=None,
                       introduction='', template='html',
                       show_individuals=False):
        """Returns a controlled vocabulary describing `items`.

        By default all entities, relations and individuals in this ontology
        are included.

        Parameters
        ----------
        items : None | sequence
            The entities (owl classes), relations (owl object properties)
            and individuals (instances) to describe.  They may be
            given as either ThingClass, ObjectPropertyClass or Thing
            objects or as label strings.  The default is to document
            all relations and entities.
        sections : None | dict
            A dict of section name - section ingress pairs. The
            section names should correspond to the name of the root
            class of the branch to document that section.

            This option cannot be combined with `items`.
        chapter : None | str
            If given, include a chapter with this name to the
            beginning of the returned document.
        introduction : str
            Introduction text of the chapter, if `chapter` is given.
        template : dict | string
            A dict defining the following template strings (and substitutions):

            :link: Formats a link.
               Substitutions: {name}
            :point: Formats a point (list item).
               Substitutions: {point}, {ontology}
            :points: Formats a list of points.  Used within annotations.
               Substitutions: {points}, {ontology}
            :annotation: Formats an annotation.
                Substitutions: {key}, {value}, {ontology}
            :item: Formats an entity or a relation with annotations.
                Substitutions: {label}, {item}, {ontology}
            :section: Formats a subsection.
                Substitutions: {header}, {ingress}, {items}, {ontology}
            :chapter: Formats a chapter.
                Substitutions: {header}, {introduction}, {content}, {ontology}
            :document: Formats a default document with all relations and
                entities.  Only used if `items` is not given.
                Substitutions: {relations}, {entities}, {individuals},
                               {ontology}
            :substitutions: list of ``(regex, sub)`` pairs for substituting
                annotation values.

            If `template` is a string, it refers to a pre-defined template.
            Currently pre-defined templates are "markdown" and "html"
        show_individuals : bool
            Whether to also include individuals (instances).

        """
        if isinstance(template, str):
            template = getattr(self, '_%s_template' % template)

        link = template.get('link', '{name}')
        point_template = template.get('point', '{point}')
        points_template = template.get('points', '{points}')
        annotation_template = template.get('annotation', '{key}: {value}\n')
        item_template = template.get('item', '{annotations}\n\n')
        #list_template = template.get('list', '{items}\n\n')
        section_template = template.get('section', '{items}\n\n')
        chapter_template = template.get('chapter', '{content}\n\n')
        doc_template = template.get('document', '{entities}')
        substitutions = template.get('substitutions', [])

        #if chapters:
        #    doc = []
        #    for header, (ingress, content) in chapters.items():
        #        print("=== Chapter: %s ===", header)
        #        if isinstance(content, dict):
        #            items, sections = None, content
        #        else:
        #            items, sections = content, None
        #        doc.append(self.get_vocabulary(
        #            items=items, sections=sections, template=template,
        #            show_individuals=show_individuals))
        #    return '\n'.join(doc)

        doc = []

        if sections is None:
            if items is None:
                relations = self.get_vocabulary(
                    items=self.object_properties(), template=template)
                entities = self.get_vocabulary(
                    items=self.classes(), template=template)
                individuals = self.get_vocabulary(
                    items=self.individuals(), template=template)
                return doc_template.format(relations=relations,
                                           entities=entities,
                                           individuals=individuals,
                                           ontology=self)
            else:
                sections = {'entity': ''}

        # Allow specifying items by label
        if items:
            items = [onto.get_by_label(item) if isinstance(item, str) else item
                     for item in items]

        # Logical "sorting" of annotations
        order = dict(definition='00', axiom='01', theorem='02',
                     elucidation='03', domain='04', range='05', example='06')
        sorter=lambda key: order.get(key, key)

        lsections = []
        for header, ingress in sections.items():
            if items is None:
                items = self.get_branch(header, sections, include_leafs=False)

            #for item in sorted(items, key=lambda i: i.label):
            litems = []
            for item in items:
                lannotations = []

                # Add annotations
                annotations = self.get_annotations(item)
                for key in sorted(annotations.keys(), key=sorter):
                    for value in annotations[key]:
                        for reg, sub in template.get('substitutions', []):
                            value = re.sub(reg, sub, value)
                        lannotations.append(annotation_template.format(
                            key=key.capitalize(), value=value, ontology=self))

                # ...add iri
                lannotations.append(annotation_template.format(
                    key='IRI', value=asstring(item.iri, link), ontology=self))

                # ...add relations from is_a
                points = []
                nonProp = (owlready2.ThingClass, #owlready2.Restriction,
                           owlready2.And, owlready2.Or, owlready2.Not)
                for p in item.is_a:
                    if (isinstance(p, nonProp) or
                        (isinstance(item, owlready2.PropertyClass) and
                         isinstance(p, owlready2.PropertyClass))):
                        points.append(point_template.format(
                            point='is_a ' + asstring(p, link), ontology=self))
                    else:
                        points.append(point_template.format(
                            point=asstring(p, link), ontology=self))

                # ...add equivalent_to relations
                for e in item.equivalent_to:
                    points.append(point_template.format(
                        point='equivalent_to ' + asstring(e, link)))

                # ...add disjoint_with relations
                if hasattr(item, 'disjoints'):
                    for d in item.disjoints():
                        for e in d.entities:
                            if e is not item:
                                points.append(point_template.format(
                                    point='disjoint_with ' + asstring(e, link),
                                    ontology=self))

                # ...add inverse_of relations
                if hasattr(item, 'inverse_property') and item.inverse_property:
                    points.append(point_template.format(
                        point='inverse_of ' + asstring(
                            item.inverse_property, link)))

                # ...add domain restrictions
                for d in getattr(item, 'domain', ()):
                    points.append(point_template.format(
                        point='domain ' + asstring(d, link)))

                # ...add range restrictions
                for d in getattr(item, 'range', ()):
                    points.append(point_template.format(
                        point='range ' + asstring(d, link)))

                # Relations
                if points:
                    value = points_template.format(
                        points=''.join(points), ontology=self)
                    lannotations.append(annotation_template.format(
                        key='Relations', value=value, ontology=self))

                # Instances (individuals)
                if show_individuals and hasattr(item, 'instances'):
                    points = []
                    for e in item.instances():
                        points.append(point_template.format(
                            point=asstring(e, link), ontology=self))
                    if points:
                        value = points_template.format(
                            points=''.join(points), ontology=self)
                        lannotations.append(annotation_template.format(
                            key='Individuals', value=value, ontology=self))

                litems.append(
                    item_template.format(label=item.label.first(), item=item,
                                         ontology=self,
                                         annotations=''.join(lannotations)))
                items = None

            lsections.append(
                section_template.format(
                    items=''.join(litems), header=header, ingress=ingress,
                    ontology=self))

        content = '\n\n'.join(lsections)
        if chapter:
            return chapter_template.format(
                header=chapter, introduction=introduction, content=content,
                ontology=self)
        else:
            return content

        #return section_template.format(
        #    items=''.join(litems), header=header, ingress=ingress,
        #    ontology=self)


def asstring(expr, link='{name}', n=0):
    """Returns a string representation of `expr`, which may be an entity,
    restriction, or logical expression of these.  `link` is a format
    string for formatting references to entities or relations.
    `n` is the recursion depth and only intended for internal use.
    """
    def fmt(e):
        """Returns the formatted label of `e`."""
        name = str(e.label.first() if hasattr(e, 'label') and e.label else e)
        if re.match(r'^[a-z]+://', name):
            return link.format(name=name, url=name)
        if hasattr(e, 'label') and e.label:
            name = e.label.first()
            url = name if re.match(r'^[a-z]+://', name) else '#' + name
            return link.format(name=name, url=url)
        elif re.match(r'^[a-z]+://', str(e)):
            return link.format(name=e, url=e)
        else:
            return str(e).replace('owl.', 'owl:')

    if isinstance(expr, str):
        #return link.format(name=expr)
        return fmt(expr)
    elif isinstance(expr, owlready2.Restriction):
        rlabel = owlready2.class_construct._restriction_type_2_label[expr.type]
        if n == 0:
            s = '%%s %s %%s' % rlabel if rlabel else '%s %s'
        elif expr.type in (owlready2.SOME, owlready2.ONLY,
                           owlready2.VALUE, owlready2.HAS_SELF):
            s = '(%%s %s %%s)' % rlabel
        else:
            s = '(%%s %s %d %%s)' % (rlabel, expr.cardinality)
        return s % (fmt(expr.property), asstring(expr.value, link, n + 1))
    elif isinstance(expr, owlready2.Or):
        s = '%s' if n == 0 else '(%s)'
        return s % ' or '.join([asstring(c, link, n + 1)
                                     for c in expr.Classes])
    elif isinstance(expr, owlready2.And):
        s = '%s' if n == 0 else '(%s)'
        return s % ' and '.join([asstring(c, link, n + 1)
                                      for c in expr.Classes])
    elif isinstance(expr, owlready2.Not):
        return 'not %s' % asstring(expr.Class, link, n + 1)
    elif isinstance(expr, owlready2.ThingClass):
        return fmt(expr)
    elif isinstance(expr, owlready2.PropertyClass):
        return fmt(expr)
    elif isinstance(expr, owlready2.Thing):  # instance (individual)
        return fmt(expr)
    elif isinstance(expr, bool):
        return repr(expr)
    else:
        raise RuntimeError('Unknown expression: %r (type: %r)' % (
            expr, type(expr)))


def is_individual(entity):
    """Returns true if entity is an individual."""
    return isinstance(type(entity), owlready2.ThingClass)

# -*- coding: utf-8 -*-
"""
A module adding additional functionality to owlready2. The main additions
includes:
  - Visualisation of taxonomy and ontology as graphs (using pydot).
  - Generation of a controlled vocabulary from an ontology.

If desireble some of this may be moved back into owlready2.
"""
import os
import sys
import re
import itertools
import warnings

if sys.version_info < (3, 2):
    raise RuntimeError('emmo requires Python 3.2 or later')

import owlready2


thisdir = os.path.abspath(os.path.dirname(__file__))
owldir = os.path.abspath(os.path.join(thisdir, '..', '..', 'emmo', 'owl'))
owlready2.onto_path.append(owldir)

# owl types
categories = (
    'annotation_properties',
    'data_properties',
    'object_properties',
    'classes',
    'individuals',
    #'properties',
)



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
    def __getattr__(self, name):
        attr = super().__getattr__(name)
        if attr:
            return attr
        else:
            return self.get_by_label(name)

    def get_dot_graph(self, root=None, graph=None, taxonomy=False,
                      other_relations=True, reflexions=False, visited=None,
                      **kw):
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
        taxonomy : bool
            Whether to only visualise the taxonomy (i.e. only include
            is_a relations).
        other_relations : bool
            Whether to visualise relations other than "is-a"-relations.
        reflexions : bool
            Whether to visualise reflective relations both ways.
        visited : None | set
            Intended for internal use only.  Used to filter out circular
            dependencies.

        Keyword arguments are passed to pydot.Dot().

        Note: This method requires pydot.
        """
        import pydot

        if graph is None:
            kw.setdefault('graph_type', 'digraph')
            kw.setdefault('rankdir', 'BT')
            #kw.setdefault('fontname', 'Bitstream Vera Sans')
            kw.setdefault('fontsize', 8)
            #kw.setdefault('splines', 'ortho')
            graph = pydot.Dot(**kw)

        if visited is None:
            visited = set()

        if root is None:
            for root in self.get_root_classes():
                self.get_dot_graph(root=root, graph=graph, taxonomy=taxonomy,
                                   other_relations=other_relations,
                                   reflexions=reflexions, visited=visited)
            return graph
        elif isinstance(root, (list, tuple, set)):
            for r in root:
                self.get_dot_graph(root=r, graph=graph, taxonomy=taxonomy,
                                   other_relations=other_relations,
                                   reflexions=reflexions, visited=visited)
            return graph
        elif isinstance(root, str):
            root = self.get_by_label(root)

        if root in visited:
            warnings.warn('Circular dependency of class %r' %
                          root.label.first())
            return graph
        visited.add(root)

        label = root.label.first()
        nodes = graph.get_node(label)
        if nodes:
            node, = nodes
        else:
            node = pydot.Node(label)
            graph.add_node(node)

        for subclass in root.subclasses():
            subnode = pydot.Node(subclass.label.first())
            edge = pydot.Edge(subnode, node, label='is_a')
            graph.add_edge(edge)
            #print('=== ', subclass.label.first())
            #print('    edge:', edge.to_string())
            self.get_dot_graph(root=subclass, graph=graph,
                               taxonomy=taxonomy,
                               reflexions=reflexions, visited=visited)

        if not taxonomy:
            #for e in
            pass

        return graph

    def get_relations(self):
        """Returns a generator for all relations."""
        return self.object_properties

    def get_dot_relations_graph(self, graph=None, **kw):
        """Returns a disjoined graph of all relations.

        This method simply calls get_dot_graph() with all root relations.
        All arguments are passed on.
        """
        relations = tuple(self.get_relations())
        roots = [relation for relation in relations
                 if not any([r in relations for r in relation.is_a])]
        return self.get_dot_graph(root=roots, graph=graph, **kw)

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
        for category in categories:
            method = getattr(self, category)
            for entity in method():
                if label in entity.label:
                    return entity
        raise KeyError('Ontology "%s" has no such label: %s' % (
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

    _markdown_template = dict(
        point='  - {point}\n',
        points='\n\n{points}\n',
        annotation='**{key}:** {value}\n\n',
        item='### {label}\n\n{annotations}\n',
        list='{items}',
        document='# Controlled vocabulary\nBased on {ontology.name}.\n\n'
                 '## Relations\n\n{relations}\n\n'
                 '## Entities\n\n{entities}\n\n'
                 '## Individuals\n\n{individuals}',
    )
    _html_template = dict(
        link='<a href="#{name}">{name}</a>',
        point='      <li>{point}</li>\n',
        points='    <ul>\n      {points}\n    </ul>\n',
        annotation='  <dd><strong>{key}:</strong> {value}</dd>\n',
        item='  <dt><dfn id="{label}">{label}</dfn></dt>\n{annotations}\n',
        list='<dl>\n{items}\n</dl>',
        document='\n'.join(['<h1>Controlled vocabulary</h1>',
                            'Based on {ontology.name}.',
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
    def get_vocabulary(self, items=None, template='html',
                     show_individuals=True):
        """Returns a controlled vocabulary describing `items`.

        By default all entities, relations and individuals in this ontology
        are included.

        Parameters
        ----------
        items : sequence
            The entities (owl classes), relations (owl object properties)
            and individuals (instances) to describe.  They may be
            given as either ThingClass, ObjectPropertyClass or Thing
            objects or as label strings.  The default is to document
            all relations and entities.
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
            :list: Formats a list of items.
                Substitutions: {items}, {ontology}
            :document: Formats a default document with all relations and
                entities.  Only used if `items` is not given.
                Substitutions: {relations}, {entities}, {ontology}
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
        list_template = template.get('list', '{items}\n\n')
        doc_template = template.get('document', '{entities}')
        substitutions = template.get('substitutions', [])

        if items is None:
            relations = self.get_vocabulary(self.object_properties(), template)
            entities = self.get_vocabulary(self.classes(), template)
            individuals = self.get_vocabulary(self.individuals(), template)
            return doc_template.format(relations=relations, entities=entities,
                                       individuals=individuals,
                                       ontology=self)

        # Allow specifying items by label
        items = [onto.get_by_label(item) if isinstance(item, str) else item
                 for item in items]

        # Sort annotations
        order = dict(definition='00', axiom='01', theorem='02',
                     elucidation='03', domain='04', range='05', example='06')
        sorter=lambda key: order.get(key, key)

        litems = []
        for item in sorted(items, key=lambda i: i.label):
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
                key='IRI', value=item.iri, ontology=self))

            # ...add relations from is_a
            points = []
            nonProp = (owlready2.ThingClass, #owlready2.Restriction,
                       owlready2.And, owlready2.Or, owlready2.Not)
            for p in item.is_a:
                if (isinstance(p, nonProp) or
                    (isinstance(item, owlready2.PropertyClass) and
                     isinstance(p, owlready2.PropertyClass))):
                    points.append(point_template.format(
                        point='is_a: ' + asstring(p, link), ontology=self))
                else:
                    points.append(point_template.format(
                        point=asstring(p, link), ontology=self))

            # ...add equivalent_to relations
            for e in item.equivalent_to:
                points.append(point_template.format(
                    point='equivalent_to: ' + asstring(e, link)))

            # ...add disjoint_with relations
            if hasattr(item, 'disjoints'):
                for d in item.disjoints():
                    for e in d.entities:
                        if e is not item:
                            points.append(point_template.format(
                                point='disjoint_with: ' + asstring(e, link),
                                ontology=self))

            # ...add inverse_of relations
            if hasattr(item, 'inverse_property') and item.inverse_property:
                points.append(point_template.format(
                    point='inverse_of: ' + asstring(
                        item.inverse_property, link)))

            # ...add domain restrictions
            for d in getattr(item, 'domain', ()):
                points.append(point_template.format(
                    point='domain: ' + asstring(d, link)))

            # ...add range restrictions
            for d in getattr(item, 'range', ()):
                points.append(point_template.format(
                    point='range: ' + asstring(d, link)))

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
        return list_template.format(items=''.join(litems), ontology=self)


def asstring(expr, link='{name}', n=0):
    """Returns a string representation of `expr`, which may be an entity,
    restriction, or logical expression of these.  `link` is a format
    string for formatting references to entities or relations.
    `n` is the recursion depth and only intended for internal use.
    """
    def fmt(e):
        """Returns the formatted label of `e`."""
        if hasattr(e, 'label') and e.label:
            return link.format(name=e.label[0])
        else:
            return str(e).replace('owl.', 'owl:')

    if isinstance(expr, owlready2.Restriction):
        rlabel = owlready2.class_construct._restriction_type_2_label[expr.type]
        if n == 0:
            s = '%s: %s'
            n -= 1
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

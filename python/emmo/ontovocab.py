# -*- coding: utf-8 -*-
"""
A module adding vocabulary functionality to emmo.ontology
"""
#
# This module was written before I had a good understanding of DL.
# Should be simplified and improved:
#   - Rewrite OntoVocab to be a standalone class instead of as an mixin
#     for Ontology.
import re

import owlready2

from .utils import asstring


class OntoVocab:
    """A mixin class used by emmo.ontology.Ontology that adds
    functionality for generating controlled vocabularies.
    """
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

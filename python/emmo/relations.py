# -*- coding: utf-8 -*-
"""This module defines some extension methods that will be injected into
the owlready2.EntityClass and its sub(meta)classes.
"""

from owlready2 import (
    EntityClass, Thing, ThingClass, ObjectPropertyClass, PropertyClass,
    Restriction, LogicalClassConstruct, ClassConstruct,
    )


def get_related(cls, relations='relation', fixed_relations=None,
                recursive=True, initial_classes=None):
    """Returns a set of all classes that are related to class `cls` via a
    restriction who's property matches any of the relations specified
    in `relations` or `fixed_relations`.

    Parameters
    ----------
    relations : string | instance of ObjectPropertyClass | sequence

    fixed_relations : string | instance of ObjectPropertyClass | sequence

    The difference between `relations` and `fixed_relations` is that
    matches `relations` matches any property that equals to or is a
    descendant of a relation in `relations`, while  """
    matches = set(initial_classes) if initial_classes else set()
    onto = cls.namespace.world

    def tolist(rels):
        if rels is None:
            rels = []
        elif isinstance(rels, (str, ObjectPropertyClass)):
            rels = [rels]
        return [p if isinstance(p, ObjectPropertyClass)
                else onto.search_one(label=p)
                for p in rels]

    def add_match(val):
        new = set()
        if isinstance(val, ThingClass):
            new.add(val)
        elif isinstance(val, LogicalClassConstruct):
            new.update(val.Classes)
        elif isinstance(val, ClassConstruct):
            new.add(val.Class)
        if recursive:
            for n in new:
                if n not in matches:
                    matches.update(get_related(
                        n, relations=relations,
                        fixed_relations=fixed_relations,
                        recursive=recursive, initial_classes=matches))
        matches.update(new)

    relations = tolist(relations)
    fixed_relations = tolist(fixed_relations)

    for r in cls.is_a:
        if isinstance(r, Restriction):
            for rel in relations:
                if issubclass(r.property, rel):
                    add_match(r.value)
            for rel in fixed_relations:
                if rel.name == r.property.name:
                    add_match(r.value)

    matches.discard(cls)
    return matches


setattr(ThingClass, 'get_related', get_related)

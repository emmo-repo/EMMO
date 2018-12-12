# -*- coding: utf-8 -*-
"""This module defines some extension methods that will be injected into
the owlready2.EntityClass and its sub(meta)classes.
"""

#import owlready2
from owlready2 import EntityClass, ThingClass, PropertyClass, Restriction


def inject_relation(name, relation_name=None):
    """Injects a property `name` into owlready2.ThingClass corresponding
    to the relation `relation_name`.

    The injected property will return a list of all classes or
    class constructs corresponding to the relation.
    """
    if relation_name is None:
        relation_name = name

    def get(cls):
        parts = []
        # include equivalent_to restrictions
        for restriction in cls.equivalent_to:
            if restriction.property.label.first() == relation_name:
                parts.append(restriction.value)
        # include is_a restrictions
        for item in cls.is_a:
            if isinstance(item, Restriction):
                if item.property.label.first() ==  relation_name:
                    parts.append(item.value)
        return parts

    get.__doc__ = 'Returns a list of %s for the given EMMO class.' % (
        name.replace('_', ' '))

    # inject method
    #setattr(ThingClass, 'get_' + name, get)

    # inject property
    setattr(ThingClass, name, property(get, doc=get.__doc__))


# Direct parthood
# It seems that the following parthood relations are actually used in EMMO
inject_relation('spatial_direct_parts', 'has_spatial_direct_part')
inject_relation('temporal_direct_parts', 'has_temporal_direct_part')
inject_relation('spacetime_direct_parts', 'has_spacetime_direct_part')

# Proper part
inject_relation('proper_parts', 'has_proper_part')
inject_relation('spatial_proper_parts', 'has_spatial_proper_part')
inject_relation('temporal_proper_parts', 'has_temporal_proper_part')
inject_relation('is_proper_part_of')

# Abstract part
inject_relation('abstract_parts', 'has_abstract_part')
inject_relation('is_abstract_part_of')

# Abstraction
inject_relation('is_abstraction_of')

# Representation
inject_relation('representations', 'has_representation')
inject_relation('is_representation_for')

# Properties
inject_relation('properties', 'has_property')


# Set theory
inject_relation('members', 'has_member')  # unused in EMMO
inject_relation('is_member_of')  # unused in EMMO

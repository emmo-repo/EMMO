# -*- coding: utf-8 -*-
"""This module defines some extension methods that will be injected into
the owlready2.EntityClass and its sub(meta)classes.
"""

#import owlready2
from owlready2 import (
    EntityClass, ThingClass, PropertyClass, Thing, Restriction
    )
from owlready2.util import CallbackList


# List of all relations in EMMO
_relations  = [
    'relation',
    'active_relation',
    'passive_relation',
    #
    # Parthood
    'has_part',  # FIXME - should be implemented
    'has_spatial_part',  # unused in EMMO
    'has_temporal_part',  # unused in EMMO
    'is_part_of',  # FIXME - should be implemented
    'is_spatial_part_of',  # unused in EMMO
    'is_temporal_part_of',  # unused in EMMO
    # -- proper part
    'has_proper_part',
    'has_spatial_proper_part',
    'has_temporal_proper_part',
    'is_proper_part_of',
    'is_spatial_proper_part_of',  # unused in EMMO
    'is_temporal_proper_part_of',  # unused in EMMO
    # -- direct part
    'has_spatial_direct_part',
    'has_temporal_direct_part',
    'has_spacetime_direct_part',
    'is_spatial_direct_part_of',  # unused in EMMO
    'is_temporal_direct_part_of',  # unused in EMMO
    'is_spacetime_direct_part_of',  # unused in EMMO
    #
    # Abstraction
    'has_abstraction',  # unused in EMMO
    'is_abstraction_of',
    #
    # Abstract part
    'has_abstract_part',
    'is_abstract_part_of',
    #
    # Representation
    'has_representation',
    'is_representation_for',
    #
    # Membership (set theory)
    'has_member',  # unused in EMMO
    'is_member_of',  # unused in EMMO
    #
    # Properties
    'has_property',
    'is_property_of',  # unused in EMMO
]


# List with all properties to be injected
_injections = []


class Relations(object):
    """Simple class for storing relations in a separate namespace.

    Implements index access, equality, containment and string representation.
    """
    def __init__(self, cls, **kw):
        self._cls = cls
        for k, v in kw.items():
            setattr(self, k, v)

    def __getitem__(self, name):
        return self.__dict__[name]

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, name):
        return name in self.__dict__

    def __repr__(self):
        #return 'Relations(%s)' % ', '.join(
        #    ['%s=%r' % (k, v) for k, v in self.__dict__.items()])
        return 'Relations(<%s>)' % ', '.join(
            k for k in self.__dict__ if not k.startswith('_'))

for relation in _relations:
    def _get_related(r, relation=relation):
        related = []
        cls = r._cls
        print('-+-', cls, relation)
        # include equivalent_to restrictions
        for restriction in cls.equivalent_to:
            if restriction.property.label.first() == relation:
                related.append(restriction.value)
        # include is_a restrictions
        for item in cls.is_a:
            if isinstance(item, Restriction):
                if item.property.label.first() ==  relation:
                    related.append(item.value)
        return related
    doc = ('Returns a list of  all classes or class constructs corresponding '
           'to relationship `%s`.' % (relation, ))
    setattr(Relations, relation, property(_get_related, doc=doc))


def mark_for_injection(attr, name, prop=True, classes=True, individuals=True):
    """Mark attribute `attr` for injection into all classes and/or
    individuals using the given name.

    If `prop` is true, it is injected as property, otherwise as
    attribute or method.

    If `classes` or `individuals` is false, no injection will be performed
    into the corresponding type.
    """
    _injections.append((attr, name, prop, classes, individuals))


def get_init(orig_init):
    """Returns an __init__ function that extends the original __init__
    function `orig_init`."""
    def init(self, *args, **kw):
        print('=+=', self)
        orig_init(self, *args, **kw)
        setattr(self, 'emmo_relations', Relations(self))
    return init

type.__setattr__(Thing, '__init__', get_init(Thing.__dict__['__init__']))
#type.__setattr__(ThingClass, '__init__', get_init(ThingClass.__dict__['__init__']))
#setattr(ThingClass, '__init__', get_init(ThingClass.__init__))



#def related_factory(cls, relation):
#    """A factory fuction returning a function that returns a list of all
#    classes or class constructs for `cls` corresponding to `relation`."""
#    print('*** factory:', cls, relation)
#    # use default arguments to speed up lookup
#    def get_related(r, cls=cls, relation=relation):
#        related = []
#        print('+-+', cls, relation)
#        # include equivalent_to restrictions
#        for restriction in cls.equivalent_to:
#            if restriction.property.label.first() == relation:
#                related.append(restriction.value)
#        # include is_a restrictions
#        for item in cls.is_a:
#            if isinstance(item, Restriction):
#                if item.property.label.first() ==  relation:
#                    related.append(item.value)
#        return related
#    get_related.__doc__ = ('Returns a list of corresponding to relationship '
#                           '`%s` for %s.' % (relation, cls))
#    return get_related
#
#
#
#def get_init(orig_init):
#    """Returns an __init__ function that extends the original __init__
#    function `orig_init`."""
#    def init(self, *args, **kw):
#        orig_init(self, *args, **kw)
#
#        # Inject relations
#        for relation in _relations:
#
#            def getter(r, cls=self, relation=relation):
#                related = []
#                print('+++', cls, relation)
#                # include equivalent_to restrictions
#                for restriction in cls.equivalent_to:
#                    if restriction.property.label.first() == relation:
#                        related.append(restriction.value)
#                # include is_a restrictions
#                for item in cls.is_a:
#                    if isinstance(item, Restriction):
#                        if item.property.label.first() == relation:
#                            related.append(item.value)
#                return related
#            getter = related_factory(self, relation)
#
#            doc = ('A list of corresponding to relationship `%s` for the '
#                   'given EMMO individual.' % relation)
#            setattr(Relations, relation, property(getter, doc=doc))
#            setattr(self, 'emmo_relations', Relations())
#
#        # Inject other attributes
#        for attr, name, prop, classes, individuals in _injections:
#            if individuals:
#                if prop:
#                    doc = getattr(attr, __doc__, '')
#                    setattr(self.__class__, name, property(attr, doc=doc))
#                else:
#                    setattr(self, name, attr)
#    return init
#
## Inject into all individuals via extended __init__ function
#type.__setattr__(Thing, '__init__', get_init(Thing.__dict__['__init__']))
#
#
#def func(cls):
#    print('~~~', cls, cls.__class__)
#
#setattr(ThingClass, 'func', property(func))
#
#
#
#def inject_into_classes():
#    """Inject into ThingClass."""
#
#    # Inject relations
#    for relation in _relations:
#
#        def getter(r):
#            cls = r._klass
#            print('+*+', cls, cls.__class__)
#            related = []
#            # include equivalent_to restrictions
#            for restriction in cls.equivalent_to:
#                if restriction.property.label.first() == relation:
#                    related.append(restriction.value)
#            # include is_a restrictions
#            for item in cls.is_a:
#                if isinstance(item, Restriction):
#                    if item.property.label.first() == relation:
#                        related.append(item.value)
#            return related
#        doc = ('A list of corresponding to relationship `%s` for the '
#               'given EMMO class.' % relation)
#        setattr(Relations, relation, property(getter, doc=doc))
#        setattr(ThingClass, 'emmo_relations', Relations(ThingClass))
#
#    # Inject other attributes
#    for attr, name, prop, classes, individuals in _injections:
#        if individuals:
#            if prop:
#                doc = getattr(attr, __doc__, '')
#                setattr(self.__class__, name, property(attr, doc=doc))
#            else:
#                setattr(self, name, attr)






#setattr(ThingClass, '__init__', get_init(ThingClass.__init__))

#def mark_relations_for_injection(relations):
#    """Injects `relations` into all classes and individuals."""
#    r = Relations()
#    for relation in relations:
#
#        def getter(cls):
#            parts = []
#            # include equivalent_to restrictions
#            for restriction in cls.equivalent_to:
#                if restriction.property.label.first() == relation:
#                    parts.append(restriction.value)
#            # include is_a restrictions
#            for item in cls.is_a:
#                if isinstance(item, Restriction):
#                    if item.property.label.first() ==  relation:
#                        parts.append(item.value)
#            return parts
#
#        getter.__doc__ = ('Returns a list of corresponding to relation `%s` '
#                          'for the given EMMO class.' % relation)
#        r[relation] = getter
#
#    mark_for_injection(r, 'emmo_relations', prop=False)



#def inject_all():
#    """Inject all attributes marked for injection."""
#    saved_init = Thing.__dict__['__init__']
#
#    # Init function replacing Thing.__init__()
#    def init(self, *args, **kw):
#        saved_init(self, *args, **kw)
#
#        # Inject relations
#        for relation in _relations:
#
#            def getter(r):
#                cls = r._klass
#                print('+++', cls, cls.__class__)
#                related = []
#                # include equivalent_to restrictions
#                for restriction in cls.equivalent_to:
#                    if restriction.property.label.first() == relation:
#                        related.append(restriction.value)
#                # include is_a restrictions
#                for item in cls.is_a:
#                    if isinstance(item, Restriction):
#                        if item.property.label.first() == relation:
#                            related.append(item.value)
#                return related
#            doc = ('A list of corresponding to relationship `%s` for the '
#                   'given EMMO class.' % relation)
#            setattr(Relations, relation, property(getter, doc=doc))
#            setattr(self, 'emmo_relations', Relations(self))
#
#        # Inject other attributes
#        for attr, name, prop, classes, individuals in _injections:
#            if individuals:
#                if prop:
#                    doc = getattr(attr, __doc__, '')
#                    setattr(self.__class__, name, property(attr, doc=doc))
#                else:
#                    setattr(self, name, attr)
#
#    type.__setattr__(Thing, '__init__', init)
#
#    for attr, name, prop, classes, individuals in _injections:
#        if classes:
#            if prop:
#                help = getattr(attr, __doc__, '')
#                setattr(ThingClass, name, property(attr, doc=help))
#            else:
#                setattr(ThingClass, name, attr)


#def get_related(cls):
#    """Returns a list of all classes or class constructs corresponding to
#    relation `cls`."""
#    related = []
#    # include equivalent_to restrictions
#    for restriction in cls.equivalent_to:
#        if restriction.property.label.first() == relation_name:
#            related.append(restriction.value)
#    # include is_a restrictions
#    for item in cls.is_a:
#        if isinstance(item, Restriction):
#            if item.property.label.first() ==  relation_name:
#                related.append(item.value)
#    return related


# Inject relations
#mark_relations_for_injection(_relations)
#mark_for_injection(
#    Relations(**{relation: get_related for relation in _relations}),
#    'emmo_relations',
#    prop=False,
#    )

#inject_all()


#_getters = {}
#
#def inject_relation(name, relation_name=None):
#    """Injects a property `name` into owlready2.ThingClass corresponding
#    to the relation `relation_name`.
#
#    The injected property will return a list of all classes or class
#    constructs corresponding to the relation.
#    """
#    if relation_name is None:
#        relation_name = name
#
#    def getter(cls):
#        parts = []
#        # include equivalent_to restrictions
#        for restriction in cls.equivalent_to:
#            if restriction.property.label.first() == relation_name:
#                parts.append(restriction.value)
#        # include is_a restrictions
#        for item in cls.is_a:
#            if isinstance(item, Restriction):
#                if item.property.label.first() ==  relation_name:
#                    parts.append(item.value)
#        return parts
#
#    getter.__doc__ = ('Returns a list of corresponding to relation `%s` for '
#                      'the given EMMO class.' % relation_name)
#    _getters[relation_name] = getter
#
#    # inject method
#    #setattr(ThingClass, 'get_' + name, getter)
#
#    # inject property
#    setattr(ThingClass, name, property(getter, doc=getter.__doc__))
#
#
## Direct parthood
## It seems that the following parthood relations are actually used in EMMO
#inject_relation('spatial_direct_parts', 'has_spatial_direct_part')
#inject_relation('temporal_direct_parts', 'has_temporal_direct_part')
#inject_relation('spacetime_direct_parts', 'has_spacetime_direct_part')
#
## Proper part
#inject_relation('proper_parts', 'has_proper_part')
#inject_relation('spatial_proper_parts', 'has_spatial_proper_part')
#inject_relation('temporal_proper_parts', 'has_temporal_proper_part')
#inject_relation('is_proper_part_of')
#
## Abstract part
#inject_relation('abstract_parts', 'has_abstract_part')
#inject_relation('is_abstract_part_of')
#
## Abstraction
#inject_relation('is_abstraction_of')
#
## Representation
#inject_relation('representations', 'has_representation')
#inject_relation('is_representation_for')
#
## Properties
#inject_relation('properties', 'has_property')
#
#
## Set theory
#inject_relation('members', 'has_member')  # unused in EMMO
#inject_relation('is_member_of')  # unused in EMMO
#
#
#
## Inject relations into individuals
#_saved_init = Thing.__dict__['__init__']
#
#def init(self, *args, **kw):
#    _saved_init(self, *args, **kw)
#    for name, getter in _getters.items():
#        setattr(self, name, getter(self))
#
#type.__setattr__(Thing, '__init__', init)
#
#
## Inject annotations
#def get_annotations(obj):
#    """Returns a dict with annotations for `entity`."""
#    d = {'comment': obj.comment}
#    for a in obj.namespace.get_annotations(obj):
#        d[a.label.first()] = [
#            o.strip('"') for s, p, o in
#            obj.namespace.get_triples(entity.storid, a.storid, None)]
#    return d
#setattr(ThingClass, 'annotations', get_annotations)
#type.__setattr__(Thing, 'get_annotations', get_annotations)
#
#
#def is_individual(obj):
#    """Returns true if entity is an individual."""
#    return isinstance(obj, owlready2.Thing)
#setattr(ThingClass, 'is_individual', is_individual)
#type.__setattr__(Thing, 'is_individual', is_individual)
#
#
#def is_defined(obj):
#    """Returns true if the entity is a defined class."""
#    if hasattr(obj, 'equivalent_to'):
#        return bool(obj.equivalent_to)
#    elif hasattr(obj, 'get_equivalent_to'):
#        return bool(obj.get_equivalent_to())
#    else:
#        return False
#setattr(ThingClass, 'is_defined', is_defined)
#type.__setattr__(Thing, 'is_defined', is_defined)
#

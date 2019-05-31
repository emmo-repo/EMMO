#!/usr/bin/env python3
"""Module for representing an EMMO-based ontology, as a collection of
DLite metadata entities.

Entities in the ontology are mapped to DLite as follows:
  - owl class -> metadata entity
  - owl object property -> relation
  - owl restriction -> entity + relation
  - owl class construct -> entity + relation(s)

TODO:
  - map restriction cardinality to collection diminsions

"""
import sys
import json
import re
from inspect import isclass

import dlite
from dlite import Instance, Dimension, Property
from emmo import get_ontology
import owlready2


# We want an ordered dict.  From Python 3.7 (unofficially 3.6) the
# built-in dict conserves insertion order.
if sys.version_info >= (3, 7):
    odict = dict
else:
    from collections import OrderedDict as odict


class EMMO2Meta:
    """A class for representing EMMO or an EMMO-based ontology as a
    collection of metadata entities using DLite.

    Parameters
    ----------
    ontology : string
        URI or path to the ontology to represent.  Defaults to EMMO.
    classes : sequence
        The classes to include.  May be given either as a sequence of
        strings or a sequence of owlready2 classes.  The default is to
        include all of the ontology.
    version : string
        Default version for classes lacking a `version` annotation.
    collid : string
        Set an explicit id to the generated collection.

    Notes
    -----
    The collection UUID is accessable via the `coll.uuid` attribute.
    Use the `collid` argument to provide a human readable id to make
    it easier to later to retrieve it from a storage (without having
    to remember its UUID).
    """
    def __init__(self, ontology=None, classes=None, version='0.1', collid=None):
        if ontology is None:
            self.onto = get_ontology()
            self.onto.load()
        elif isinstance(ontology, str):
            self.onto = get_ontology(ontology)
            self.onto.load()
        else:
            self.onto = ontology
        self.version = version
        self.iri = self.onto.base_iri
        self.namespace = self.onto.base_iri.rstrip('#')
        self.coll = dlite.Collection(collid)
        # To avoid infinite recursion when adding cyclic dependent entities
        # we keep track of all labels we add (or are going to add) to the
        # collection
        self.labels = set()

        if classes is None:
            classes = self.onto.classes()
        elif isinstance(classes, str):
            classes = [classes]

        for cls in classes:
            self.add_class(cls)

    def get_subclasses(self, cls):
        """Returns a generator yielding all subclasses of owl class `cls`."""
        yield cls
        for subcls in cls.subclasses():
            yield from all_subclasses(subcls)

    def get_uri(self, name, version=None):
        """Returns uri (namespace/version/name)."""
        if version is None:
            version = self.version
        return '%s/%s/%s' % (self.namespace, version, name)

    def get_uuid(self, uri=None):
        """Returns a UUID corresponding to `uri`.  If `uri` is None,
        a random UUID is returned."""
        return dlite.get_uuid(uri)

    def get_label(self, entity):
        """Returns a label for entity."""
        if hasattr(entity, 'label'):
            return entity.label.first()
        name = repr(entity)
        label, n = re.subn(r'emmo(-[a-z]+)?\.', '', name)
        return label

    def find_label(self, inst):
        """Returns label for class instance `inst` already added to the
        collection."""
        if hasattr(inst, 'uuid'):
            uuid = inst.uuid
        else:
            uuid = dlite.get_uuid(inst)
        rel = self.coll.find_first(p='_has-uuid', o=uuid)
        if not rel:
            raise ValueError('no class instance with UUID: %s' % uuid)
        return rel.s

    def add(self, entity):
        """Adds owl entity to collection and returns a reference to the
        new metadata."""
        if entity == owlready2.Thing:
            raise ValueError("invalid entity: %s" % entity)
        elif isinstance(entity, owlready2.ThingClass):
            return self.add_class(entity)
        elif isinstance(entity, owlready2.ClassConstruct):
            return self.add_class_construct(entity)
        else:
            raise ValueError("invalid entity: %s" % entity)

    def add_class(self, cls):
        """Adds owl class `cls` to collection and returns a reference to
        the new metadata."""
        if isinstance(cls, str):
            cls = self.onto[cls]
        label = cls.label.first()
        if label not in self.labels:
            assert not self.coll.has(label)
            self.labels.add(label)
            uri = self.get_uri(label)
            for r in cls.is_a:
                if isinstance(r, owlready2.ThingClass):
                    self.labels.add(label)
                    self.coll.add_relation(label, "is_a", r.label.first())
                    self.add_class(r)
                elif isinstance(r, owlready2.Restriction):
                    if     (issubclass(r.property, self.onto.has_property) and
                            isinstance(r.value, owlready2.ThingClass) and
                            isinstance(r.value, self.onto.property)):
                        self.add_class(r.value)
                    else:
                        self.add_restriction(r)
                elif isinstance(r, owlready2.ClassConstruct):
                    self.add_class_construct(r)
                else:
                    raise TypeError('Unexpected is_a member: %s' % type(r))
            dims, props = self.get_properties(cls)
            e = Instance(uri, dims, props, self.get_description(cls))
            self.coll.add(label, e)
        return self.coll.get(label)

    def get_properties(self, cls):
        """Returns two lists with the dlite dimensions and properties
        correspinding to owl class `cls`."""
        dims = []
        props = []
        dimindices = {}
        propnames = set()
        types = dict(integer='int', real='double', string='string')

        def get_dim(r, name, descr=None):
            """Returns dimension index corresponding to dimension name `name`
            for property `r.value`."""
            t = owlready2.class_construct._restriction_type_2_label[r.type]
            if (t in ('some', 'only', 'min') or
                (t in ('max', 'exactly') and r.cardinality > 1)):
                if name not in dimindices:
                    dimindices[name] = len(dims)
                    dims.append(Dimension(name, descr))
                return [dimindices[name]]
            else:
                return []

        for c in cls.mro():
            if not isinstance(c, owlready2.ThingClass):
                continue
            for r in c.is_a:
                if     (isinstance(r, owlready2.Restriction) and
                        issubclass(r.property, self.onto.has_property) and
                        isinstance(r.value, owlready2.ThingClass) and
                        isinstance(r.value, self.onto.property)):
                    name = self.get_label(r.value)
                    if name in propnames:
                        continue
                    propnames.add(name)

                    # Default type, ndims and unit
                    if isinstance(r.value, (self.onto.descriptive_property,
                                            self.onto.qualitative_property,
                                            self.onto.subjective_property)):
                        ptype = 'string'
                    else:
                        ptype = 'double'
                    d = []
                    d.extend(get_dim(r, 'n_%ss' % name, 'Number of %s.' % name))
                    unit = None

                    # Update type, ndims and unit from relations
                    for r2 in [r] + r.value.is_a:
                        if isinstance(r2, owlready2.Restriction):
                            if issubclass(r2.property, self.onto.has_type):
                                typelabel = self.get_label(r2.value)
                                ptype = types[typelabel]
                                d.extend(get_dim(r2, '%s_length' % name,
                                                 'Length of %s' % name))
                            elif issubclass(r2.property, self.onto.has_unit):
                                unit = self.get_label(r2.value)

                    descr = self.get_description(r.value)
                    props.append(Property(name, type=ptype, dims=d,
                                          unit=unit, description=descr))
        return dims, props

    def add_restriction(self, r):
        """Adds owl restriction `r` to collection and returns a reference
        to it."""
        rtype = owlready2.class_construct._restriction_type_2_label[r.type]
        cardinality = r.cardinality if r.cardinality else 0
        label = 'restriction_%s_%d' % (rtype, cardinality)
        if label not in self.labels:
            assert not self.coll.has(label)
            self.labels.add(label)
            e = self.add_restriction_entity()
            inst = e(id=label)
            inst.type = rtype
            inst.cardinality = cardinality
            vlabel = self.get_label(r.value)
            if not vlabel in self.labels:
                self.labels.add(vlabel)
                self.add(r.value)
            if not self.coll.has(label):
                self.coll.add(label, inst)
            self.coll.add_relation(label, r.property.label.first(), vlabel)
        return self.coll.get(label)

    def add_restriction_entity(self):
        """Adds restriction metadata to collection and returns a reference
        to it."""
        uri = self.get_uri("Restriction")
        uuid = self.get_uuid(uri)
        if not self.coll.has('Restriction'):
            props = [
                Property('type', type='string', description='Type of '
                         'restriction.  Valid values for `type` are: '
                         '"only", "some", "exact", "min" and "max".'),
                Property('cardinality', type='int', description='The '
                         'cardinality.  Unused for "only" and '
                         '"some" restrictions.'),
            ]
            e = Instance(uri, [], props,
                         "Class restriction.  For each instance of a class "
                         "restriction there should be a relation\n"
                         "\n"
                         "    (r.label, r.property, r.value.label)\n"
                         "\n"
                         "where `r.label` is the label associated with the "
                         "restriction, `r.property` is a relation and "
                         "`r.value.label` is the label of the value of the "
                         "restriction.")
            self.labels.add('Restriction')
            self.coll.add('Restriction', e)
        return self.coll.get('Restriction')

    def add_class_construct(self, c):
        """Adds owl class construct `c` to collection and returns a reference
        to it."""
        ctype = c.__class__.__name__
        label = 'class_construct_%s' % ctype
        if not label in self.labels:
            assert not self.coll.has(label)
            e = self.add_class_construct_entity()
            self.labels.add(label)
            inst = e(id=label)
            inst.type = ctype
            if isinstance(c, owlready2.LogicalClassConstruct):
                args = c.Classes
            else:
                args = [c.Class]
            for arg in args:
                self.coll.add_relation(label, 'has_argument',
                                       self.get_label(arg))
            self.coll.add(label, inst)
        return self.coll.get(label)

    def add_class_construct_entity(self):
        """Adds class construct metadata to collection and returns a reference
        to it."""
        uri = self.get_uri("ClassConstruct")
        uuid = self.get_uuid(uri)
        if not self.coll.has('ClassConstruct'):
            props = [
                Property('type', type='string', description='Type of '
                         'class construct.  Valid values for `type` are: '
                         '"not", "inverse", "and" or "or".'),
            ]
            e = Instance(uri, [], props,
                         "Class construct.  For each instance of a class "
                         "construct there should be one or more relations "
                         "of type\n"
                         "\n"
                         "    (c.label, \"has_argument\", c.value.label)\n"
                         "\n"
                         "where `c.label` is the label associated with the "
                         "class construct, `c.value.label` is the label of "
                         "an argument.")
            self.labels.add('ClassConstruct')
            self.coll.add('ClassConstruct', e)
        return self.coll.get('ClassConstruct')

    def get_description(self, cls):
        """Returns description for OWL class `cls` by combining its
        annotations."""
        if isinstance(cls, str):
            cls = onto[cls]
        descr = []
        annotations = self.onto.get_annotations(cls)
        if 'definition' in annotations:
            descr.extend(annotations['definition'])
        if 'elucication' in annotations and annotations['elucidation']:
            for e in annotations['elucidation']:
                descr.extend(['', 'ELUCIDATION:', e])
        if 'axiom' in annotations and annotations['axiom']:
            for e in annotations['axiom']:
                descr.extend(['', 'AXIOM:', e])
        if 'comment' in annotations and annotations['comment']:
            for e in annotations['comment']:
                descr.extend(['', 'COMMENT:', e])
        if 'example' in annotations and annotations['example']:
            for e in annotations['example']:
                descr.extend(['', 'EXAMPLE:', e])
        return '\n'.join(descr).strip()

    def save(self, *args, **kw):
        """Saves collection to storage."""
        self.coll.save(*args, **kw)


def main():
    e = EMMO2Meta()
    e.save('json', 'emmo2meta.json', 'mode=w')
    return e


if __name__ == '__main__':
    e = main()
    coll = e.coll
    onto = e.onto

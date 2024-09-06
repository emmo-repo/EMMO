#!/usr/bin/env python3
#
# This Python script generates the graphs in this directory from the
# EMMO owl sources using EMMO-python.
import sys
import os
from pathlib import Path

from ontopy import get_ontology
from ontopy.graph import OntoGraph
from ontopy.graph import (plot_modules, get_module_dependencies,
                          check_module_dependencies)
import owlready2


def add_children(parent, children):
    """Make sure that `children` are subclasses of `parent`.
    Also add `children` to global `all_children` set."""
    for child in children:
        if parent not in child.is_a:
            child.is_a.append(parent)
    all_children.update(children)


docdir = Path(__file__).absolute().parent
rootdir = docdir.parent


# Visualise EMMO top-level
top = get_ontology(str(rootdir / 'top' / 'top.ttl')).load()
entities = list(top.classes())  # FIXME - needed for correct reasoning
top.sync_reasoner()
g = OntoGraph(top, top.EMMO, relations='all', entities=entities)
#g.add_entities([owlready2.Thing, owlready2.Nothing], relations='all',
#               style='dashed')
g.add_legend()
g.save(str(docdir / 'top.png'))


# Load EMMO middle
middle = get_ontology(str(rootdir / 'middle' / 'middle.ttl')).load()
all_entities = list(middle.classes())  # FIXME - needed for reasoning
middle.sync_reasoner()
all_entities2 = list(middle.classes())  # FIXME - needed for reasoning


# Visualise EMMO middle-level, i.e. perspectives
# There seems to be problems with the reasoner. Add inferred subclasses manually
all_children = set()
add_children(middle.Physicalistic,
             [middle.Matter, middle.Field, middle.Particle])
add_children(middle.Reductionistic,
             [middle.State, middle.Existent])
add_children(middle.Semiotics,
             [middle.SemioticEntity, middle.Semiosis])
add_children(middle.Holistic,
             [middle.Whole, middle.Role])
add_children(middle.Persistence,
             [middle.Object, middle.Process])
add_children(middle.Perceptual,
             [middle.Visual, middle.Auditory, middle.Gustatory,
              middle.Olfactory, middle.Somatosensory])
g = OntoGraph(middle, root=middle.Perspective, leafs=all_children,
              relations='all', excluded_nodes=['Particle'])
g.add_legend()
g.save(str(docdir / 'perspective.png'))


# All of mid-level ontology
g = OntoGraph(middle, middle.Perspective, relations='all')
g.add_legend()
g.save(str(docdir / 'middle.png'))


# Representation of the standard model in the physicalistic branch
g = OntoGraph(middle, middle.Particle, relations='all')
g.add_legend()
g.save(str(docdir / 'particle.png'))


# Relation graph
g = OntoGraph(middle, middle.EMMORelation)
g.save(str(docdir / 'relations.png'))


# Visualise module dependencies (requires that we load the non-inferred
# ontology)
modules = get_module_dependencies(middle)
plot_modules(modules, filename=str(docdir / 'modules.png'))
check_module_dependencies(modules)

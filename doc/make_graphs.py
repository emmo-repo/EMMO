#!/usr/bin/env python3
#
# This Python script generates the graphs in this directory from the
# EMMO owl sources using EMMO-python.
import sys
import os

from emmo import get_ontology
from emmo.graph import OntoGraph
from emmo.graph import (plot_modules, get_module_dependencies,
                        check_module_dependencies)


# Default inferred ontology
emmo = get_ontology()
emmo.load()


# Visualise some core parts of EMMO
g = OntoGraph(emmo, emmo.EMMO, leafs=[emmo.Perspective, emmo.Elementary],
              relations='all', edgelabels=False)
g.add_legend()
g.save('top.png')


leafs = set()
for s in emmo.Perspective.subclasses():
    leafs.update(s.subclasses())
g = OntoGraph(emmo, emmo.Perspective, leafs=leafs, parents=1,
              relations='all', edgelabels=False)
g.add_legend()
g.save('perspectives.png')


leafs = {emmo.Interpreter, emmo.Conventional, emmo.Icon, emmo.Observation,
         emmo.Object}
exclude = {emmo.SIUnitSymbol, emmo.SpecialUnit, emmo.Manufacturing,
            emmo.Engineered, emmo.PhysicalPhenomenon}
g = OntoGraph(emmo)
g.add_branch(emmo.Holistic, leafs=leafs, exclude=exclude,
             relations='all', edgelabels=False)
g.add_legend()
g.save('semiotics.png')


# Visualise module dependencies (requires that we load the non-inferred
# ontology)
iri = 'http://emmo.info/emmo/1.0.0-alpha2'
onto = get_ontology(iri)
onto.load()

modules = get_module_dependencies(onto)
plot_modules(iri, filename='modules.png', modules=modules)
check_module_dependencies(modules)

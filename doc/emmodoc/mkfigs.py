#!/usr/bin/env python3
# Script for generating figures
import sys
import os

from emmo import get_ontology
from emmo.graph import (plot_modules, get_module_dependencies,
                        check_module_dependencies)


# Plot module dependencies
iri = 'http://emmo.info/emmo/1.0.0-beta2'
emmo = get_ontology(iri)
emmo.load()
modules = get_module_dependencies(emmo)
plot_modules(src=modules, filename='genfigs2/modules.png')
check_module_dependencies(modules)


#

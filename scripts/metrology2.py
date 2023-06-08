#!/usr/bin/env python
"""Python script that updates sidimensionalunits, unitsextension and
prefixedunits from QUDT.

Usage: python metrology2.py

This script simply add EMMO representations of units found in QUDT but
not in unitsextension. Missing dimensional units will be added to
sidimensionalunits. It will not overwrite manual changes to
sidimensionalunits, unitsextension and prefixedunits.

Hence, it is safe to manually edit sidimensionalunits, unitsextension
and prefixedunits and run this script multiple times.

"""
# pylint: disable=invalid-name
import json
import logging
import re
from logging import info
from pathlib import Path

import yaml

from ontopy import World
import owlready2

from tripper import Triplestore, Literal
from tripper import DCTERMS, EMMO, OWL, RDF, RDFS, XSD

from emmoutils import (
    en, as_preflabel, dimension_string, get_symbol, latex2text, htmlstrip,
    remove_python_name, set_turtle_prefix
)


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
thisdir = Path(__file__).resolve().parent
disciplinesdir = thisdir.parent / "disciplines"


# Declare datatypes (must be done before loading ontologies)
class double(float):
    """Python datatype for xsd:double."""

owlready2.declare_datatype(
    # pylint: disable=unnecessary-lambda
    double, XSD.double, lambda x: double(x), lambda v: str(v)
)


# Load metrology data
with open(thisdir / "metrology.yaml", "rt", encoding="utf-8") as f:
    metrology_data = yaml.safe_load(f)


# Create common world and load unitsextension into it
world = World()

onto_du = world.get_ontology(
    disciplinesdir / "sidimensionalunits.ttl"
).load()

onto_ue = world.get_ontology(
    disciplinesdir / "unitsextension.ttl"
).load()

onto_pu = world.get_ontology(
    disciplinesdir / "prefixedunits.ttl"
).load()

onto_pu.sync_python_names()


# Load QUDT units using tripper
qudtcache = thisdir / "qudt_cache.ttl"
ts = Triplestore(backend="rdflib")
if qudtcache.exists():
    info("loading QUDT from cache...")
    ts.parse(source=qudtcache)
else:
    info("loading QUDT web, caching...")
    ts.parse(source="http://qudt.org/2.1/vocab/unit")
    ts.parse(source="http://qudt.org/2.1/schema/qudt")
    ts.serialize(qudtcache)




# Create namespaces
QUDT = ts.bind("qudt", "http://qudt.org/schema/qudt/")
UNIT = ts.bind("unit", "http://qudt.org/vocab/unit/")

# All units
units = {
    u: u.qudtReference for u in onto_pu.classes(imported=True)
    if u.qudtReference
}





# Save ontologies
# ---------------
#remove_python_name(onto_du)
info("saving ontologies...")
onto_du.save(disciplinesdir / "sidimensionalunits.ttl", format="turtle", overwrite=True)
onto_pu.save(disciplinesdir / "prefixedunits.ttl", format="turtle", overwrite=True)
onto_ue.save(disciplinesdir / f"unitsextension.ttl", format="turtle", overwrite=True)


set_turtle_prefix(disciplinesdir / "sidimensionalunits.ttl", EMMO, EMMO)
set_turtle_prefix(disciplinesdir / "prefixedunits.ttl", EMMO, EMMO)
set_turtle_prefix(disciplinesdir / "unitsextension.ttl", EMMO, EMMO)


# Replace all owl:hasValue from decimal to xsd:double
if False:
    with open(disciplinesdir / "unitsextension.ttl", "rt") as f:
        lines = [
            re.sub(
                r"owl:hasValue +([0-9.]+)(\s|$)",
                r'owl:hasValue "\1"^^xsd:double ',
                line
            ) for line in f
        ]

    with open(disciplinesdir / "unitsextension.ttl", "wt") as f:
        for line in lines:
            f.write(line)

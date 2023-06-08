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
    remove_python_name, replace, set_turtle_prefix, get_metricprefix_value,
    get_siconversion_multiplier, get_siconversion_offset,
    has_siconversion_multiplier, has_siconversion_offset
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

skos = world['http://www.w3.org/2004/02/skos/core#prefLabel'].namespace
skos.prefix = "skos"
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


onto = onto_pu

# Create namespaces
QUDT = ts.bind("qudt", "http://qudt.org/schema/qudt/")
UNIT = ts.bind("unit", "http://qudt.org/vocab/unit/")

# Maps unit to QUDT reference
units = {
    u: u.qudtReference for u in onto_pu.classes(imported=True)
    if u.qudtReference
}
exclude = [
    onto.Quantity,
    onto.DimensionlessUnit,
    onto.UnitOne,
    onto.LogarithmicUnit,
    onto.CountingUnit,
]
for u in exclude:
    del units[u]


# Maps preflabel to unit
preflabels = {u.prefLabel.first(): u for u in units}


corrected_preflabels = metrology_data["corrected_preflabels"]
prefixes = metrology_data["prefixes"]
metric_prefixes = {onto[p]: get_metricprefix_value(onto[p]) for p in prefixes}
siunits = set(
    u.prefLabel.first() for u in
    onto.SIBaseUnit.disjoint_unions[0] + onto.SISpecialUnit.disjoint_unions[0]
)



# Correct preflabels
# Each component should start with a big case.
# Trailing "s"'s after a prefixed unit are removed.
if True:  # pylint: disable=using-constant-test
    for unit in units:
        preflabel = unit.prefLabel.first()
        unit.prefLabel = en(preflabel)
        if preflabel.startswith((
                "Cal_", "Bu_", "Btu", "Bbl_", "Gi_", "M2_",
                 "Oz_", "Pk_", "Qt_", "Ton_", "W_M2",
        )):
            continue
        if unit in siunits or unit in metric_prefixes:
            continue
        prefixed = False
        coherent = True

        tokens = re.findall("[A-ZÅ][a-zö0-9_]*", preflabel)
        power = 1
        mult = 1.0
        known = True
        for i, token in enumerate(tokens):
            if token in siunits:
                pass
            elif token in prefixes:
                prefixed = True
                coherent = False
                prefix = onto[token]
                mult *= metric_prefixes[prefix]**power
            elif token in {"Number"}:
                pass
            elif token in {"Per", "Inverse", "Reciprocal"}:
                power = -1
            elif token == "Square":
                if not tokens[i+1] in onto:
                    known = False
                    break
                u = onto[tokens[i+1]]
                if u in metric_prefixes:
                    mult *= metric_prefixes[u]**power
                    if not tokens[i+2] in onto:
                        known = False
                        break
                    u = onto[tokens[i+2]]
                mult *= get_siconversion_multiplier(u)**power
            elif token == "Cubic":
                if not tokens[i+1] in onto:
                    known = False
                    break
                u = onto[tokens[i+1]]
                if u in metric_prefixes:
                    mult *= metric_prefixes[u]**(2*power)
                    if not tokens[i+2] in onto:
                        known = False
                        break
                    u = onto[tokens[i+2]]
                mult *= get_siconversion_multiplier(u)**(2*power)
            elif token == "Squared":
                print("Unexpected unit token '{token}' in '{preflabel}'")
            elif token in onto:
                coherent = False
                u = onto[token]
                if issubclass(u, onto.DimensionlessUnit):
                    pass
                elif has_siconversion_multiplier(u):
                    mult *= get_siconversion_multiplier(u)**power
                else:
                    print(f"*** cannot convert: {preflabel}: {u}")
            else:
                known = False
                if not has_siconversion_multiplier(unit):
                    print(f"*** unknown: {preflabel}: {token}")
                break

        print(f"--- {preflabel}: {known=}, {prefixed=}, {coherent=}, {mult=}")

        if known:
            if not has_siconversion_multiplier(unit):
                unit.is_a.append(onto.hasSIConversionMultiplier.value(mult))

                if not has_siconversion_offset(unit):
                    unit.is_a.append(onto.hasSIConversionOffset.value(0.0))

        #hasMult = hasOff = False
        #for r in unit.is_a:
        #    if isinstance(r, owlready2.Restriction):
        #        if r.property == onto.hasSIConversionMultiplier:
        #            hasMult = True
        #        if r.property == onto.hasSIConversionOffset:
        #            hasOff = True
        #if not hasMult or not hasOff:
        #    print("*x*", preflabel, hasMult, hasOff)


# Save ontologies
# ---------------
info("saving ontologies...")
remove_python_name(onto_du)

onto_du.save(disciplinesdir / "sidimensionalunits.ttl", format="turtle", overwrite=True)
onto_ue.save(disciplinesdir / "unitsextension.ttl", format="turtle", overwrite=True)
onto_pu.save(disciplinesdir / "prefixedunits.ttl", format="turtle", overwrite=True)

set_turtle_prefix(disciplinesdir / "sidimensionalunits.ttl", EMMO,
                  EMMO / "disciplines/sidimensionalunits")
set_turtle_prefix(disciplinesdir / "unitsextension.ttl", EMMO,
                  EMMO / "disciplines/unitsextension")
set_turtle_prefix(disciplinesdir / "prefixedunits.ttl", EMMO,
                  EMMO / "disciplines/prefixedunits")

# Correct prefixes
prefixfix = {"core:": "skos:", "term:": "dcterms:"}
replace(disciplinesdir / "sidimensionalunits.ttl", prefixfix)
replace(disciplinesdir / "unitsextension.ttl", prefixfix)
replace(disciplinesdir / "prefixedunits.ttl", prefixfix)

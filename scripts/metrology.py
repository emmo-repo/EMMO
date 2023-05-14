#!/usr/bin/env python
"""Python script that updates sidimensionalunits and unitsextension from QUDT.

Usage: python metrology.py

This script simply add EMMO representations of units found in QUDT but
not in unitsextension. Missing dimensional units will be added to
sidimensionalunits. It will not overwrite manual changes to
sidimensionalunits and unitsextension.

Hence, it is safe to manually edit sidimensionalunits and
unitsextension and run this script multiple times.

"""
import json
import logging
import re
from logging import info
from pathlib import Path
from uuid import uuid4

from ontopy import World
import owlready2

from tripper import Triplestore, Literal
from tripper import DCTERMS, EMMO, OWL, RDF, RDFS, XSD


#logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
thisdir = Path(__file__).resolve().parent
disciplinesdir = thisdir.parent / "disciplines"


def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


def as_preflabel(s):
    """Return dimensional string `s` as a valid prefLabel."""
    table = str.maketrans("()-", "___")
    table.update((ord(c), None) for c in " ^?.\xa0")
    preflabel = s.title().translate(table).replace(
        "\xc3\xa5Ngstr\xe3\xb6M", "Angstrom"
    )
    if not preflabel.isidentifier():
        raise ValueError(f"Cannot convert '{s}' to preflabel.")
    return preflabel


def dimension_string(dimvec):
    """Convert QUDT dimension vection to EMMO dimension string."""
    d = dict(re.findall("([A-Z])(-?[0-9]+)", dimvec))
    return " ".join(f"{e}{int(d[q]):+}" for e, q in zip(
        "TLMI\u0398NJ", "TLMEHAI")).replace("+0", "0")


def get_symbol(unit):
    """Return the symbol string for `unit` or None if `unit` has no symbol."""
    if unit.unitSymbol:
        return unit.unitSymbol.first()
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasSymbolData):
            return r.value
    return None


# Declare datatypes (must be done before loading ontologies)
class double(float):
    """Python datatype for xsd:double."""

owlready2.declare_datatype(
    double, XSD.double, lambda x: double(x), lambda v: str(v)
)


# Load metrology data
with open(thisdir / "metrology.json", "rt") as f:
    metrology_data = json.load(f)


# Create common world and load unitsextension into it
world = World()
du = world.get_ontology(
    disciplinesdir / "sidimensionalunits.ttl"
).load()
onto = world.get_ontology(
    disciplinesdir / "unitsextension.ttl"
).load()
onto.sync_python_names()

# Load QUDT units using tripper
ts = Triplestore(backend="rdflib")
ts.parse(source="http://qudt.org/2.1/vocab/unit")
ts.parse(source="http://qudt.org/2.1/schema/qudt")

# Create namespaces
QUDT = ts.bind("qudt", "http://qudt.org/schema/qudt/")
UNIT = ts.bind("unit", "http://qudt.org/vocab/unit/")


# Map dimensional string to dimensional unit class - will be extended
dimensional_units = {
    c.equivalent_to[0].value: c
    for c in onto.SIDimensionalUnit.subclasses()
}
dimensional_units["T0 L0 M0 I0 \u03980 N0 J0"] = onto.DimensionlessUnit

# Map dimensional string to old physical dimension IRI and preflabel
physical_dimensions = metrology_data["physical_dimensions"]

# All existing unit symbols
symbols = set(get_symbol(unit) for unit in onto.MeasurementUnit.descendants())
symbols.remove(None)

# Map QUDT unit IRI to corresponding Owlready2 class
units = {}

# Map names to corresponding symbol. Ex: {"Kilo": "k", ...}
prefixes = {
    prefix: (onto[prefix+"PrefixedUnit"] if prefix+"PrefixedUnit" in onto
             else None, symbol)
    for prefix, symbol in metrology_data["prefixes"].items()
}


# QUDT units to skip
qudt_skip = metrology_data["qudt_skip"]

# Corrected symbols that are wrong in QUDT...
corrected_qudt_symbols = {
    "Picometre": "pm",
}

# Corrected preflabels (will be further populated...)
corrected_preflabels = {
    "MilliW": "MilliWatt",
    "MicroM3": "CubicMicroMetre",
    "Angstrom": "Ångström",
}


# Extend dimensional_units from physical_dimensions
for dimstr in set(physical_dimensions).difference(set(dimensional_units)):
    d = physical_dimensions[dimstr]
    iri = d["iri"]
    if not world[iri]:
        preflabel = d["preflabel"]
        dim = du.new_entity(iri, (onto.SIDimensionalUnit, ))
        dim.prefLabel = en(preflabel.replace("Dimension", "Unit"))
        dim.iri = iri
        dim.equivalent_to.append(onto.hasDimensionString.value(dimstr))
        dimensional_units[dimstr] = dim


# ==================================================

# Loop over all units in QUDT and add them to `onto` if they are
# not already in the ontology
for qudtunit in ts.subjects(RDF.type, QUDT.Unit):
    if qudtunit in qudt_skip:
        continue

    # Infer the superclasses of current unit
    bases = set()
    for parent in ts.objects(qudtunit, RDF.type):
        if parent == QUDT.DerivedUnit:
            bases.add(onto.DerivedUnit)
        if parent == QUDT.DerivedCoherentUnit:
            bases.add(onto.SICoherentUnit)
        if parent == QUDT["SI-Unit"]:
            bases.add(onto.SIUnit)
        if parent == QUDT.ScaledUnit:
            bases.add(onto.PrefixedUnit)
        if parent == QUDT.CountingUnit:
            bases.add(onto.PureNumberUnit)
        if parent == QUDT.DimensionLessUnit:
            bases.add(onto.DimensionLessUnit)
        if parent == QUDT.LogarithmicUnit:
            bases.add(onto.LogarithmicUnit)
    if not bases:
        bases.add(onto.MeasurementUnit)
    if onto.PureNumberUnit in bases and onto.UnitOne in bases:
        bases.remove(onto.UnitOne)

    # Fetch some annotations from QUDT
    label = ts.value(qudtunit, RDFS.label, any=True, lang="en")
    if not label:
        label = ts.value(qudtunit, RDFS.label, any=True)
    if label and "(" not in label:
        prefLabel = as_preflabel(label)
    else:
        prefLabel = as_preflabel(qudtunit.rsplit("/", 1)[-1])

    if prefLabel in corrected_qudt_symbols:
        symbol = corrected_qudt_symbols[prefLabel]
    else:
        symbol = ts.value(qudtunit, QUDT.symbol)

    isReplacedBy = ts.value(qudtunit, DCTERMS.isReplacedBy)
    if isReplacedBy:
        info(f"replaced, skipping: {prefLabel} ({symbol})")
        continue

    if prefLabel in onto:
        info(f"exists, skipping:   {prefLabel} ({symbol})")
        if prefLabel in onto:
            units[qudtunit] = onto[prefLabel]
        continue

    qudt_descr = ts.value(qudtunit, QUDT.plainTextDescription)
    dc_descr = ts.value(qudtunit, DCTERMS.description)

    isDefinedBy = ts.value(qudtunit, RDFS.isDefinedBy)

    # Determine conversion multiplier and offset
    mult = ts.value(qudtunit, QUDT.conversionMultiplier)
    offset = ts.value(qudtunit, QUDT.conversionOffset)
    if ((mult is not None and float(mult) != 1.0) or
        (offset is not None and float(offset) != 0.0)):
        if onto.SICoherentUnit in bases:
            raise RuntimeError(
                f"SICoherentUnit cannot have multiplier: {qudtunit}"
            )
        bases.add(onto.SINonCoherentUnit)

    # Physical dimension - creating new if it doesn't already exists
    dimiri = ts.value(qudtunit, QUDT.hasDimensionVector)
    dimstr = dimension_string(dimiri.rsplit("/", 1)[-1])
    if dimstr not in dimensional_units:
        if dimstr in physical_dimensions:
            iri = physical_dimensions[dimstr].get("iri", EMMO[f"EMMO_{uuid4()}"])
            name = physical_dimensions[dimstr]["preflabel"].replace("Dimension", "Unit")
        else:
            iri = EMMO[f"EMMO_{uuid4()}"]
            kind = ts.value(qudtunit, QUDT.hasQuantityKind, any=True)
            tr = str.maketrans("-\u0398", "_H")
            tr.update((ord(c), None) for c in " +")
            name = (
                kind.rsplit("/", 1)[-1] + "Unit" if kind
                else dimstr.translate(tr)
            )
        if not world[iri]:
            dim = du.new_entity(iri, (onto.SIDimensionalUnit, ))
            dim.prefLabel = en(name)
            dim.iri = iri
            dim.equivalent_to.append(onto.hasDimensionString.value(dimstr))
            dimensional_units[dimstr] = dim

    # Create new unit and assign properties and restrictions
    unit = onto.new_entity(prefLabel, bases)
    units[qudtunit] = unit
    if qudt_descr:
        unit.elucidation.append(en(str(qudt_descr)))
    elif dc_descr:
        unit.elucidation.append(en(str(dc_descr)))
    unit.prefLabel.append(en(prefLabel))
    if prefLabel != label:
        unit.altLabel.append(en(label))
    if symbol:
        unit.unitSymbol = str(symbol)
        if issubclass(unit, onto.UnitSymbol):
            unit.is_a.append(onto.hasSymbolData.value(str(symbol)))

    unit.is_a.append(dimensional_units[dimstr])
    if onto.SINonCoherentUnit in bases and float(mult) != 0.0:
        unit.is_a.append(onto.hasConversionMultiplier.value(
            1.0 if mult is None else float(mult)))
        unit.is_a.append(onto.hasConversionOffset.value(
            0.0 if offset is None else float(offset)))
    unit.qudtReference.append(qudtunit)
    if isDefinedBy:
        unit.isDefinedBy.append(isDefinedBy)

    for ucumCode in ts.objects(qudtunit, QUDT.ucumCode):
        unit.ucumCode.append(str(ucumCode))

    for ref in ts.objects(qudtunit, QUDT.informativeReference):
        ref = str(ref)
        if "wikipedia" in ref:
            unit.wikipediaReference = ref
        elif "dbpedia" in ref:
            unit.dbpediaReference = ref
        elif "iupac" in ref:
            unit.iupacReference = ref
        else:
            unit.seeAlso = ref


# Make LogarithmicUnit a subclass of DimensionlessUnit instead of UnitOne
onto.LogarithmicUnit.is_a = [onto.DimensionlessUnit]


# Relate prefixed units to their prefix and base unit
for unit in units.values():
    prefLabel = unit.prefLabel.first()
    symbol = unit.unitSymbol.first()
    if symbol:
        for prefix, (prefixunit, s) in prefixes.items():
            if prefLabel.startswith(prefix) and symbol.startswith(s):
                if prefixunit in unit.is_a:
                    break
                if onto.DerivedUnit in unit.is_a:
                    unit.is_a.remove(onto.DerivedUnit)
                if onto.MeasurementUnit in unit.is_a:
                    unit.is_a.remove(onto.MeasurementUnit)
                if prefixunit:
                    unit.is_a.append(prefixunit)
                n = len(prefix)
                refname = prefLabel[n].upper() + prefLabel[n+1:]

                # Hmm, QUDT sometimes add a extra "s", like "KiloMolesPerSecond"
                # instead of "KiloMolePerSecond" - strip that "s" off
                m = re.match("^([A-Z][a-z]*?)s?([A-Z].*)?$", refname)
                if m:
                    g0, g1 = m.groups()
                    refname = "".join(m.groups()) if g1 else g0

                if refname in onto:
                    refunit = onto[refname]
                    if get_symbol(refunit) == symbol[len(s):]:
                        unit.is_a.append(onto.hasReferenceUnit.some(refunit))
                break


# QUDT marks some prefixed units as derived units. Ex: AttoCoulomb.
# Remove such inconsistencies!
for unit in onto.DerivedUnit.descendants():
    if onto.DerivedUnit in unit.is_a:
        for r in unit.is_a:
            if r in (onto.SINonCoherentUnit, onto.PrefixedUnit):
                info(f"fix QUDT inconsistency, make non-derived unit: {unit}")
                unit.is_a.remove(onto.DerivedUnit)
                break


# Add deprecated classes with old IRIs
for preflabel, d in metrology_data["units"].items():
    iri, s = d['iri'], d['symbol']
    if not world[iri]:
        name = iri.split("#", 1)[1]
        new = onto.new_entity(name, (owlready2.Thing, ))
        new.deprecated = True
        new.isReplacedBy.append(onto[preflabel].iri)


# Correct preflabels
# Each component should start with a big case.
# Trailing "s"'s after a prefixed unit are removed.
for unit in units.values():
    prefLabel = unit.prefLabel.first()
    if prefLabel in {"Ångström", }:
        continue
    if prefLabel in corrected_preflabels:
        unit.prefLabel = [corrected_preflabels[prefLabel]]
    else:
        newlabel = []
        for s in re.findall("[A-Z][a-z0-9_]*", prefLabel):
            for prefix in prefixes.keys():
                if s.startswith(prefix):
                    newlabel.append(prefix)
                    s = s[len(prefix):].title()
                    break
            if s in onto:
                newlabel.append(s)
            elif s.endswith("s") and s[:-1] in onto:
                newlabel.append(s[:-1])
            else:
                newlabel.append(s)
        unit.prefLabel = ["".join(newlabel)]


# Correct QUDT errors
# -------------------
# Mobility has wrong dimensionality.  We have already added ElectricMobility
# with the correct dimensionality.  Just get rid of MobilityUnit
if 'MobilityUnit' in du:
    owlready2.destroy_entity(du.MobilityUnit, True)


# Save ontologies
# ---------------
onto.save(disciplinesdir / f"unitsextension.ttl", format="turtle", overwrite=True)
du.save(disciplinesdir / "sidimensionalunits.ttl", format="turtle", overwrite=True)

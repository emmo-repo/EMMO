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
# pylint: disable=invalid-name
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

from emmoutils import (
    en, as_preflabel, dimension_string, get_symbol, latex2text, htmlstrip,
    remove_python_name, set_turtle_prefix
)


#logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
thisdir = Path(__file__).resolve().parent
disciplinesdir = thisdir.parent / "disciplines"


# Corrected preflabels. Maps QUDT label to correct prefLabel
corrected_preflabels = {
    "MilliW": "MilliWatt",
    "MicroM3": "CubicMicroMetre",
    "Angstrom": "Ångström",
    "AU": "AstronomicalUnit",
    "Absiemen": "Absiemens",
    "Kilopond": "KiloPond",
    "CubicCentimeterPerMoleSecond": "CubicCentiMetrePerMoleSecond",
    "PicofaradPerMetre": "PicoFaradPerMetre",
}

# Corrected symbols that are wrong in QUDT...
corrected_qudt_symbols = {
    "Picometre": "pm",
}


# Declare datatypes (must be done before loading ontologies)
class double(float):
    """Python datatype for xsd:double."""

owlready2.declare_datatype(
    # pylint: disable=unnecessary-lambda
    double, XSD.double, lambda x: double(x), lambda v: str(v)
)


# Load metrology data
with open(thisdir / "metrology.json", "rt", encoding="utf-8") as f:
    metrology_data = json.load(f)


# Create common world and load unitsextension into it
world = World()

du = world.get_ontology(
    disciplinesdir / "sidimensionalunits.ttl"
).load()

pu = world.get_ontology(
    disciplinesdir / "prefixedunits.ttl"
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

# Map prefix names to corresponding symbol. Ex: {"Kilo": "k", ...}
prefixes = {
    prefix: (onto[prefix+"PrefixedUnit"] if prefix+"PrefixedUnit" in onto
             else None, symbol)
    for prefix, symbol in metrology_data["prefixes"].items()
}


# QUDT units to skip
qudt_skip = metrology_data["qudt_skip"]

# QUDT IRIs of units already loaded from QUDT
existing_qudtiris = {
    c.qudtReference.first() for c in onto.classes() if hasattr(c, "qudtReference")
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
        r = onto.hasDimensionString.value(dimstr)
        if r not in dim.equivalent_to:
            dim.equivalent_to.append(r)
        dimensional_units[dimstr] = dim


# ==================================================

# Loop over all units in QUDT and add them to `onto` if they are
# not already in the ontology
for qudtunit in ts.subjects(RDF.type, QUDT.Unit):
    if qudtunit in qudt_skip or qudtunit in existing_qudtiris:
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
    if prefLabel in corrected_preflabels:  # pylint: disable=consider-using-get
        prefLabel = corrected_preflabels[prefLabel]

    symbol = corrected_qudt_symbols.get(
        prefLabel, ts.value(qudtunit, QUDT.symbol)
    )

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
            r = onto.hasDimensionString.value(dimstr)
            if r not in dim.equivalent_to:
                dim.equivalent_to.append(r)
            dimensional_units[dimstr] = dim

    # Create new unit and assign properties and restrictions
    unit = onto.new_entity(prefLabel, bases)
    units[qudtunit] = unit
    if qudt_descr or dc_descr:
        descr = htmlstrip(latex2text(qudt_descr or dc_descr))
        unit.elucidation.append(en(descr + "\n\n-- QUDT"))
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
                        unit.is_a.append(onto.hasMetrologicalReference.some(refunit))
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


# Add deprecated classes with old IRIs - moved to separate ontology
if False:  # pylint: disable=using-constant-test
    for preflabel, d in metrology_data["units"].items():
        iri, s = d['iri'], d['symbol']
        if not world[iri]:
            name = iri.split("#", 1)[1]
            new = onto.new_entity(name, (owlready2.Thing, ))
            new.deprecated = True
            new.isReplacedBy.append(onto[preflabel].iri)


# Correct preflabels -- should not be needed any more...
# Each component should start with a big case.
# Trailing "s"'s after a prefixed unit are removed.
if False:  # pylint: disable=using-constant-test
    for unit in units.values():
        prefLabel = unit.prefLabel.first()
        if prefLabel in {"Ångström", }:
            continue
        unit.prefLabel.clear()
        if prefLabel in corrected_preflabels:
            unit.name = corrected_preflabels[prefLabel]
            unit.prefLabel.append(en(corrected_preflabels[prefLabel]))
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
            label = "".join(newlabel)
            unit.name = label
            unit.prefLabel.append(en(label))


# Add description with citations - should not be needed any more...
if False:  # pylint: disable=using-constant-test
    for qudtunit, unit in units.items():
        qudt_descr = ts.value(qudtunit, QUDT.plainTextDescription)
        dc_descr = ts.value(qudtunit, DCTERMS.description)
        unit = onto[unit.prefLabel.first()]
        if (qudt_descr or dc_descr) and (
                not unit.elucidation or
                unit.elucidation.first() in (qudt_descr, dc_descr)
        ):
            descr = htmlstrip(latex2text(qudt_descr or dc_descr))
            unit.elucidation.clear()
            unit.elucidation.append(en(descr + "\n\n-- QUDT"))


# Rename classes - should not be needed any more...
if False:  # pylint: disable=using-constant-test
    ignored = "Ångström", "CGSUnit", "SIAcceptedSpecialUnit", "OffSystemUnit"
    for cls in onto.classes():
        preflabel = cls.prefLabel.first()
        if preflabel != cls.name:
            if preflabel not in ignored:
                cls.name = preflabel


# Change hasMetrologicalReference to hasUnitSymbol for prefixed units
if False:  # pylint: disable=using-constant-test
    ignored = "CGSUnit", "SIAcceptedSpecialUnit", "OffSystemUnit"
    for unit in onto.classes():
        if unit in ignored:
            continue
        if unit.name.startswith("Ab"):
            refname = unit.name[2].upper() + unit.name[3:]
            if refname in onto:
                ref = onto.hasUnitSymbol.some(onto[refname])
                if ref not in unit.is_a:
                    unit.is_a.append(ref)
            else:
                info(f"*** Missing unit symbol '{refname}' for '{unit.name}")
        else:
            for prefix in prefixes.keys():
                if unit.name.startswith(prefix):
                    for i, r in enumerate(unit.is_a):
                        if (isinstance(r, owlready2.Restriction) and
                            r.property == onto.hasMetrologicalReference):
                            unit.is_a[i] = onto.hasUnitSymbol.some(r.value)
                            break
                    else:
                        n = len(prefix)
                        refname = unit.name[n].upper() + unit.name[n+1:]
                        if refname in onto:
                            ref = onto.hasUnitSymbol.some(onto[refname])
                            if ref not in unit.is_a:
                                unit.is_a.append(ref)
                        else:
                            info(f"*** Missing unit symbol '{refname}' "
                                 "for '{unit.name}")


# Move prefixed units to an own ontology - should not be needed any more...
if True:  # pylint: disable=using-constant-test
    disjoint_unions = set()
    disjoints = set()
    for cls in onto.classes():
        preflabel = cls.prefLabel.first()
        for prefix in prefixes.keys():
            if preflabel.startswith(prefix):
                with pu:
                    new = pu.new_entity(cls.name, (owlready2.Thing,))
                for k, v in cls.get_annotations().items():
                    getattr(new, k).extend(v)
                new.equivalent_to.extend(cls.equivalent_to)
                new.is_a.extend(cls.is_a)
                new.disjoint_unions.extend(cls.disjoint_unions)

                for d in cls.disjoint_unions:
                    disjoint_unions.add(c.prefLabel.first() for c in d)
                for d in cls.disjoints():
                    names = set(c.prefLabel.first() for c in d)
                    names.add(preflabel)
                    disjoints.add(names)

    for names in disjoints.difference(disjoint_unions):
        with pu:
            owlready2.AllDisjoint(pu[name] for name in names)
    for unit in pu.classes():
        #print("***", unit)
        preflabel = unit.prefLabel.first()
        with onto:
            owlready2.destroy_entity(onto[preflabel])



# Correct QUDT errors
# -------------------
# Mobility has wrong dimensionality.  We have already added ElectricMobility
# with the correct dimensionality.  Just get rid of MobilityUnit
if 'MobilityUnit' in du:
    owlready2.destroy_entity(du.MobilityUnit, True)


# Save ontologies
# ---------------
remove_python_name(du)

du.save(disciplinesdir / "sidimensionalunits.ttl", format="turtle", overwrite=True)
pu.save(disciplinesdir / "prefixedunits.ttl", format="turtle", overwrite=True)
onto.save(disciplinesdir / f"unitsextension.ttl", format="turtle", overwrite=True)


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

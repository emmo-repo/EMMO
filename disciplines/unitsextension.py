#!/usr/bin/env python
"""Python script that generates unitsextension.ttl from QUDT.
"""
import re
import logging
from logging import info
from pathlib import Path

from ontopy import World, get_ontology
import owlready2

from tripper import Triplestore
from tripper import DCTERMS, OWL, RDF, RDFS, XSD


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
thisdir = Path(__file__).resolve().parent


def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


def as_preflabel(s):
    """Return `s` as a valid prefLabel."""
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
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasSymbolData):
            return r.value
    return None


def prefix_value(prefix):
    """Return a `(label, symbol)` tuple for `prefix`."""
    symbol, value = None, None
    for r in prefix.is_a:
        if isinstance(r, owlready2.Restriction):
            #if str(r.property) == "Inverse(emmo.hasVariable)":
            #    value = r.value.value
            if r.property == onto.hasSymbolData:
                #symbol = r.value
                return (prefix.prefLabel.first(), r.value)
    #return (prefix.prefLabel.first(), (symbol, value))
    raise TypeError(f"invalid prefix: {prefix}")



# Declare datatypes (must be done before loading ontologies)
class double(float):
    """Represents xsd:double."""

owlready2.declare_datatype(double, XSD.double, lambda x: double(x), lambda v: str(v))


# Create common world and load unitsextension into it
world = World()
unitsextension = world.get_ontology(thisdir / "unitsextension.ttl").load()

# Create new ontology
ontology_name = "qudtunits"
base_iri = f"http://emmo.info/emmo/disciplines/{ontology_name}#"
onto = world.get_ontology(base_iri)
onto.base_iri = base_iri
onto.imported_ontologies.append(unitsextension)
onto.sync_python_names()

# Load QUDT units using tripper
ts = Triplestore(backend="rdflib")
ts.parse(source="http://qudt.org/2.1/vocab/unit")
ts.parse(source="http://qudt.org/2.1/schema/qudt")

# Create namespaces
QUDT = ts.bind("qudt", "http://qudt.org/schema/qudt/")
UNIT = ts.bind("unit", "http://qudt.org/vocab/unit/")

owl = world.get_ontology(str(OWL))
with owl:
    class sameAs(owlready2.Property):
        """The property that determines that two given individuals
        are equal."""

with onto:
    class hasConversionMultiplier(owlready2.AnnotationProperty):
        """A factor to multiply the numerical part of a quantity with
        when converting it into a SI-coherent unit."""
        domain = [onto.SINonCoherentUnit]
        range = [double]

    class hasConversionOffset(owlready2.AnnotationProperty):
        """An offset to add to the numerical part of a quantity
        when converting it into a SI-coherent unit."""
        domain = [onto.SINonCoherentUnit]
        range = [double]

    class hasMetricPrefix(onto.hasSpatialTile):
        """Relates a prefixed unit to its unit prefix."""
        domain = [onto.PrefixedUnit]
        range = [onto.MetricPrefix]


# All existing physical dimensions - will be extended
physical_dimensions = {
    c.equivalent_to[0].value: c
    for c in onto.PhysicalDimension.subclasses()
}

# All existing unit symbols
symbols = set(get_symbol(unit) for unit in onto.MeasurementUnit.descendants())
symbols.remove(None)

# Maps QUDT IRI to corresponding Owlready2 class
units = {}

prefixes = dict(
    prefix_value(p) for p in onto.SIMetricPrefix.disjoint_unions[0]
)



# Loop over all units in QUDT and add them to `onto` if they not already
# exists
for qudtunit in ts.subjects(RDF.type, QUDT.Unit):
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
            bases.add(onto.UnitOne)
        if parent == QUDT.LogarithmicUnit:
            bases.add(onto.LogarithmicUnit)
    if not bases:
        bases.add(onto.MeasurementUnit)

    label = ts.value(qudtunit, RDFS.label, any=True, lang="en")
    if not label:
        label = ts.value(qudtunit, RDFS.label, any=True)
    if label and "(" not in label:
        prefLabel = as_preflabel(label)
    else:
        prefLabel = as_preflabel(qudtunit.rsplit("/", 1)[-1])

    symbol = ts.value(qudtunit, QUDT.symbol)

    isReplacedBy = ts.value(qudtunit, DCTERMS.isReplacedBy)
    if isReplacedBy:
        info(f"replaced, skipping: {prefLabel} ({symbol})")
        continue

    if prefLabel in onto or symbol in symbols:
        info(f"exists, skipping:   {prefLabel} ({symbol})")
        if prefLabel in onto:
            units[qudtunit] = onto[prefLabel]
        continue

    qudt_descr = ts.value(qudtunit, QUDT.plainTextDescription)
    dc_descr = ts.value(qudtunit, DCTERMS.description)

    isDefinedBy = ts.value(qudtunit, RDFS.isDefinedBy)

    mult = ts.value(qudtunit, QUDT.conversionMultiplier)
    offset = ts.value(qudtunit, QUDT.conversionOffset)
    if ((mult is not None and float(mult) != 1.0) or
        (offset is not None and float(offset) != 0.0)):
        if onto.SICoherentUnit in bases:
            raise RuntimeError(
                f"SICoherentUnit cannot have multiplier: {qudtunit}"
            )
        bases.add(onto.SINonCoherentUnit)

    dimiri = ts.value(qudtunit, QUDT.hasDimensionVector)
    dimstr = dimension_string(dimiri.rsplit("/", 1)[-1])
    if dimstr not in physical_dimensions:
        kind = ts.value(qudtunit, QUDT.hasQuantityKind, any=True)
        tr = str.maketrans("-\u0398", "_H")
        tr.update((ord(c), None) for c in " +")
        name = (
            kind.rsplit("/", 1)[-1] + "Dimension" if kind
            else dimstr.translate(tr)
        )
        dim = onto.new_entity(name, (onto.PhysicalDimension, ))
        dim.hasSymbolData = dimstr
        physical_dimensions[dimstr] = dim

    unit = onto.new_entity(prefLabel, bases)
    units[qudtunit] = unit
    if qudt_descr:
        unit.elucidation.append(en(str(qudt_descr)))
    elif dc_descr:
        unit.elucidation.append(en(str(dc_descr)))
    unit.prefLabel.append(en(prefLabel))
    unit.altLabel.append(en(label))
    unit.is_a.append(onto.hasSymbolData.value(str(symbol)))
    unit.is_a.append(onto.hasPhysicalDimension.some(physical_dimensions[dimstr]))
    if onto.SINonCoherentUnit in bases:
        unit.hasConversionMultiplier = [1.0 if mult is None else float(mult)]
        unit.hasConversionOffset = [0.0 if offset is None else float(offset)]
    unit.qudtReference.append(qudtunit)
    if isDefinedBy:
        unit.isDefinedBy.append(isDefinedBy)

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


# Adding sameAs relations
for qudtunit, unit in units.items():
    for same in ts.objects(qudtunit, OWL.sameAs):
        if same in units:
            unit.sameAs = [units[same].iri]


# Relate prefixed units to their prefix and base unit
for unit in units.values():
    prefLabel = unit.prefLabel.first()
    symbol = get_symbol(unit)
    for prefix, s in prefixes.items():
        if prefLabel.startswith(prefix) and symbol.startswith(s):
            n = len(prefix)
            refname = prefLabel[n].upper() + prefLabel[n+1:]
            if refname in onto:
                refunit = onto[refname]
                if get_symbol(refunit) == symbol[len(s):]:
                    unit.is_a.append(onto.PrefixedUnit)
                    unit.hasMetricPrefix.append(onto[prefix])
                    unit.hasReferenceUnit.append(refunit)
            break



# Convert class docstrings to rdfs:comment
onto.sync_attributes(name_policy=None)


# Add metadata
version = unitsextension.get_version()
version_iri = f"http://emmo.info/emmo/{version}/disciplines/{ontology_name}"
onto.set_version(version_iri=version_iri)


onto.set_version(
    version=version,
    version_iri=f"{onto.base_iri.rstrip('/#')}/{version}",
)
abstract = en(
    "The module 'unitsextension' defines all units in EMMO perspectives "
    "that are not included in the 'siumits' module."
)
onto.metadata.title.append(en("Units extension"))
onto.metadata.abstract.append(abstract)
onto.metadata.creator.append(en("Simon Clark, SINTEF, NO"))
onto.metadata.creator.append(en("Jesper Friis, SINTEF, NO"))
onto.metadata.creator.append(en("Emanuele Ghedini, University of Bologna, IT"))
onto.metadata.creator.append(en("Gerhard Goldbeck, Goldbeck Consulting Ltd, UK"))
onto.metadata.creator.append(en("Adham Hashibon, UCL, UK"))
onto.metadata.creator.append(en("Georg J. Schmitz, ACCESS, GE"))

onto.metadata.license.append(en(
    'https://creativecommons.org/licenses/by/4.0/legalcode'))
onto.metadata.versionInfo.append(en(version))


# Hack to ensure that we import using versionURI
# FIXME: included this in sync_attributes()
d = {o.base_iri.rstrip('/#'): o.get_version(as_iri=True)
     for o in onto.imported_ontologies}
for abbrev_iri in onto.world._get_obj_triples_sp_o(
        onto.storid, owlready2.owl_imports):
    iri = onto._unabbreviate(abbrev_iri)
    version_iri = d[iri]
    onto._del_obj_triple_spo(
        onto.storid,
        owlready2.owl_imports,
        abbrev_iri)
    onto._add_obj_triple_spo(
        onto.storid,
        owlready2.owl_imports,
        onto._abbreviate(version_iri))


onto.save(thisdir / f"{ontology_name}.ttl", format="turtle", overwrite=True)

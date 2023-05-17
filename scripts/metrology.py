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


def latex2text(latex):
    """Convert LaTeX to UTF-8."""

    def fscript(m):
        """Convert superscripts and subscripts from regex match object `m`."""
        op, _, _, exp1, exp2 = m.groups()
        exp = exp1 or exp2
        assert op in "^_"
        table = str.maketrans(
            "0123456789+-",
            "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077"
            "\u2078\u2079\u207a\u207b" if op == "^" else
            "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087"
            "\u2088\u2089\u208a\u208b"
        )
        return exp.translate(table)

    subs = {
        r"\,": " ",
        r'\"': '"',
        r"\'": "'",
        r"\pm": "\u00b1",
        r"\cdot": "\u00b7",
        r"\times": "\u00d7",
        r"\div": "\u00f7",
        r"\neg": "\u00ac",
        r"\ast": "\u2217",
        r"\star": "\u22c6",
        r"\sqrt": "\u221a",
        r"\cuberoot": "\u221b",
        r"\forthroot": "\u221c",
        r"\infty": "\u221e",
        r"\sum": "\u2211",
        r"\prod": "\u220f",
        r"\int": "\u222b",
        r"\vedge": "\u2227",
        r"\vee": "\u2228",
        r"\cap": "\u2229",
        r"\cup": "\u222a",
        r"\prime": "\u2032",
        r"\dprime": "\u2033",
        r"\tprime": "\u2034",
        r"\forall": "\u2200",
        r"\complement": "\u2201",
        r"\exists": "\u2203",
        r"\nexists": "\u2204",
        r"\nothing": "\u2205",
        r"\varnothing": "\u2205",
        r"\top": "\u22a4",
        r"\bot": "\u22a5",
        r"\in": "\u2208",
        r"\notin": "\u2209",
        r"\ni": "\u220b",
        r"\nni": "\u220c",
        r"\subset": "\u2282",
        r"\supset": "\u2283",
        r"\nsubset": "\u2284",
        r"\nsupset": "\u2285",
        r"\diameter": "\u2300",
        r"\propto": "\u221d",
        r"\mid": "\u2223",
        r"\sim": "\u223c",
        r"\approx": "\u2248",
        r"\equiv": "\u2261",
        r"\nequiv": "\u2262",
        r"\leq": "\u2264",
        r"\geq": "\u2265",
        r"\ll": "\u226a",
        r"\gg": "\u226b",
        r"\leftarrow": "\u2190",
        r"\rightarrow": "\u2192",
        r"\leftrightarrow": "\u2194",
        r"\Leftarrow": "\u21d0",
        r"\Rightarrow": "\u21d2",
        r"\leftrightarrow": "\u21d4",
        r"\hslash": "\u210f",
        r"\alpha": "\u03b1",
        r"\beta": "\u03b2",
        r"\gamma": "\u03b3",
        r"\delta": "\u03b4",
        r"\epsilon": "\u03b5",
        r"\zeta": "\u03b6",
        r"\eta": "\u03b7",
        r"\theta": "\u03b8",
        r"\iota": "\u03b9",
        r"\kappa": "\u03ba",
        r"\lambda": "\u03bb",
        r"\mu": "\u03bc",
        r"\nu": "\u03bd",
        r"\xi": "\u03be",
        r"\omicron": "\u03bf",
        r"\pi": "\u03c0",
        r"\rho": "\u03c1",
        r"\sigma": "\u03c3",
        r"\tau": "\u03c4",
        r"\upsilon": "\u03c5",
        r"\phi": "\u03c6",
        r"\chi": "\u03c7",
        r"\psi": "\u03c8",
        r"\omega": "\u03c9",
        r"\Gamma": "\u0393",
        r"\Delta": "\u0394",
        r"\Theta": "\u0398",
        r"\Lambda": "\u039b",
        r"\Xi": "\u039e",
        r"\Pi": "\u03a0",
        r"\Sigma": "\u03a3",
        r"\Upsilon": "\u03a5",
        r"\Phi": "\u03a6",
        r"\Psi": "\u03a8",
        r"\Omega": "\u03a9",
        r"\AA{}": "\u00c5",
        r"\euro": "\u20ac",
    }
    # Strip of inline equations
    sub1 = re.sub(r"\\?\\\((.*?)\\?\\\)", r"\1", latex)
    # Convert subscripts and superscripts
    sub2 = re.sub("([_^])((\{([-+]?[0-9]+)\})|([-+]?[0-9]+))", fscript, sub1)
    # Convert latex symbols
    for k, v in subs.items():
        sub2 = sub2.replace(rf"\{k}", v)
        sub2 = sub2.replace(k, v)
    # Strip off \frac
    sub3 = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", sub2)
    # Strip off remaining latex macros
    sub4 = re.sub(r"\\[a-zA-Z]+\{['`]?([^}]+?)['`]?\}", r"`\1`", sub3)
    return sub4


def htmlstrip(s):
    """Strip off html tags in string `s`."""
    return re.sub("<[^>]+>", "", s).replace("&quot;", '"')


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


# Add description with citations
for qudtunit, unit in units.items():
    qudt_descr = ts.value(qudtunit, QUDT.plainTextDescription)
    dc_descr = ts.value(qudtunit, DCTERMS.description)
    unit = onto[unit.prefLabel.first()]
    if (qudt_descr or dc_descr) and (
            not unit.elucidation or
            unit.elucidation.first() in (qudt_descr, dc_descr)
    ):
        print("***", unit.elucidation.first())
        descr = htmlstrip(latex2text(qudt_descr or dc_descr))
        #sub1 = re.sub(r"\\?\\\((.*?)\\?\\\)", r"\1", qudt_descr or dc_descr)
        #sub2 = re.sub(r"\{([^}]*)\} ", r"\1 ", sub1)
        #descr = sub2.replace(r"\,", "").replace(r"\cdot", "·")
        citation = "\n\n-- QUDT"
        unit.elucidation.clear()
        unit.elucidation.append(en(descr + citation))


# Correct QUDT errors
# -------------------
# Mobility has wrong dimensionality.  We have already added ElectricMobility
# with the correct dimensionality.  Just get rid of MobilityUnit
if 'MobilityUnit' in du:
    owlready2.destroy_entity(du.MobilityUnit, True)


# Save ontologies
# ---------------
du.save(disciplinesdir / "sidimensionalunits.ttl", format="turtle", overwrite=True)
onto.save(disciplinesdir / f"unitsextension_gen.ttl", format="turtle", overwrite=True)


def set_turtle_prefix(filename, prefix, base=None):
    """Set/overwrite @prefix in top of a turtle file.  Optionally, also set @base."""
    with open(filename, "rt") as f:
        lines = f.readlines()

    prefix1 = base1 = None
    for i in range(len(lines)):
        line = lines[i]
        if not line.startswith("@"):
            break
        match = re.match(r"^@prefix\s*:\s*<(.*)>", line)
        if match:
            prefix1 = match.groups()[0]
            lines.pop(i)
        if base is not None:
            match = re.match(r"^@base\s*<(.*)>", line)
            if match:
                base1 = match.groups()[0]
                lines.pop(i)

    with open(filename, "wt") as f:
        if prefix:
            f.write(f"@prefix : <{prefix}> .\n")
        elif prefix is None and prefix1:
            f.write(f"@prefix : <{prefix1}> .\n")
        for i in range(len(lines)):
            line = lines[i]
            if not line.startswith("@"):
                break
            f.write(line)
        if base:
            f.write(f"@base <{base}> .\n")
        elif base is None and base1:
            f.write(f"@base <{base1}> .\n")
        for line in lines[i:]:
            f.write(line)



set_turtle_prefix(disciplinesdir / "sidimensionalunits.ttl", EMMO, EMMO)
set_turtle_prefix(disciplinesdir / "unitsextension_gen.ttl", EMMO, EMMO)


# Simply replace all owl:hasValue from decimal to xsd:double
with open(disciplinesdir / "unitsextension_gen.ttl", "rt") as f:
    lines = [
        re.sub(
            "owl:hasValue +([0-9.]+)(\s|$)",
            r'owl:hasValue "\1"^^xsd:double ',
            line
        ) for line in f
    ]

with open(disciplinesdir / "unitsextension.ttl", "wt") as f:
    for line in lines:
        f.write(line)

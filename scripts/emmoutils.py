"""Module with utility functions.
"""
# pylint: disable=invalid-name
import re

import owlready2


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
    onto = unit.namespace.ontology
    if unit.unitSymbol:
        return unit.unitSymbol.first()
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasUnitSymbol):
            return r.value
    return None


def fix_preflabel(label, onto, prefixes, corrected_preflabels=None):
    """Convert `label` to a valid prefLabel.
    Each component will start with a big case.
    Trailing "s"'s after a prefixed unit are removed.

    Arguments:
        label: Label to convert.
        onto: Ontology to look for unit components in.
        prefixes: Dict mapping prefix names to corresponding symbol.
            Ex: {"Kilo": "k", ...}
        corrected_preflabels: Optional dict for handling special cases.
            It should map `label` to correct preflabel.

    Returns:
        Valid prefLabel.
    """
    if corrected_preflabels and label in corrected_preflabels:
        return corrected_preflabels[label]
    newlabel = []
    for s in re.findall("[A-ZÅ][a-zö0-9_]*", label):
        for prefix in prefixes.keys():
            if s.startswith(prefix):
                newlabel.append(prefix)
                s = s[len(prefix):].title()
                break
        if s in onto:
            newlabel.append(onto[s].prefLabel.first())
        elif s.endswith("s") and s[:-1] in onto:
            newlabel.append(onto[s[:-1]].prefLabel.first())
        else:
            newlabel.append(s)
    return "".join(newlabel)


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
        r'\"': r'\"',
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
        r"\Leftrightarrow": "\u21d4",
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
    sub2 = re.sub(r"([_^])((\{([-+]?[0-9]+)\})|([-+]?[0-9]+))", fscript, sub1)
    # Convert latex symbols
    for k, v in subs.items():
        sub2 = sub2.replace(rf"\{k}", v)
        sub2 = sub2.replace(k, v)
    # Strip off \frac
    sub3 = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", sub2)
    # Strip off remaining latex macros
    sub4 = re.sub(r"\\[a-zA-Z]+\{['`]?([^}]+?)['`]?\}", r"`\1`", sub3)
    return sub4.replace(r"\'", "'").replace(r" \\; ", " ").replace(r"\\(", "").replace(r"^\\circ", "\u00b0")


def htmlstrip(s):
    """Strip off html tags in string `s`."""
    return re.sub("<[^>]+>", "", s).replace("&quot;", '"')


def remove_python_name(onto):
    """Strip off all uses of owlr:python_name from ontology."""
    storid = onto._abbreviate(
        "http://www.lesfleursdunormal.fr/static/_downloads/"
        "owlready_ontology.owl#python_name"
    )
    for s, p, o, d in onto._get_triples_spod_spod(None, 2, None):
        if d is None:
            onto._del_obj_triple_spo(s, p, o)
        else:
            onto._del_data_triple_spod(s, p, o, d)


def set_turtle_prefix(filename, prefix, base=None):
    """Set/overwrite @prefix in top of a turtle file.  Optionally, also set @base."""
    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    prefix1 = base1 = None
    for i in range(len(lines)):  # pylint: disable=consider-using-enumerate
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

    with open(filename, "wt", encoding="utf-8") as f:
        if prefix:
            f.write(f"@prefix : <{prefix}> .\n")
        elif prefix is None and prefix1:
            f.write(f"@prefix : <{prefix1}> .\n")
        for line in lines:
            if not line.startswith("@"):
                break
            f.write(line)
        if base:
            f.write(f"@base <{base}> .\n")
        elif base is None and base1:
            f.write(f"@base <{base1}> .\n")
        for line in lines[i:]:
            f.write(line)


def replace(filename, replacements):
    """For the given filename, replace each occurence of `replacements`
    keys with corresponding values.

    """
    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    with open(filename, "wt", encoding="utf-8") as f:
        for line in lines:
            for k, v in replacements.items():
                line = re.sub(k, v, line)
            f.write(line)


def get_metricprefix_value(prefix):
    """Returns the numerical value of a metric prefix."""
    onto = prefix.namespace.ontology
    for r in prefix.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasNumericalValue):
            return r.value
    raise TypeError(f"not a metric prefix: {prefix}")


def get_siconversion_multiplier(unit):
    """Returns the SI conversion multiplier of the given unit."""
    onto = unit.namespace.ontology
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasSIConversionMultiplier):
            return r.value
    if unit in onto.SIBaseUnit.disjoint_unions[0] + onto.SISpecialUnit.disjoint_unions[0]:
        return 1.0
    raise TypeError(f"missing SI conversion multiplier: {unit}")


def get_siconversion_offset(unit):
    """Returns the SI conversion offset of the given unit."""
    onto = unit.namespace.ontology
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasSIConversionOffset):
            return r.value
    if unit in onto.SIBaseUnit.disjoint_unions[0] + onto.SISpecialUnit.disjoint_unions[0]:
        return 0.0
    raise TypeError(f"missing SI conversion offset: {unit}")


def has_siconversion_multiplier(unit):
    """Returns whether a a SI conversion multiplier is defined for the unit."""
    onto = unit.namespace.ontology
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasSIConversionMultiplier):
            return True
    return False


def has_siconversion_offset(unit):
    """Returns whether a a SI conversion offset is defined for the unit."""
    onto = unit.namespace.ontology
    for r in unit.is_a:
        if (isinstance(r, owlready2.Restriction) and
            r.property == onto.hasSIConversionOffset):
            return True
    return False


def add_is_a(cls, r):
    """Add restriction `r` to class `cls` (if it doesn't already exists)."""
    if r not in cls.is_a:
        cls.is_a.append(r)


def has_is_a(cls, r):
    """Returns whether given restriction or property is in the is_a list.."""
    if isinstance(r, owlready2.Restriction):
        return r in cls.is_a

    for t in cls.is_a:
        if isinstance(t, owlready2.Restriction):
            if t.property == r:
                return True

    return False


def del_is_a(cls, r):
    """Remove restriction `r` from class `cls` (if it exists)."""
    if r in cls.is_a:
        print("# remove:", r)
        cls.is_a.remove(r)

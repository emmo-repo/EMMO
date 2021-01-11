#!/usr/bin/env python
"""Python script that generates the periodic table ontology.
"""
import os
import subprocess
import warnings
import types

import ase

import rdflib
from rdflib import URIRef, Literal
from rdflib.namespace import RDFS, OWL, DCTERMS

from emmo import World, get_ontology


thisdir = os.path.abspath(os.path.dirname(__file__))


# Check rdflib version (for preferred turtle serialising)
if not int(rdflib.__version__.split('.')[0]) >= 5:
    warnings.warn('upgrade to rdflib v5.0.0 or higher to get preferred output')

# Connect to db and load emmo
#world = World(filename='periodic-table.sqlite3')
world = World()
emmo = world.get_ontology(os.path.join(thisdir, '../middle/middle.ttl'))
emmo.load()
emmo.sync_python_names()

# Create new ontology
onto = world.get_ontology('http://emmo.info/emmo/domain/periodic-table#')
onto.base_iri = 'http://emmo.info/emmo#'
onto.imported_ontologies.append(emmo)
onto.sync_python_names()


# Populate the new ontology
with onto:

    class EMMOConventionalQuantityAssignment(
            onto.ConventionalQuantitativePropertyAssignment):
        """The class of conventional assignments performed by the EMMO
        Comittee."""

    class EMMOAtomicNumber(onto.AtomicNumber):
        """Atomic number declared by the EMMO committee as a conventional
        quantitative property."""

    class EMMOAtomicMass(onto.AtomicMass):
        """Atomic mass declared by the EMMO committee as a conventional
        quantitative property.

        Values taken from IUPAC2016.
        """

    # FIXME - update when the chemistry module is included in EMMO
    class hasChemicalSymbol(onto.hasSymbolData):
        """Conventional chemical symbol of an atomic element."""
        range = [str]


    EMMOCommittee = onto.Interpreter('EMMOCommittee')

    unitOne = onto.UnitOne('unitOne')
    dalton = onto.Dalton('dalton')

    for Z, (s, name, m) in enumerate(zip(
            ase.data.chemical_symbols,
            ase.data.atomic_names,
            ase.data.atomic_masses_iupac2016)):
        if not name:
            continue  # skip Z=0
        lname = name.lower()

        AtomClass = types.new_class(name + 'Atom', (onto.Atom, ))
        AtomClass.elucidation.append('Atom subclass for %s.' % lname)
        AtomClass.is_a.append(hasChemicalSymbol.value(s))

        z = onto.Integer(lname + 'AtomicNumberValue',
                         hasNumericalData=int(Z))
        number = EMMOAtomicNumber(lname + 'AtomicNumber',
                                  hasReferenceUnit=[unitOne],
                                  hasQuantityValue=[z])

        mval = onto.Real(lname + 'AtomicMassValue',
                         hasNumericalData=float(m))
        mass = EMMOAtomicMass(lname + 'AtomicMass')
        mass.hasReferenceUnit = [dalton]
        mass.hasQuantityValue = [mval]

        # TODO: add covalent_radii, ground_state_magnetic_moments,
        #           reference_states, vdw_radii,

        at = AtomClass(lname,
                       hasConventionalQuantity=[number, mass],
        )

        assignment = EMMOConventionalQuantityAssignment(
            lname + 'AtomicAtomicNumberAssignment')
        assignment.hasParticipant = [EMMOCommittee, at, number]
        print(Z, s, lname, m)

# Save new ontology as owl
onto.sync_attributes(name_policy='uuid', name_prefix='EMMO_')
onto.set_version(
    version_iri="http://emmo.info/emmo/1.0.0-beta/domain/periodic-table")
onto.dir_label = False
onto.save(os.path.join(thisdir, 'periodic-table.owl'), overwrite=True)


# Do final manipulation with rdflib
BASE = rdflib.Namespace('http://emmo.info/emmo/domain/periodic-table')

g = rdflib.Graph()
g.bind('skos', rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#'))
g.bind('', rdflib.term.URIRef('http://emmo.info/emmo#'))
g.parse('periodic-table.owl', format='xml')

# Add version to imported ontologies
version = '1.0.0-beta'
for s, p, o in g.triples((None, OWL.imports, None)):
    o2 = URIRef(o.replace('http://emmo.info/emmo/',
                          'http://emmo.info/emmo/%s/' % version))
    g.remove((s, p, o))
    g.add((s, p, o2))

# Add ontology annotations
g.add((URIRef(BASE), OWL.versionInfo, Literal(version)))
g.add((URIRef(BASE), DCTERMS.title, Literal('Periodic table', lang='en')))
g.add((URIRef(BASE), DCTERMS.creator, Literal('Jesper Friis')))
g.add((URIRef(BASE), DCTERMS.contributor, Literal('SINTEF')))
g.add((URIRef(BASE), DCTERMS.creator, Literal('Emanuele Ghedini')))
g.add((URIRef(BASE), DCTERMS.contributor, Literal('University of Bologne')))
g.add((URIRef(BASE), DCTERMS.publisher, Literal('EMMC ASBL')))
g.add((URIRef(BASE), DCTERMS.license,
       Literal('https://creativecommons.org/licenses/by/4.0/legalcode')))

g.add((URIRef(BASE), DCTERMS.abstract,
       Literal('''\
The periodic table domain ontology provide a simple reference \
implementation of all atoms in the periodic table with a few \
selected conventional properties.  It is ment as both an example \
for other domain ontologies as well as a useful assert by itself.

Periodic table is released under the Creative Commons Attribution 4.0 \
International license (CC BY 4.0).
''', lang='en')))

g.add((URIRef(BASE), RDFS.comment,
       Literal('''\
The EMMO requires FacT++ reasoner plugin in order to visualize all \
inferences and class hierarchy (ctrl+R hotkey in Protege).
''', lang='en')))

g.add((URIRef(BASE), RDFS.comment,
       Literal('''\
This ontology is generated with data from the ASE Python package.
''', lang='en')))

g.add((URIRef(BASE), RDFS.comment,
       Literal('''\
Contacts:
Gerhard Goldbeck
Goldbeck Consulting Ltd (UK)
email: gerhard@goldbeck-consulting.com

Emanuele Ghedini
University of Bologna (IT)
email: emanuele.ghedini@unibo.it
''', lang='en')))

# Store in turtle format
g.serialize(destination='periodic-table.ttl', format='turtle', base=BASE)

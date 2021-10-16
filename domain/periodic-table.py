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
import owlready2


__version__ = '1.0.0-beta'

thisdir = os.path.abspath(os.path.dirname(__file__))


def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


# Check rdflib version (for preferred turtle serialising)
if not int(rdflib.__version__.split('.')[0]) >= 5:
    warnings.warn('upgrade to rdflib v5.0.0 or higher to get preferred output')

# Connect to db and load emmo
#world = World(filename='periodic-table.sqlite3')
world = World()
emmo = world.get_ontology(os.path.join(thisdir, '../middle/middle.ttl')).load()
isq = world.get_ontology(os.path.join(thisdir, 'isq.ttl')).load()
units_extension = world.get_ontology(os.path.join(thisdir, 'units-extension.ttl')).load()
emmo.sync_python_names()

# Create new ontology
onto = world.get_ontology('http://emmo.info/emmo/domain/periodic-table#')
onto.base_iri = 'http://emmo.info/emmo#'
onto.imported_ontologies.append(emmo)
onto.imported_ontologies.append(isq)
onto.imported_ontologies.append(units_extension)
onto.sync_python_names()


# Populate the new ontology
with onto:

    class hasChemicalSymbol(onto.hasSymbolData):
        """Conventional chemical symbol of an atomic element."""
        domain = [emmo.Atom]
        range = [str]

    class hasAtomicNumber(owlready2.DataProperty):
        """The atomic number of an atomic element."""
        domain = [emmo.Atom]
        range = [int]
        comment = [
            'This is a convenient shortcut for the conventional declaration '
            'process of assigning an atomic number to an atom subclass.'
        ]

    class hasAtomicMassIUPAC2016(owlready2.DataProperty):
        """The mass of an atomic element according to IUPAC 2016."""
        domain = [emmo.Atom]
        range = [float]

    for Z, (symbol, name, mass) in enumerate(zip(
            ase.data.chemical_symbols,
            ase.data.atomic_names,
            ase.data.atomic_masses_iupac2016)):
        if not name:
            continue  # skip Z=0

        print(Z, symbol, name, mass)

        AtomClass = types.new_class(name.capitalize() + 'Atom', (onto.Atom, ))
        AtomClass.elucidation.append(en('Atom subclass for %s.' % name.lower()))
        AtomClass.is_a.append(hasChemicalSymbol.value(symbol))
        AtomClass.is_a.append(hasAtomicNumber.value(Z))
        AtomClass.is_a.append(hasAtomicMassIUPAC2016.value(float(mass)))


# Set ontology metadata
version_iri = f'http://emmo.info/emmo/{__version__}/domain/periodic-table'
onto.set_version(version_iri=version_iri)

onto.metadata.abstract.append(en(
    'The periodic table domain ontology provide a simple reference '
    'implementation of all atoms in the periodic table with a few '
    'selected conventional properties.  It is ment as both an example '
    'for other domain ontologies as well as a useful assert by itself. '
    'Periodic table is released under the Creative Commons Attribution 4.0 '
    'International license (CC BY 4.0).'))

onto.metadata.title.append(en('Periodic table'))
onto.metadata.creator.append(en('Jesper Friis'))
onto.metadata.creator.append(en('Francesca Lønstad Bleken'))
onto.metadata.contributor.append(en('SINTEF'))
onto.metadata.creator.append(en('Emanuele Ghedini'))
onto.metadata.contributor.append(en('University of Bologna'))
onto.metadata.publisher.append(en('EMMC ASBL'))
onto.metadata.license.append(en(
    'https://creativecommons.org/licenses/by/4.0/legalcode'))
version = '1.0.0-beta'
onto.metadata.versionInfo.append(en(version))
onto.metadata.comment.append(en(
    'The EMMO requires FacT++ reasoner plugin in order to visualize all '
    'inferences and class hierarchy (ctrl+R hotkey in Protege).'))
onto.metadata.comment.append(en(
    'This ontology is generated with EMMOntoPy using data from the ASE '
    'Python package.'))
onto.metadata.comment.append(en(
    'You can contact EMMO Authors via emmo@emmc.eu'))

# Save new ontology as turtle
onto.sync_attributes(name_policy='uuid', name_prefix='EMMO_',
                     class_docstring='elucidation')
onto.dir_label = False
onto.save(os.path.join(thisdir, 'periodic-table.ttl'), format='turtle', overwrite=True)
0/0


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
g.add((URIRef(BASE), DCTERMS.creator, Literal('Francesca Bleken Lønstad')))
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

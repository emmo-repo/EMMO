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

from ontopy import World, get_ontology
import owlready2


thisdir = os.path.abspath(os.path.dirname(__file__))


def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


# Check rdflib version (for preferred turtle serialising)
if not int(rdflib.__version__.split('.')[0]) >= 5:
    warnings.warn('upgrade to rdflib v5.0.0 or higher to get preferred output')

# Connect to db and load emmo
#world = World(filename='periodictable.sqlite3')
world = World()
chemistry = world.get_ontology(os.path.join(thisdir, 'chemistry.ttl')).load()
#emmo_middle.sync_python_names()

# Create new ontology
onto = world.get_ontology('https://w3id.org/emmo/disciplines/periodictable#')
onto.iri = 'https://w3id.org/emmo/disciplines/periodictable'
onto.base_iri = 'https://w3id.org/emmo#'
onto.prefix = 'emmo'
onto.imported_ontologies.append(chemistry)
onto.sync_python_names()


# Populate the new ontology
with onto:

    class hasAtomicNumber(owlready2.DataProperty):
        """The atomic number of an atomic element."""
        domain = [onto.Atom]
        range = [int]
        comment = [
            'This is a convenient shortcut for the conventional declaration '
            'process of assigning an atomic number to an atom subclass.'
        ]

    class hasIUPAC2016AtomicMass(owlready2.DataProperty):
        """The mass of an atomic element according to IUPAC 2016."""
        domain = [onto.Atom]
        range = [float]
        comment = [
            'This is a convenient shortcut for the measurement process '
            'process of the atomic mass reported by IUPAC2016.'
        ]

    class hasChemicalSymbol(onto.hasProperty):
        """The chemical symbol of an atomic element."""
        domain = [onto.Atom]
        range = [onto.ChemicalElement]

    #onto.Atom.hasChemicalSymbol.exactly(1, onto.ChemicalElement)

    for Z, (symbol, name, mass) in enumerate(zip(
            ase.data.chemical_symbols,
            ase.data.atomic_names,
            ase.data.atomic_masses_iupac2016)):
        if not name:
            continue  # skip Z=0

        print(Z, symbol, name, mass)

        Element = types.new_class(
            name.capitalize() + 'Symbol', (onto.ChemicalElement, )
        )
        Element.is_a.append(onto.hasSymbolValue.value(symbol))

        AtomClass = types.new_class(name.capitalize() + 'Atom', (onto.Atom, ))
        AtomClass.elucidation.append(en('Atom subclass for %s.' % name.lower()))
        AtomClass.is_a.append(hasAtomicNumber.value(Z))
        AtomClass.is_a.append(hasIUPAC2016AtomicMass.value(float(mass)))
        AtomClass.is_a.append(hasChemicalSymbol.some(Element))


# Set ontology metadata
version = chemistry.get_version()
version_iri = f'https://w3id.org/emmo/{version}/disciplines/periodictable'
onto.set_version(version_iri=version_iri)

onto.metadata.abstract.append(en(
    'The periodic table domain ontology provide a simple reference '
    'implementation of all atoms in the periodic table with a few '
    'selected conventional properties.  It is ment as both an example '
    'for other domain ontologies as well as a useful assert by itself. '
    'Periodic table is released under the Creative Commons Attribution 4.0 '
    'International license (CC BY 4.0).'))

onto.metadata.title.append(en('Periodic table'))
onto.metadata.creator.append(en('Jesper Friis, SINTEF, NO'))
onto.metadata.creator.append(en('Francesca Lønstad Bleken, SINTEF, NO'))
onto.metadata.creator.append(en('Emanuele Ghedini, University of Bologna, IT'))
onto.metadata.publisher.append(en('EMMC ASBL'))
onto.metadata.license.append(en(
    'https://creativecommons.org/licenses/by/4.0/legalcode'))
onto.metadata.versionInfo.append(en(version))
onto.metadata.comment.append(en(
    'The EMMO requires HermiT reasoner plugin in order to visualize all '
    'inferences and class hierarchy (ctrl+R hotkey in Protege).'))
onto.metadata.comment.append(en(
    'This ontology is generated with EMMOntoPy using data from the ASE '
    'Python package.'))
onto.metadata.comment.append(en(
    'You can contact EMMO Authors via emmo@emmc.eu'))

# Synchronise Python attributes to ontology
onto.sync_attributes(name_policy='uuid', name_prefix='EMMO_',
                     class_docstring='elucidation')
onto.dir_label = False

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

# Save new ontology as turtle
onto.save(
    os.path.join(thisdir, 'periodictable.ttl'), format='turtle', overwrite=True
)

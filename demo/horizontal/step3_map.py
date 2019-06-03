#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3 - map to common representation
-------------------------------------
maps it to a collection of instances of the metadata generated from the
ontology.


This script uses the Atomistic Simulation Environment (ASE) to load
a atomistic Al-Fe4Al13 interface structure from a cif file and
represents it using the same metadata framework as used in step 1.
"""
import ase
import ase.io
from ase.spacegroup import Spacegroup
from ase.visualize import view

import dlite


def map_app2common(inst, metacoll, out_id=None):
    """Maps atom structure `atoms` from our application representation
    (based on a not explicitly stated ontology) to the common
    EMMO-based representation in `metacoll`.

    Parameters
    ----------
    inst : Instance of http://sintef.no/meta/soft/0.1/Atoms
        Input atom structure.
    metacoll : Collection
        Collection of EMMO-based metadata generated from the ontology.
    out_id : None | string
        An optional id associated with the returned collection.

    Returns
    -------
    atcoll : Collection
        New collection with the atom structure represented as instances
        of metadata in `metacoll`.
    """
    infodict = dict(inst.info)  # make dict out of the info field

    # Create new collection representing `inst` in our case ontology
    atcoll = dlite.Collection(out_id)

    # Get metadata from metacoll
    Crystal = metacoll['crystal']
    UnitCell = metacoll['crystal_unit_cell']
    EBondedAtom = metacoll['e-bonded_atom']

    # Instanciate the structure
    crystal = Crystal([])
    crystal.spacegroup = infodict['spacegroup']
    atcoll.add('crystal', crystal)

    unit_cell = UnitCell([3, 3, 36])
    unit_cell.lattice_vector = inst.cell
    atcoll.add('unit_cell', unit_cell)
    atcoll.add_relation('crystal', 'has_spatial_direct_part', 'unit_cell')

    for i in range(inst.natoms):
        label = 'atom%d' % i
        a = EBondedAtom([3])
        a.atomic_number = inst.numbers[i]
        a.atomic_mass = inst.masses[i]
        a.position = inst.positions[i]
        atcoll.add(label, a)
        atcoll.add_relation('unit_cell', 'has_spatial_direct_part', label)

    return atcoll


# Load metadata collection from step 1
metacoll = dlite.Collection('json://case_metadata.json?mode=r#case_ontology', True)

# Load dlite-representation of atoms structure from step 2
coll = dlite.Collection('json://case_data.json?mode=r#case_data', False)
inst = coll.get('atoms')


# Do the mapping
new = map_app2common(inst, metacoll)


# Append the new atoms collection to the storage
new.save('json://case_data.json?mode=append')
new.save('json', 'case_data.json', 'mode=append')

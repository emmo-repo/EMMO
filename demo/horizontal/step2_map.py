#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This script uses the Atomistic Simulation Environment (ASE) to load
a atomistic Al-Fe4Al13 interface structure from a cif file and
maps it to a collection of instances of the metadata generated from the
ontology.
"""
import ase
import ase.io
from ase.visualize import view

import dlite


# Create an ASE Atoms subclass that also inherits from dlite atoms.json
BaseAtoms = dlite.classfactory(ase.Atoms, url='json://atoms.json?mode=r#')
class DLiteAtoms(BaseAtoms):
    """ASE Atoms class extended as a dlite entity."""
    def _dlite_get_info(self):
        return [(k, repr(v)) for k, v in self.info.items()]

    def _dlite_set_info(value):
        self.info.update(value)

    def _dlite_get_celldisp(self):
        return self.get_celldisp()[:, 0]


def map_ase2onto(atoms, metacoll):
    """Maps ASE atoms instance to a collection of instances of metadata
    generated from the ontology.

    Parameters
    ----------
    atoms : Instance
        Input DLiteAtoms instance corresponding to an ASE Atoms objects.
    metacoll : Collection
        Collection with metadata generated from the ontology.

    Returns
    -------
    atcoll : Collection
        A new collection with instances of the metadata in `metacoll`.
    """

    # Create new collection representing `atoms` in our case ontology
    atcoll = dlite.Collection('coll_Al-Fe4Al13')

    Crystal = metacoll['crystal']
    crystal = Crystal([], 'Al-Fe4Al13')
    crystal.spacegroup = 'P1'  # symmetry is broken by the interface
    atcoll.add('crystal', crystal)

    UnitCell = metacoll['crystal_unit_cell']
    unit_cell = UnitCell([3, 3])
    unit_cell.lattice_vector = at.cell
    atcoll.add('unit_cell', unit_cell)
    atcoll.add_relation('crystal', 'has_spatial_direct_part', 'unit_cell')

    EBondedAtom = metacoll['e-bonded_atom']
    for i, atom in enumerate(atoms):
        a = EBondedAtom([3])
        a.atomic_number = atom.number
        a.atomic_mass = atom.mass
        a.position = atom.position
        label = 'atom%d' % i
        atcoll.add(label, a)
        atcoll.add_relation('unit_cell', 'has_spatial_direct_part', label)

    return atcoll



# Load atom structure from cif file and convert it to a DLiteAtoms object
at = ase.io.read('../vertical/Al-Fe4Al13.cif')
atoms = dlite.objectfactory(at, cls=DLiteAtoms, instanceid='atoms_Al-Fe4Al13')
atoms.dlite_inst.save('json', 'atoms_Al-Fe4Al13.json', 'mode=w')


# Load metadata collection from step 1
metacoll = dlite.Collection('json://horizontal.json?mode=r#crystal', True)

# Do the mapping
atcoll = map_ase2onto(atoms, metacoll)

# Append the new atoms collection to the storage
atcoll.save('json', 'horizontal.json', 'mode=append')

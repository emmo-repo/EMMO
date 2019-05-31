#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2 - load atom structure and represent it using our metadata framework
--------------------------------------------------------------------------
In this step we uses the Atomistic Simulation Environment (ASE) to load
a atomistic Al-Fe4Al13 interface structure from a cif file and
represents it using the same metadata framework as used in step 1.
"""
import ase
import ase.io
from ase.spacegroup import Spacegroup

import dlite


# Create an ASE Atoms subclass that also inherits from dlite atoms.json
BaseAtoms = dlite.classfactory(ase.Atoms, url='json://atoms.json?mode=r#')
class DLiteAtoms(BaseAtoms):
    """ASE Atoms class extended as a dlite entity."""
    def _dlite_get_info(self):
        d = self.info.copy()
        sg = Spacegroup(d.get('spacegroup', 'P 1'))
        d['spacegroup'] = sg.symbol
        return [(k, str(v)) for k, v in d.items()]

    def _dlite_set_info(value):
        self.info.update(value)
        self.info['spacegroup'] = Spacegroup(self.info['spacegroup'])

    def _dlite_get_celldisp(self):
        return self.get_celldisp()[:, 0]


# Load atom structure from cif file and convert it to a DLiteAtoms object
at = ase.io.read('../vertical/Al-Fe4Al13.cif')
atoms = dlite.objectfactory(at, cls=DLiteAtoms, instanceid='atoms_Al-Fe4Al13')


# Create a new collection for data instances
coll = dlite.Collection('case_data')
coll.add('Atoms', atoms.dlite_meta)
coll.add('atoms', atoms.dlite_inst)
coll.save('json', 'case_data.json', 'mode=w')

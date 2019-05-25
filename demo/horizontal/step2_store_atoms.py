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


# Load atom structure from cif file and convert it to a DLiteAtoms object
at = ase.io.read('../vertical/Al-Fe4Al13.cif')
atoms = dlite.objectfactory(at, cls=DLiteAtoms, instanceid='atoms_Al-Fe4Al13')

# Load collection ASE_Atoms from case ontology
coll = dlite.Collection('json://horizontal.json?mode=r#ASE_Atoms', True)
ase_atom = coll['ASE_Atom']
ase_atoms = coll['ASE_Atoms']

# Create a collection representing `atoms` in our case ontology
acoll = dlite.Collection('coll_Al-Fe4Al13')

acoll.save('json', 'horizontal.json', 'mode=append')



# Append the atoms object to the storage
atoms.dlite_inst.save('json', 'horizontal.json', 'mode=append')

import dlite

coll = dlite.Collection('json://horizontal.json?mode=r#ASE_Atoms', True)

Atoms = dlite.Instance('json://atoms.json?mode=r')
atoms = dlite.Instance('json', 'horizontal.json', 'mode=r', 'atoms_Al-Fe4Al13')

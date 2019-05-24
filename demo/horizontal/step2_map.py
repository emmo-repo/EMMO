import dlite

Atoms = dlite.Instance('json://atoms.json?mode=r#')

coll = dlite.Collection('json://horizontal.json?mode=r#ASE_Atoms', True)

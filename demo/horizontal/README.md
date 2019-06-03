EMMO use case for horizontal interoperability
=============================================
Horizontal interoperability is about interoperability between
different types of models and codes for a single material (i.e. one
use case, multiple models).


The key here is to show how to map between EMMO (or an EMMO-based
ontology) and another ontology (possible EMMO-based).  In this example
we use a data-driven approach based on SOFT.


This is done in three steps:

  1. Generate metadata from the common EMMO-based ontology.

     Implemented in the script [step1_generate.py](step1_generate.py).

  2. Define application metadata and instansiate an atom structure
     in terms of this metadata.

     Implemented in the script [step2_load_atoms.py](step2_load_atoms.py).

  3. Map the atom structure from the application representation to the
     common EMMO-based representation.

     Implemented in the script [step3_map.py](step3_map.py).




Requirements for running the user case
--------------------------------------
In addition to emmo, this demo also requires:
  - [dlite][1], a C-implementation of [SOFT][2] used for handling metadata
  - [ASE][2], for reading atom structure from cif and visualisation



[1] https://stash.code.sintef.no/projects/SIDASE/repos/dlite/
[2] https://github.com/NanoSim/SOFT5
[3] https://wiki.fysik.dtu.dk/ase/

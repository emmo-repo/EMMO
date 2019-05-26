EMMO use case for horizontal interoperability
=============================================
Horizontal interoperability is about interoperability between
different types of models and codes for a single material (i.e. one
use case, multiple models).


The key here is to show how to map between EMMO (or an EMMO-based
ontology) and another ontology (possible EMMO-based).  In this example
we use a data-driven approach based on SOFT.


Requirements
------------
In addition to emmo, this demo also requires:
  - [dlite][1], a C-implementation of [SOFT][2] used for handling metadata
  - [ASE][2], for reading atom structure from cif and visualisation



[1] https://stash.code.sintef.no/projects/SIDASE/repos/dlite/
[2] https://github.com/NanoSim/SOFT5
[3] https://wiki.fysik.dtu.dk/ase/

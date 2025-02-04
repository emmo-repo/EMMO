Using Protégé
-------------
In order to be able to view and navigate the EMMO ontology we recommend to download the Protégé editor from [https://protege.stanford.edu/products.php#desktop-protege](https://protege.stanford.edu/products.php#desktop-protege).

See [these instructions](doc/protege-setup.md) for how to set up Protégé for working with EMMO-based ontologies.

The fastest way to access the EMMO is to open the ontology via Protégé via the menu under *File -> Open from URL...* and copy the URL [https://w3id.org/emmo](https://w3id.org/emmo):
Protégé will automatically download all the necessary dependencies.

The EMMO hierarchy will be visible only after reasoning inference: use *ctrl-R* to start the reasoner and under the *Entities* tab, select the *Classes* subtab and *Inferred* in the scroll button.

From EMMO 1.0.0 it is recommended to use HermiT as reasoner (distributed by default with Protege).
For earlier EMMO versions is FaCT++ the recommended reasoner.
You can select it through the menu *Reasoner*.
An instruction for how to install the FaCT++ plugin on Protege 5.5.0 on Windows can be found in the [doc subdirectory](doc/installing_factplusplus.md).

To access EMMO from Python, we recommend [EMMOntoPy](https://github.com/emmo-repo/EMMOntoPy) (former EMMO-python).

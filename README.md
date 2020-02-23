# The European Materials Modelling Ontology (EMMO)

## About
EMMO is a multidisciplinary effort to develop a standard representational framework (the ontology) for applied sciences.  It is based on physics, analytical philosophy and information and communication technologies. It has been instigated by materials science and provides the connection between the physical world, the experimental world (materials characterisation) and the simulation world (materials modelling).  It is released under a [Creative Commons license](LICENSE.md).

The full documentation of EMMO, is available in
[html](https://emmo-repo.github.io/latest/doc/emmo.html) and
[pdf](https://emmo-repo.github.io/latest/doc/emmo.pdf) formats.


## EMMO in a Nutshell
The EMMO ontology is structured in shells, expressed by specific ontology fragments, that extends from fundamental concepts to the application domains, following the dependency flow.


### Base
The [emmo-base](emmo-base.owl) is the group of fundamental axioms that constitute the philosophical foundation of the EMMO.  Adopting a physicalistic/nominalistic perspective, the EMMO defines real world objects as 4D objects that are always extended in space and time (i.e. real world objects cannot be spaceless nor timeless).  For this reason abstract objects, i.e. objects that does not extend in space and time, are forbidden in the EMMO.

EMMO is strongly based on the analytical philosophy dicipline semiotic.
The role of abstract objects are in EMMO fulfilled by semiotic objects, i.e. real world objects (e.g. symbol or sign) that stand for other real world objects that are to be interpreted by an agent. These symbols appear in actions (semiotic processes) meant to communicate meaning by establishing relationships between symbols (signs).

Another important building block of from analytical philosophy is atomistic mereology applied to 4D objects.  The EMMO calls it 'quantum mereology', since the there is a epistemological limit to how fine we can resolve space and time due to the uncertanity principles.

The [emmo-mereotopology](base/emmo-mereotopology.owl) introduces the fundamental mereotopological concepts and their relations with the real world objects that they represent.  The EMMO uses mereotopology as the ground for all the subsequent ontology modules.  The concept of topological connection is used to define the first distinction between ontology entities namely the *Item* and *Collection* classes.  Items are causally self-connected objects, while collections are causally disconnected.  Quantum mereology is represented by the *Quantum* class.

The subsequent module, [emmo-4d](base/emmo-4d.owl), introduces the fundamental mereotopological relations used to distinguish between space and time dimensions.

The [emmo-physicals](base/emmo-physicals.owl) module, defines the *Physical* objects and the concept of *void* that plays a fundamental role in the description of multiscale objects and quantum systems. It also define the *Elementary* class, that restricts mereological atomism in space, referring to the concept of elementary particles coming from the [Standard Model](https://en.wikipedia.org/wiki/Standard_Model) of particle physics.

![Figure 1. The most fundamental top-level classes of EMMO.](doc/emmo-base.png)


### Perspectives
In EMMO, the only univocally defined real world object is the *Item* individual called **universe** that stands for the universe. Every other real world object is a composition of elementaries up to the most comprehensive object; the **universe**. Intermediate objects are not univocally defined, but their definition is provided according to some specific philosophical perspectives.  This is an expression of reductionism (i.e. objects are made of sub-objects) and epistemological pluralism (i.e. objects are always defined according to the perspective of an interpreter, or a class of interpreters).

The modules collected in [emmo-perspectives](emmo-perspectives.owl) are different ways to represent the objects that populate the conceptual region between the elementary and universe levels.  *emmo-perspectives* provides different ways to represent the same intermediate objects.

The [emmo-existent](perspectives/emmo-existent.owl) introduces the fundamental non-transitive parthood relation, called *direct parthood*, that provides a powerful granularity description of multiscale real world objects. The EMMO can in principle represents the **universe** with direct parthood relations as a direct rooted tree up to its elementary constituents.

The [emmo-processsual](perspectives/emmo-processual.owl) introduces the concept of real world objects that unfold in time in a way that has a meaning for the EMMO user, through the definition of the classes *process* and *participant*.

The [emmo-semiotics](perspectives/emmo-semiotics.owl) introduces the concepts of semiotics and the *Semiosis* process that has a *Sign*, an *Object* and an *Interpreter* as participants.  This forms the basis in EMMO to represent e.g. models, formal languages, theories, information and properties.

The [emmo-impression](perspectives/emmo-impression.owl) introduces the concept of real world objects that have a meaning for the EMMO user, by means of a recognisable pattern in space or time that impress the user. Under this class the EMMO categorises e.g. formal languages, pictures, geometry, mathematics and sounds. Impressions can be used in a semiotic process as signs.

![Figure 2. The basic taxonomy of EMMO perspectives.](doc/emmo-perspectives.png)


### Domains
The domains ontologies act as roots for extending the EMMO for specific application domains. Up to now the EMMO includes the domains
[graphical](domains/emmo-graphical.owl),
[geometry](domains/emmo-geometry.owl),
[materials](domains/emmo-material.owl),
[math](domains/emmo-math.owl),
[models](domains/emmo-models.owl),
[properties](domains/emmo-properties.owl),
[physical properties](domains/emmo-physical-properties.owl) and
[usercase](domains/emmo-usercase.owl).



### EMMO relations
All EMMO relations are subrelations of the relations found in the two roots: *mereotopological* and *semiological*. The relation hierarchy extends more vertically (i.e. more subrelations) than horizontally (i.e. less sibling relations), facilitating the categorisation and inferencing of individuals.

![Figure 3. The full hierarchy of EMMO relations.](doc/EMMORelation.png)


## Repository Description
You can find the EMMO ontology at [http://emmo.info/emmo.owl](http://emmo.info/emmo.owl).  The basic structure of the EMMO is declared in the [base](base) subfolder, and collected by the [emmo-base](emmo-base.owl) ontology.

The main perspectives used by the EMMO for real world objects representation are declared in the [perspectives](perspectives) subfolder, and collected by the [emmo-perspectives](emmo-perspectives.owl) ontology.

The root classes of the domains that are actually addressed by the EMMO (and in development by several H2020 projects initiatives) are declared in the [domains](domains) subfolder, and collected by the [emmo](emmo.owl) ontology.

The OWL2-DL sources are available in RDF/XML format.


## How To Use It
In order to be able to view and navigate the EMMO ontology we recommend to download the Protégé editor from [https://protege.stanford.edu/products.php#desktop-protege](https://protege.stanford.edu/products.php#desktop-protege).

The fastest way to access the EMMO is to open the ontology via Protégé via the menu under *File -> Open from URL...* and copy the URL [http://emmo.info/emmo.owl](http://emmo.info/emmo.owl): Protégé will automatically download all the necessary dependencies.

The EMMO hierarchy will be visible only after reasoning inference: use *ctrl-R* to start the reasoner and under the *Entities* tab, select the *Classes* subtab and *Inferred* in the scroll button.

It is recommended to use FaCT++ as reasoner. You can select it through the menu *Reasoner*.  An instruction for how to install the FaCT++ plugin on Protege 5.5.0 on Windows can be found in the [doc subdirectory](doc/installing_factplusplus.md).


---

## Contacts:
Emanuele Ghedini
University of Bologna (IT)
email: emanuele.ghedini@unibo.it

Gerhard Goldbeck
Goldbeck Consulting Ltd (UK)
email: gerhard@goldbeck-consulting.com

### Acknowledgement
This work is conducted under the framework of the [SimDOME](https://simdome.eu) project (2019-2023), that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 814492

This work was conducted under the framework of the [EMMC-CSA](https://emmc.info) project (2016-2019), that has received funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 723867

This work was conducted using the Protégé resource, which is supported by grant GM10331601 from the National Institute of General Medical Sciences of the United States National Institutes of Health.

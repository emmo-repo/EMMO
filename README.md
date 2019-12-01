# The European Materials Modelling Ontology (EMMO)

## About
EMMO is a multidisciplinary effort to develop a standard representational framework (the ontology) based on current materials modelling knowledge, including physical sciences, analytical philosophy and information and communication technologies. It provides the connection between the physical world, materials characterisation world and materials modelling world.

EMMO is released under a [Creative Commons license](LICENSE.md).

## EMMO in a Nutshell

The EMMO ontology is structured in shells, expressed by specific ontology fragments, that extends from fundamental concepts to the application domains, following the dependency flow.

### emmo-base
The [emmo-base](emmo-base.owl) is the fundamental group of axioms that constitutes the philosophical foundation of the EMMO. Following a physicalistic/nominalistic perspective the EMMO defines real world objects as 4D objects that always extends in space and time (i.e. real world objects cannot be spaceless or timeless).

For this reason abstract objects, i.e. objects that does not extend in space and time, are forbidden in the EMMO. The role of abstract objects is fulfilled by semiotics objects, i.e. real world objects (e.g. symbols) that stand for other real world objects within a semiotic process.

The EMMO is also based on atomistic mereology applied to 4D. The EMMO calls it 'quantum mereology', since the atomic mereological object in the EMMO is a portion of spacetime at Planck level in time and space.

The [emmo-mereotopology](emmo-mereotopology.owl) introduces the fundamental mereotopological concepts and their relations with the real world objects that they represent that lay the ground for all the subsequent ontology modules. The concept of topological connection is used to define the first distinction between ontology entities according to definition of self connectedness, by introducing the *item* and *collection* classes. Quantum mereology is represented by the *quantum* class. Connectivity is related to the concept of phisical causality.

The [emmo-4d](emmo-4d.owl) introduces the fundamental mereotopological relations used to distinguish between space and time dimensions.

The [emmo-physicals](emmo-physicals.owl) introduces the fundamental definitions in order to define the *physical* objects and the concept of *void* that plays a fundamental role in the description of multiscale objects and quantum systems. It also define the *elemetary* object that restricts mereological atomism in space, and refers to the concept of elementary particles coming from the Standard Model of Particles.
 
### emmo-perspectives
For the EMMO, the only univocally defined real world objects are the *item* individual call **universe** that stands for the Universe and the *quantum* individuals. Every other real world object is a composition in time and space of *quantum* objects up to the most comprehensive object: the **universe**. These intermediate objects are not univocally defined, but their definition is provided according to some specific perspectives.

This is an expression of reductionism (i.e. objects are made of sub-objects) and epistemological pluralism (i.e. objects are always defined according to the perspective of an interpreter, or a class of interpreters).

The ontologies collected in the [emmo-perspectives](emmo-perspectives.owl) are different ways to represent the objects that populate the conceptual region between quantum and universe levels.

The [emmo-existent](emmo-existent.owl) introduces the fundamental non-transitive parthood relations, called direct parthood, that provides a powerful granularity description of multi scale real world objects. The EMMO can in principle represents the **universe** as a direct rooted tree up to its quantum constituents.

The [emmo-impression](emmo-impression.owl) introduces the concept of real world objects that have a meaning for the EMMO user, by means of a recognizable pattern in space or time that impress the user. Under this class the EMMO categorize e.g. formal languages, pictures, geometry, mathematics, sounds. Impressions can be used in a semiotic process as signs.

The [emmo-processsual](emmo-processual.owl) introduces the concept of real world objects that unfold in time in a way that has a meaning for the EMMO user, through the definition of the classes *process* and *participant*.

The [emmo-semiotics](emmo-semiotics.owl) introduces the concept of semiotic process that is used in the EMMO to represent e.g. models, formal languages, theories, information, properties.

### domains
The domains ontologies act as roots for extending the EMMO under specific application domains. Up to now the EMMO includes graphical, geometry, material, mathematics, models, properties, physical properties and usercase. 
 
### EMMO relations
All EMMO relations are subrelations of two roots relations: mereotopology and semiosis. The relation hierarchy extends more vertically (i.e. subrelations) than horizontally (i.e. sibling realtions), facilitating the categorization and inferencing of individual.

## Repository Description
You can find the EMMO ontology at http://emmo.info/emmo.owl

The basic structure of the EMMO is declared in the [base](base) subfolder, and collected by the [emmo-base](emmo-base.owl) ontology.

The main perspectives used by the EMMO for real world objects representation are declared in the [perspectives](perspectives) subfolder, and collected by the [emmo-perspectives](emmo-perspectives.owl) ontology.

The root classes of the domains that are actually addressed by the EMMO (and in development by several H2020 projects initiatives) are declared in the [domains](domains) subfolder, and collected by the [emmo](emmo.owl) ontology.

The OWL2-DL sources are available in RDF/XML format.

## How To Use It
In order to be able to view and navigate the EMMO ontology we recommend to download the Protégé editor at https://protege.stanford.edu/products.php#desktop-protege

The fastest way to access the EMMO is to open the ontology via Protégé via the menu under *File -> Open from URL...* and copy the URL http://emmo.info/emmo.owl: Protégé will automatically download all the necessary dependencies.

The EMMO hierarchy will be visible only after reasoning inference: use *ctrl-R* to start the reasoner and under the *Entities* tab, select the *Classes* subtab and *Inferred* in the scroll button.

It is recommended to use FaCT++ as reasoner. You can select it through the menu *Reasoner*.

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

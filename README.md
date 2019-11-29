# The European Materials Modelling Ontology (EMMO)

## About
EMMO is a multidisciplinary effort to develop a standard representational framework (the ontology) based on current materials modelling knowledge, including physical sciences, analytical philosophy and information and communication technologies. This multidisciplinarity is illustrated by the figure on the title page. It provides the connection between the physical world, materials characterisation world and materials modelling world.

EMMO is released under a [Creative Commons license](LICENSE.md).

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

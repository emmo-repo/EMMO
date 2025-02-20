[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5730500.svg)](https://doi.org/10.5281/zenodo.5730500)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
![CI tests](https://github.com/emmo-repo/EMMO/workflows/CI%20tests/badge.svg)
[![GitHub release](https://img.shields.io/github/v/release/emmo-repo/emmo)](https://emmo-repo.github.io/)


# Elementary Multiperspective Material Ontology (EMMO)

<!-- LOGO -->
<p align="center">
  <a href="https://github.com/emmo-repo/EMMO">
    <img src="doc/emmo-logo.png" alt="EMMO logo" width="180">
  </a>
</p>

EMMO results from a multidisciplinary effort to develop a standard representational framework  that is consistent with scientific principles and methodologies.
It is based on physics, analytical philosophy and information and communication technologies.
EMMO provides a framework for knowledge capture and interoperability in applied science and engineering, especially materials science and manufacturing.
It is released under a Creative Commons CC BY 4.0 license.


## EMMO resources

* [EMMO Wiki] - documentation
* [Publication list] - EMMO-related publication list maintained by EMMC
* [EMMO reference index] - all classes and properties
* [Usage tips] - how to work with EMMO using Protégé
* [EMMO name and logo] - some notes about the name


## EMMO structure
This repository contains the EMMO top- and middle level ontologies, constituting the core of EMMO.
The EMMO top-level ontology is consists of the fundamental mereocausality level and the perspective level, which supports a pluralistic representation of the world.

The EMMO middle-level ontology consists of the reference level, which includes the full standard model of physics and the representation of data and information, and the discipline level, providing a common foundation for different disciplines including metrology, materials and manufacturing.
Each level is implemented in a set of interdependent modules as illustrated in the figure below.
A more detailed figure including all the modules can be found [here](doc/figs/EMMO-structure.png).


<table>
  <tr>
    <td><img src="doc/figs/EMMO-structure-description.png" alt="EMMO structure description" height="480"></td>
    <td><img src="doc/figs/EMMO-structure-overview.png" alt="EMMO structure overview" height="480"></td>
  </tr>
</table>


## Repository Description
The different levels and versions of EMMO can be imported according to the following table:

| Name           | Link                            | Comment                                                                         |
|----------------|---------------------------------|---------------------------------------------------------------------------------|
| emmo           | https://w3id.org/emmo           | Loads all EMMO modules, excluding the full standard model and specialised units |
| emmo-tol       | https://w3id.org/emmo/tlo       | EMMO top level                                                                  |
| emmo-reference | https://w3id.org/emmo/reference | EMMO reference level                                                            |
| emmo-mlo       | https://w3id.org/emmo/mlo       | EMMO middle level                                                               |
| emmo-full      | https://w3id.org/emmo/emmo-full | Loads all EMMO modules, including the full standard model and specialised units |


Also, the following versions of EMMO are provided for ease of use:

| Name            | Link                                  | Comment                                                                                          |
|-----------------|---------------------------------------|--------------------------------------------------------------------------------------------------|
| emmo-for-humans | https://w3id.org/emmo/emmo-for-humans | Version of EMMO middle with IRIs replaced with human readable names. Only intended for examples. |
| emmo-lite       | https://w3id.org/emmo/emmo-lite       | Selected leaf classes and properties for rapid development and deployment in graph databases.    |
| emmo-inferred   | https://w3id.org/emmo/inferred        | Pre-inferred version of EMMO middle level                                                        |

Also, individual levels and modules be imported from the GitHub repository using their IRI.
Use for example https://w3id.org/emmo/perspectives to import the Perspectives level and https://w3id.org/emmo/perspectives/semiotics to import the Semiotics module.
A specific version can be imported by adding the version number after the initial https://w3id.org/emmo/.
For example, https://w3id.org/emmo/1.0.0/perspectives will import Perspectives from version 1.0.0.

> [!NOTE]
> Importing directly from the GitHub repository requires a client that understands `owl:imports`.
> It is also much slower than importing from the links in the above table.

A description of the EMMO Governance, organisation of related repositories, conventions and how to contribute can be found [here](doc/EMMO_governance.md).


## EMMO expressivity and reasoning
EMMO 1.0.0 Reference Level is compliant with OWL2 DL and supports HermiT and FaCT++ reasoners.
The axioms have been optimised to reduce reasoning time, facilitating usage and development.
Developers of EMMO based ontologies are encouraged to use a reasoner to ensure consistency with the overall framework.
However, all relevant inferred axioms have been already included in the ontology, so that the EMMO 1.0.0 can also be used as-is with reasoning based on less expressive rules than OWL2 DL, or without reasoning at all, according to users' needs.


## Domain Ontologies
Based on the EMMO core, a set of domain-level ontologies have developed by the community.
They either import one of the versions of EMMO listed on [https://emmo-repo.github.io/](https://emmo-repo.github.io/) or selected module from EMMO core.
The following table lists the public EMMO-based domain ontologies that we are aware of.
Please create an issue if you have a public domain ontology that you think should be listed here.

| Domain ontology                                                                                                           | Base IRI                                                          |
|---------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| [Characterisation Methodology Domain Ontology (CHAMEO)](https://github.com/emmo-repo/domain-characterisation-methodology) | https://w3id.org/emmo/domain/characterisation-methodology/chameo# |
| [Electrochemistry](https://github.com/emmo-repo/domain-electrochemistry)                                                  | https://w3id.org/emmo/domain/electrochemistry#                    |
| [Battery Ontology](https://github.com/emmo-repo/domain-battery)                                                           | https://w3id.org/emmo/domain/battery#                             |
| [Battery Interface Ontology (BattINFO)](https://big-map.github.io/BattINFO/)                                              | https://w3id.org/battinfo#                                        |
| [Nuclear Energy Ontology](https://github.com/emmo-repo/domain-neo)                                                        | https://w3id.org/emmo/domain/neo#                                 |
| [Nanoindentation Ontology](https://github.com/emmo-repo/domain-nanoindentation)                                           | https://w3id.org/emmo/domain/nanoindentation#                     |
| [Chemical Substance Domain Ontology](https://github.com/emmo-repo/domain-chemical-substance)                              | https://w3id.org/emmo/domain/chemical-substance#                  |
| [Microstructure Domain Ontology](https://github.com/emmo-repo/domain-microstructure)                                      | https://w3id.org/emmo/domain/microstructure#                      |
| [OTE Interface Ontology (OTEIO)](https://github.com/emmo-repo/domain-oteio)                                               | https://w3id.org/emmo/domain/oteio#                               |
| [Coating Domain Ontology](https://github.com/emmo-repo/domain-coating)                                                    | https://w3id.org/emmo/domain/coating#                             |
| [Domain Ontology for Concrete](https://github.com/emmo-repo/domain-concrete)                                              | https://w3id.org/emmo/domain/concrete#                            |
| [Domain ontology for solid oxide fuel cells](https://github.com/emmo-repo/domain-sofc)                                    | https://w3id.org/emmo/domain/sofc#                                |
| [Domain ontology for equivalent circuit models](https://github.com/emmo-repo/domain-equivalent-circuit-model)             | https://w3id.org/emmo/domain/equivalent-circuit-model#            |
| [Domain Ontology for Additive Manufacturing (DOAM)](https://github.com/emmo-repo/domain-doam)                             | https://w3id.org/emmo/domain/doam#                                |
| [Atomistic and Electronic Modelling](https://github.com/emmo-repo/domain-atomistic)                                       | https://w3id.org/emmo/domain/atomistic#                           |
| [Crystallography](https://github.com/emmo-repo/domain-crystallography)                                                    | http://emmo.info/domain-crystallography/crystallography#          |
| [CIF ontology](https://github.com/emmo-repo/CIF-ontology)                                                                 | http://emmo.info/CIF-ontology/ontology/cif_core#                  |
| [Magnetic Materials Ontology (MaMMoS)](https://github.com/MaMMoS-project/MagneticMaterialsOntology/)                      | https://w3id.org/emmo/domain/magnetic_material#                   |
| [General Process Ontology (GPO)](https://github.com/General-Process-Ontology/ontology)                                    | https://gpo.ontology.link/                                        |
| [Ontology for the Battery Value Chain (BVC)](https://github.com/Battery-Value-Chain-Ontology/ontology)                    | https://bvco.ontology.link/                                       |

<!--
| [Mechanical Testing](https://github.com/emmo-repo/domain-mechanical-testing)                                              | http://emmo.info/emmo/domain/mechanical-testing#                  |
-->


## Application Ontologies

EMMO application ontologies are engineered for a specific use or application by reusing and extending concepts from one or more domain ontologies.
Even though that the delineation between "domain" and "application" ontologies are somewhat arbitrary, a main difference is that the application ontologies are generally not developed for reuse by other domain or application ontologies, while such reuse is the main focus of domain ontologies.


---

## Contacts:
You can contact EMMO Authors via emmo@emmc.eu


## Acknowledgement
This work has been supported by several European projects, including:

  - [EMMC-CSA](https://emmc.info) (2016-2019), that has received funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 723867.
  - [SimDOME](https://simdome.eu) (2019-2023), that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 814492.
  - [MarketPlace](https://www.the-marketplace-project.eu) (2018-2022) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 760173.
  - [VIMMP](https://www.vimmp.eu) (2018-2021) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 760907.
  - [OntoTrans](https://cordis.europa.eu/project/id/862136) (2020-2024) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 862136.
  - [ReaxPro](https://cordis.europa.eu/project/id/814416) (2019-2023) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 814416.
  - [OntoCommons](https://cordis.europa.eu/project/id/958371) (2020-2023) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 958371.
  - [OYSTER](https://www.oyster-project.eu/) (2017-2021) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 760827.
  - [NanoMECommons](https://www.nanomecommons.net/) (2021-2025) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 952869.
  - [OpenModel](https://www.open-model.eu/) (2021-2025) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 953167.
  - [SFI PhysMet](https://www.ntnu.edu/physmet/) (2020-2028) that receives funding from the Research Council of Norway, project no. 309584.
  - [BIG-MAP](https://www.big-map.eu/) (2020-2024) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 957189.

This work was conducted using the Protégé resource, which is supported by grant GM10331601 from the National Institute of General Medical Sciences of the United States National Institutes of Health.


[EMMO Wiki]: https://github.com/emmo-repo/EMMO/wiki
[Publication list]: https://emmc.eu/emmo/
[EMMO reference index]: https://w3id.org/emmo/
[Usage tips]: doc/using-protege.md
[EMMO name and logo]: doc/about-name-logo.md

[EMMO versions]: https://emmo-repo.github.io/
[mereocausality]: https://github.com/emmo-repo/EMMO/wiki/Mereocausality

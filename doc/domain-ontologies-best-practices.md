# Best practices for domain ontologies
These are some recommendations for developers of EMMO-based domain ontologies.


## Repository layout
For redirections to work as expected, should the name of domain repositories should be prefixed with `domain-`.

The listing below shows a possible directory layout for a domain ontology names `x`.

```tree
domain-x/
├── LICENSE
├── README.md
├── docs/
│   └── x.md
├── .github
│   ├── env
│   ├── emmocheck_conf.yml
│   └── workflows
│       ├── ci_tests.yml
│       └── cd_ghpages.yml
├── modules/
│   ├── catalog-v001.xml
│   ├── module1.ttl
│   └── module2.ttl
├── catalog-v001.xml
├── contributors.ttl
├── x-local.ttl
├── x-dependencies.ttl
├── x-dynamic.ttl
└── x.ttl
```

Description of files:
- **`LICENSE`**: License file. Recommended license is [CC-BY-4.0].
  If you copy the [license text] literally from [EMMO], GitHub will be able to automatically detect the license.
- **`README.md`**: Markdown-formatted file describing the domain ontology.
  See [domain-electrochemistry] for an example.
- **`docs/`**: Optional sub-directory with additional documentation of the domain ontology.
- **`.github/`**: Optional sub-directory for continuous testing.
- **`.github/env`**: Defines environment variables for the GitHub CI/CD workflows.

  Example:
  ```bash
  ONTOLOGY_NAME=x
  ONTOLOGY_IRI=https://w3id.org/emmo/domain/x
  ```

  Replace `x` with the name of your domain ontology.
- **`.github/emmocheck_conf.yml`**: Optional configurations for the [emmocheck] tool.
- **`.github/workflows/ci_tests.yml`**: GitHub workflow for testing the ontology with [emmocheck].
  Just copy [ci_tests.yml] file as-is from the microscopy domain ontology.
- **`.github/workflows/cd_ghpages.yml`**: GitHub workflow for saving the squashed and inferred versions of the domain ontology to GitHub Pages.
  Just copy [cd_ghpages.yml] file as-is from the microscopy domain ontology.
- **`modules/`**: Optional sub-directory with domain ontology modules.
  This might be useful for large domain ontologies with an internal structure.
- **`catalog-v001.xml`**: Catalog file that maps the versionIRI of domain ontology modules to their file location.
  This allows tools like [Protégé] or [EMMOntoPy] to find and load the domain ontology modules from the local file system increases of the checked out repository, instead of loading them from the web.
  Makes the loading faster and more robust.

  Example context catalog-v001.xml:
  ```xml
  <?xml version="1.0" encoding="UTF-8" standalone="no"?>
  <catalog prefer="public" xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
    <group id="Folder Repository, directory=, recursive=true, Auto-Update=false, version=2" prefer="public" xml:base="">
      <uri name="https://w3id.org/emmo/domain/x/0.0.1/contributors" uri="./contributors.ttl"/>
      <uri name="https://w3id.org/emmo/domain/x/0.0.1/dynamic"      uri="./x-dynamic.ttl"/>
      <uri name="https://w3id.org/emmo/domain/x/0.0.1/dependencies" uri="./x-external.ttl"/>
      <uri name="https://w3id.org/emmo/domain/x/0.0.1/local"        uri="./x-local.ttl"/>
      <uri name="https://w3id.org/emmo/domain/x/0.0.1"              uri="./x.ttl"/>
    </group>
  </catalog>
  ```
  Replace `x` with the name of your domain ontology.
- **`contributors.ttl`**: Turtle file listing contributors that haven't already been defined in any of the depending ontologies.
- **`x-local.ttl`**: Defines the domain ontology, but does not import dependencies.
  If the domain ontology has modules, this file should import the modules using `owl:imports`.
  Otherwise, it defines the classes and properties.
- **`x-dependencies.ttl`**: Turtle file defining external dependencies.
  Imports dependent ontologies as well as `x-local.ttl`.

  Example:
  ```turtle
  @prefix owl: <http://www.w3.org/2002/07/owl#> .
  @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

  <https://w3id.org/emmo/domain/x/dependencies> rdf:type owl:Ontology ;
    owl:versionIRI <https://w3id.org/emmo/domain/x/0.0.1/dependencies> ;
    owl:imports <https://w3id.org/emmo/domain/electrochemistry/0.30.0-beta/electrochemistry>,
                <https://w3id.org/emmo/domain/microstructure/0.3.1> .
  ```
- **`x-dynamic.ttl`**: Imports `x-local.ttl` and `x-dependencies.ttl`.
  This file can be opened in [Protégé], but will load very slow since all dependencies will be loaded recursively.
  Loading it may also fail due to too many requests to GitHub.
- **`x.ttl`**: Imports `x-local.ttl` and squashed version of `x-dependencies.ttl` from GitHub Pages.
  This file can be opened in [Protégé], and will load fast, since it only download one file from the web.
  This is typically preferred main file to load for both developers and users.


## Naming conventions
It is recommended to follow the EMMO naming conventions described [here](https://github.com/emmo-repo/EMMO/blob/master/doc/EMMO_governance.md#emmo-conventions).


## Versioning


## Testing



[CC-BY-4.0]: https://creativecommons.org/licenses/by/4.0/
[license text]: https://raw.githubusercontent.com/emmo-repo/EMMO/refs/heads/master/LICENSE
[EMMO]: https://github.com/emmo-repo/EMMO
[domain-electrochemistry]: https://github.com/emmo-repo/domain-electrochemistry
[Protégé]: https://protege.stanford.edu/products.php#desktop-protege
[EMMOntoPy]: https://github.com/emmo-repo/EMMOntoPy
[emmocheck]: https://emmo-repo.github.io/EMMOntoPy/stable/tools-instructions/#emmocheck
[ci_tests.yml]: https://github.com/emmo-repo/domain-microscopy/blob/master/.github/workflows/ci_tests.yml
[cd_ghpages.yml]: https://github.com/emmo-repo/domain-microscopy/blob/master/.github/workflows/ci_tests.yml

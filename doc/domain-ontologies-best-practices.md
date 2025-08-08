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
├── modules/
│   ├── catalog-v001.xml
│   ├── module1.ttl
│   └── module2.ttl
├── catalog-v001.xml
├── contributors.ttl
├── x-dependencies.ttl
└── x.ttl
```

Description of files:
- **`LICENSE`**: License file. Recommended license is [CC-BY-4.0].
  If you copy the [license text] literally from [EMMO], GitHub will be able to automatically detect the license.
- **`README.md`**: Markdown-formatted file describing the domain ontology.
  See [domain-electrochemistry] for an example.
- **`docs/`**: Optional directory with additional documentation of the domain ontology.
- **`.github/`**: Optional directory for continuous testing.
  This directory (including all its content) should be generated with the [ontokit] tool.
- **`modules/`**: Optional directory with domain ontology modules.
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
  If the domain ontology has modules, this file should import the modules using `owl:imports`.
  Otherwise, it defines the classes and properties.
- **`x-dependencies.ttl`**: Turtle file defining external dependencies.
  Imports dependent ontologies.

  Example:
  ```turtle
  @prefix owl: <http://www.w3.org/2002/07/owl#> .
  @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

  <https://w3id.org/emmo/domain/x/dependencies> rdf:type owl:Ontology ;
    owl:versionIRI <https://w3id.org/emmo/domain/x/0.0.1/dependencies> ;
    owl:imports <https://w3id.org/emmo/domain/electrochemistry/0.30.0-beta/electrochemistry>,
                <https://w3id.org/emmo/domain/microstructure/0.3.1> .
  ```
- **`x.ttl`**: Imports the domain ontology from `modules/`, which in turn imports the squashed version of `x-dependencies.ttl` from GitHub Pages.
  This file can be opened in [Protégé], and will load fast, since it only download one file from the web.


## Naming conventions
It is recommended to follow the EMMO naming conventions described [here](https://github.com/emmo-repo/EMMO/blob/master/doc/EMMO_governance.md#emmo-conventions).


## Versioning


## Setting up continuous testing and continuous deployment (CI/CD)
The [ontokit] tool can be used to setup CI/CD for the domain ontology.


1. Setup GitHub Pages:

   1. Create a orphan branch for GitHub Pages

      Run the following commands on your local machine:

          git checkout --orphan gh-pages
          git push origin gh-pages

   2. Enable GitHub Pages:
      - On GitHub, go to `Settings`.
      - In the memu to the left, select `Pages`.
      - Under `Build and deployment` select "Deploy from a branch"
      - Under `Branch`, select "gh-pages" and `/ (root)` directory

2. Go to the root of the repository and run the following commands:

       python -m venv venv  # create a new virtual environment
       source venv/bin/activate
       pip install EMMOntoPy
       ontokit cicd setup

   This will generate the `.github/` directory and setup a CI/CD system that:
   - run [emmocheck] on the ontology for each commit
   - generate squashed and inferred ontologies (on github pages)
   - generate the squashed ontology with dependencies mentioned above
   - generate reference documentation
   - for new releases, automatically register the new version in ontology registries
   - check dependencies and generate dependency diagram/table
   - whatever else is needed...

The CI/CD framework can be updated with (should seldom be needed)

    ontokit cicd update


## Acknowledging contributors
For each module, use dcterms:creator and dcterms:contributor to acknowledge contributors.
Contributors that are not declared in imported ontologies should be defined in the contributors.ttl file.



[CC-BY-4.0]: https://creativecommons.org/licenses/by/4.0/
[license text]: https://raw.githubusercontent.com/emmo-repo/EMMO/refs/heads/master/LICENSE
[EMMO]: https://github.com/emmo-repo/EMMO
[domain-electrochemistry]: https://github.com/emmo-repo/domain-electrochemistry
[Protégé]: https://protege.stanford.edu/products.php#desktop-protege
[EMMOntoPy]: https://github.com/emmo-repo/EMMOntoPy
[emmocheck]: https://emmo-repo.github.io/EMMOntoPy/stable/tools-instructions/#emmocheck
[ci_tests.yml]: https://github.com/emmo-repo/domain-microscopy/blob/master/.github/workflows/ci_tests.yml
[cd_ghpages.yml]: https://github.com/emmo-repo/domain-microscopy/blob/master/.github/workflows/ci_tests.yml
[ontokit]: https://emmo-repo.github.io/EMMOntoPy/stable/tools-instructions/#ontokit
[emmocheck]: https://emmo-repo.github.io/EMMOntoPy/stable/tools-instructions/#emmocheck

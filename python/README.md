emmo - Python package providing an API to Euroean Materials Modelling Ontology (EMMO)
=====================================================================================
This package is based on [Owlready2] and provides an intuitive
representation of EMMO in Python.

EMMO is an ongoing effort to create an ontology that takes into
account fundamental concepts of physics, chemistry and materials
science and is designed to pave the road for semantic
interoperability.  The aim of EMMO is to be generic and provide a
common ground for describing materials, models and data that can be
adapted by all domains.

EMMO is formulated using OWL.  `emmo` makes it easier to use EMMO for
solving real problems, by providing a natural representation of it in
Python.  No knowledge of OWL is required to use `emmo`.  In `emmo`,
entities in EMMO are represented as Python classes, while individuals
are represented as instances of these. Relations are represented as
class properties.

Below is a basic example showing how to access an entity using `emmo`:

```python
>>> from emmo import get_ontology

>>> emmo = get_ontology('emmo.owl')
>>> emmo.load()
>>> emmo.sync_reasoner()

>>> emmo.matter
emmo.matter

>>> emmo.matter.is_a
[emmo.elementary | emmo.has_proper_part.some(emmo.elementary),
emmo.is_part_of.only(emmo.matter),
emmo.field | emmo.matter,
emmo.physical]
```


Features
--------




Dependencies
------------
  * Python 3.5 or greater
  * [Owlready2]:  Developed and tested for v0.10. Install it with

        pip3 install Owlready2

  * [pydot].  Required for generating graphs.  Install it with

        pip3 install pydot

  * [java]. Needed for reasoning.

  * [pandoc]: Only used for converting generated controlled vocabulary
    from markdown to nicely formatted html or pdf.


[Owlready2]: https://pypi.org/project/Owlready2/
[pydot]: https://pypi.org/project/pydot/
[pandoc]: http://pandoc.org

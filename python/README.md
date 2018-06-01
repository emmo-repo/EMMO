Python package providing an API to Euroean Materials Modelling Ontology (EMMO).

This package is based on Owlready2 and provides an intuitive
representation of EMMO in Python.

Entities are represented as classes, while individuals are represented as
instances of these classes. Relations are represented as class properties.

Below is a simple example showing how to access the "matter" entity in EMMO:

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


Dependencies:
  * Python 3.5 or greater
  * [Owlready2].  Install it with

        pip3 install Owlready2

  * [pydot].  Required for generating
    graphs.  Install it with

        pip3 install pydot


[Owlready2]: https://pypi.org/project/Owlready2/
[pydot]: https://pypi.org/project/pydot/

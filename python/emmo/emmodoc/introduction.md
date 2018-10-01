# Introduction

EMMO is a multidisciplinary effort to develop a standard
representational framework (the ontology) based on current materials
modelling knowledge, including physical sciences, analytical
philosophy and information and communication technologies.
This multidisciplinarity is illustrated by the figure on the title page.

It is based on and consistent with the [Review of Materials
Modelling][RoMM], [CEN Workshop Agreement][CWA] and [MODA
template][MODA].  But in contrast to these, is formalised and provided
in a both machine and human readable way.  It provides the connection
between the physical world, materials characterisation world and
materials modelling world.

![EMMO provides the connection between the physical world, materials
characterisation world and materials modelling world.](html_files/emmo-three_worlds.png){ width=620px }

As illustrated in the figure below, EMMO cover all aspects of
materials modelling and characterisation, including:

  - the **material** itself, which must be described in a rigorous way
  - the **physics laws** that describes the material behaviour
  - the **observation process** involving an observer that percieves the
    real world
  - the **physical models** that approximate the physics laws
  - the **properties** that is measured or modelled
  - the **solver** including the numerical discretisation method that
    leads to a solvable mathimatical representation under certain
    simplifying assumptions
  - the **numerical solver** that performs the calculations
  - the **post processing** of experimental or modelled data

![The aspects of materials modelling and characterisation covered by EMMO.](html_files/emmo-scope.png){ width=260px }



## Primitive elements in EMMO

![The primitive building blocks of EMMO.](html_files/emmo-primitives.png){ width=620px }

### Individuals
Individuals are the basic, "ground level" components of EMMO.  They
may include concrete objects such as cars, flowers, stars, persons and
molecules, as well as abstract individuals such as a measured height,
a specific equation and software programs.  They are a logical picture
of the real world entity they represent.

Individuals are not simple, but possess attributes in form of axioms
that are defined by the user (interpreter) upon declaration.


### Classes
Classes represents concepts.  They are the building blocks that we use
to create an ontology as a representation of knowledge.  We distinguish
between *defined* and *non-defined* classes.

Defined classes are defined by the requirements for being a member
of the class.  In the graphical representations of EMMO, defined
classes are orange.  For instance, in the graph of the top-level
entity branch below, `set` and `abstract` are defined classes.  `set`
is defined via the `has_member` relationship, while `abstract` is
defined via the `has_abstract_part` relationship.

Non-defined classes are defined as an abstract group of objects,
whos members are defined as belonging to the class.  They are yellow
in the graphical representations.

![Example of the top-level entity branch showing some classes and relationships between them.](html_files/entity_branch.png){ width=246px }


### Axioms
Axioms are propositions in a logical framework that define the
relations between the individuals and classes.  They are used to
categorise individuals in classes and to define the *defined* classes.




## Theoretical foundations
EMMO is build upon several theoretical frameworks, including:


### Semiotics
Semiotics is the study of meaning-making.  It is the dicipline
of formulating something that possibly can exists in a defined
space and time in the real world. It is introdused in EMMO via the
`semion` class and used as a way to reduce the complexity of a
physical to a simple sign (symbol).  A `semion` is a physical
entity that represents an abstract object.


### Set theory
Set theory is the theory of membership. This is introduced via
the `set` class, representing the collection of all individuals
(signs) that represents a collection of items.  Sets are defined
via the `has_member` / `is_member_of` relations.


### Mereology
Mereology is the science of parthood.  It is introdused via
the `item` class and based on the mereological `has_part` /
`is_part_of` relations.

EMMO makes a strong distinction between membership and parthood
relations.  In contrast to sets, items can only have parts that
are themselves items.  This means for instance that parthood is
only between substrates of the same dimensionality.  Hence, the
boundary of an item is not a part of the item since it has a lower
dimensionality.

For further information, see [Casati and Varzi "Parts and Places" (1999)][Casati1999].


### Topology
Topology is the study of geometrical properties and spatial
(and time-wise) relations.  It is introdused in combination with
mereology (and therefore often referred to as **mereotopology**) via
the `substrate` class, which represents the place in space and
time in which every real world item exists.  Substrates in EMMO
are always topologically connedted in space and time.

Mereotopological relationships are defined with the `encloses` /
`is_enclosed_by` relations.

### Metrology
Metrology is the science of measurements.  It is used to
introduce units and link them to properties.


### Description logic
[Description logic (DL)][DL] is a formal knowledge representation language
in which the *axioms* are expressed.  It is less expressive than
[first-order logic (FOL)][FOL], but commonly used for providing the
logical formalism for ontologies and semantic web.  EMMO is expressed
in the [Web Ontology Language (OWL)][OWL], which is in turn is based
on DL.  This opens for features like reasoning.

Since it is essential to have a basic notion for OWL and DL, we
include here a very brief overview.  For a proper introduction to OWL
and DL, we refer the reader to sources like [Grau et.al. (2008)][Grau2008],
[OWL2 Primer][OWL2_Primer] and [OWL Reference][OWL_Reference].

OWL distinguishes six between types of class descriptions:

  1. a class identifier (a IRI reference)
  2. an exhaustive enumeration of individuals that together form the instances
     of a class (`owl:oneOf`)
  3. a property restriction (`owl:someValuesFrom`, `owl:allValuesFrom`,
     `owl:hasValue`, `owl:cardinality`, `owl:minCardinality`,
     `owl:maxCardinality`)
  4. the intersection of two or more class descriptions (`owl:intersectionOf`)
  5. the union of two or more class descriptions (`owl:unionOf`)
  6. the complement of a class description (`owl:complementOf`)

Except for the first, all of refer to *defined classes*.  The table
below shows the notation in OWL, DL and the [Manchester OWL
syntax][Manchester_OWL], all commonly used for the definitions.  The
Manchester syntax is used [Protege][Protege] and is designed to be not
use DL symbols and to be easy and quick to read and write.

-----------------------------------------------------------------------------------------
OWL constructor    DL               Manchester        Read                 Meaning
---------------    ---------------- ----------------- -------------------  --------------
                   $A\doteq B$      ?                 A is defined to be   Class *definition*
                                                      equal to B

rdf:subclassOf     $A\sqsubseteq B$ A subclass_of B   all A are B          Class *inclusion*

owl:equivalentTo   $A\equiv B$      A equivalent_to B A is equivalent to B Class *equivalence*

owl:intersectionOf $A\sqcap B$      A and B           A and B              Class *intersection* (*conjunction*)

owl:unionOf        $A\sqcup B$      A or B            A or B               Class *union* (*disjunction*)

owl:complementOf   $\lnot A$        not A             not A                Class *complement* (*negation*)

owl:oneOf          $\{a, b, ...\}$  {a, b, ...}       one of a, b, ...     Class *enumeration*

rdf:type           $a:A$            a is_a A          a is a A             Class *assertion*

                   $(a,b):R$        a object property a is R-related to b  Property *assertion*
                                    assertion b

                   $(a,n):R$        a data property   a is R-related to n  Data *assertion*
                                    assertion n

                   $\top$           ?                 top                  A special class with every individual as an instance

                   $\bot$           ?                 bottom               The empty class

owl:allValuesFrom  $\forall R.A$    R only A          all A with R         [*Universal restriction*][universal_restriction]

owl:someValuesFrom $\exists R.A$    R some A          some A with R        [*Existential restriction*][existential_restriction]

owl:cardinality    $=n R.A$         R exactly n A                          *Cardinality restriction*

owl:minCardinality $\leq n R.A$     R min n                                *Minimum cardinality restriction*

owl:maxCardinality $\geq n R.A$     R max n                                *Minimum cardinality restriction*

owl:hasValue       $\exists R\{a\}$ R value a

rdfs:domain        $\exists R.\top  R domain A
                   \sqsubseteq A$

rdfs:range         $\top\sqsubseteq R range A
                   \forall R.A$

owl:inverseOf      $S\equiv R^-$    S inverse_of R    S is inverse of R    Property *inverse*

-----------------------------------------------------------------------------------------

Table: Notation for DL and Protege. A and B are classes, R is an active
relation, S is an passive relation, i and j are individuals and n is a
literal.

#### Examples
Here are some examples of different class descriptions using both
the DL and Manchester notation.

##### Inclusion (`rdf:subclassOf`)
Inclusion ($sqsubseteq$) defines necessary conditions. Necessary and
sufficient ($\equiv$) conditions defined with equivalence.

An employee is a person.

  **DL:** `employee` $sqsubseteq$ `person`

  **Manchester:** `employee is_a person`

##### Enumeration (`owl:oneOf`)
The color of a wine is either white, rose or red:

  **DL:** `wine_color` $\equiv$ {`white`, `rose`, `red`}

  **Manchester:** `wine_color equivalent_to {white, rose, red}`

##### Property restriction (`owl:someValuesFrom`)
A mother is a woman that has a child (some person):

  **DL:** `mother` $\equiv$ `woman` $\sqcap$ $\exists$`has_child`.`person`

  **Manchester:** `mother equivalent_to woman and has_child some person`

##### Property restriction (`owl:allValuesFrom`)
All parents that only have daughters:

  **DL:** `parents_with_only_daughters` $\equiv$ `person` $\sqcap$ $\forall$`has_child`.`woman`

  **Manchester:** `parents_with_only_daughters equivalent_to person and has_child only woman`

##### Property restriction (`owl:hasValue`)
The owl:hasValue restriction allows to define classes based on the
existence of particular property values. There must be at least one
matching property value.

All children of Mary:

  **DL:** `Marys_children` $\equiv$ `person` $\sqcap$ $\exists$`has_parent`.{`Mary`}

  **Manchester:** `Marys_children equivalent_to person and has_parent value Mary`

##### Property cardinality (`owl:cardinality`)
The owl:cardinality restriction allows to define classes based on the
maximum (owl:maxCardinality), minimum (owl:minCardinality) or exact
(owl:cardinality) number of occurences.

A person with one parent:

  **DL:** `half_orphant` $\equiv$ `person` and =1`has_parent`.`person`

  **Manchester:** `half_orphant equivalent_to person and has_parent exactly 1 person`

##### Intersection (`owl:intersectionOf`)
Individuals of the intersection of two classes, are simultaneously instances
of both classes.

A man is a person that is male:

  **DL:** `man` $\equiv$ `person` $\sqcap$ `male`

  **Manchester:** `man equivalent_to person and male`

##### Union (`owl:unionOf`)
Individuals of the union of two classes, are either instances
of one or both classes.

A person is a man or woman:

  **DL:** `person` $\equiv$ `man` $\sqcup$ `woman`

  **Manchester:** `person equivalent_to man or woman`

##### Complement (`owl:complementOf`)
Individuals of the union of two classes, are either instances
of one or both classes.

A person is a man or woman:

  **DL:** `person` $\equiv$ `man` $\sqcup$ `woman`

  **Manchester:** `person equivalent_to man or woman`





## Important concepts

### Mereotopological composition

#### Substrate

A `substrate` represents the place (in general sense) in which every
real world item exists. It provides the dimensions of existence for
real world entities.  This follows from the fact that everything that
exists is placed somewhere and space and time coordinates can be used
to identify it.

Substrates are always **topologically connected spaces** (a topological
space X is said to be disconnected if it is the union of two disjoint
non-empty open sets.  Otherwise, X is said to be connected).

`substrate` is the superclass of `space`, `time` and their combinations,
like `spacetime`.

*Following Kant, space and time are a priori forms of intuition,
i.e. they are the substrate upon which we place our intuitions,
assigning space and time coordinates to them.*


#### Hybrid
A `hybrid` is the combination of `space` and `time`.  It has the subclasses
`world_line` (0D space + 1D time), `world_sheet` (1D space + 1D time),
`world_volume` (2D space + 1D time) and `spacetime` (3D space + 1D time).


#### Spacetime
EMMO represents real world entities as subclasses of `spacetime`.
A `spacetime` is valid for all reference systems (as required by the
theory of relativity).


#### Matter
`matter` is used to represent a group of `elementary` in an enclosing
`spacetime`.  As illustrated in the figure, a `matter` is an `elementary`
or a composition of other `matter` and `vacuum`.

![Matter.](html_files/emmo-matter.png){ width=540px }

In EMMO is `matter` always a 4D spacetime.  This is a fundamental difference
between EMMO and most other ontologies.

In order to describe the real world, we must also take into account
the vacuum between the `elementary` that composes a higher granularity
level entity (e.g. an atom).

In EMMO `vacuum` is defined as a `spacetime` that has no `elementary` parts.


#### Existent
An `existent` is defined as a `matter` that unfolds in time as a
succession of states.  It is used to represent the whole life of a
complex but structured state-changing `matter` entity, like e.g. an
atom that becomes ionised and then recombines with an electron.

On the contrary, a `matter and not existent` entity is something
"amorphous", randomly collected and not classifiable by common terms
or definitions.  That is a heterogeneous heap of `elementary`,
appearing and disappearing in time.


#### State
A `state` is matter in a particular configurational state.  It is
defined as having spatial direct parts that persists (do not change)
throughout the lifetime of the `state`.  Hence, a `state` is like a
snapshot of a physical in a finite time interval.

![A physical can always be decomposed into a sequence of finite `state`s.](html_files/emmo-state.png){ width=440px }

The use of spatial direct parthood in the definition of `state` means that
a `state` cannot overlap in space with another `state`.

An important feature of states, that follows from the fact that they are
`spacetime`, is that they constitute a finite time interval.


#### Elementary
The basic assumption of decomposition in EMMO, is that the most basic
manifestation of `matter` is represented by a subclass of `spacetime`
called `elementaty`.

The `elementary` class defines the "atomic" (undividable) level in EMMO.
A generic `matter` can always be decomposed in proper parts down to the
`elementary` level using proper parthood.  However, an `elementary` can
still be decomposed in temporal parts, that are themselves `elementary`.

Example of elementaries are electron, photon and quarks.

![Elementary.](html_files/emmo-elementary.png){ width=320px }


### Granularity - direct parthood
Granularity is a central concept of EMMO, which allows the user to
percieve the world at different levels of details (granularity) that
follows physics and materials science perspectives.

![Different levels of granularity.](html_files/emmo-granularity2.png){ width=660px }

Every material in EMMO is placed on a granularity level and the
ontology gives information about the direct upper and direct lower
level classes.  This is done with the non-transitive `is_direct_part_of`
relation.

![Direct parthood.](html_files/emmo-direct_part.png){ width=220px }

Granularity is a defined class and is useful sine a reasoner
automatically can put the individuals defined by the user under a
generic class that clearly expresses the types of its compositional
parts.


### Mathematical entities
The class `mathematical_entities` represents fundamental elements of
mathematical expressions, like numbers, variables, unknowns and
equations.  Mathematical entities are pure mathematical and have no
physical unit.


### Natural law
A `natural_law` is an abstraction for a series of experiments that
tries to define a common cause and effect of the time evolution of a
set of interacting participants.  It is (by definition) a
pre-mathematical entity.

The `natural_law` class is defined as

    is_abstraction_for some experiment

It can be represented e.g. as a thought in the mind of the
experimentalist, a sketch and textual description in a book of
science.

`physical_law` and `material_law` are, according to the [RoMM][RoMM]
and [CWA][CWA], the laws behind physical equations and material
relations, respectively.


### Properties
Properties are abstracts that are related to a specific material
entity with the relation *has_property*, but that depends on a
**specific observation process**, participated by a **specific
observer**, who catch the physical entity behaviour that is abstracted
as a property.

Properties enables to connect a measured property to the measurement
process and the measurement instrument.


## How to read this document

### Annotations
All entities and relations in EMMO have some attributes, including:

- **IRI** (required). The IRI is an

### Graphs
The graphs

### Relations





[RoMM]: https://publications.europa.eu/en/publication-detail/-/publication/ec1455c3-d7ca-11e6-ad7c-01aa75ed71a1
[CWA]: https://www.cen.eu/news/workshops/Pages/WS_2016-013.aspx
[MODA]: https://emmc.info/moda-workflow-templates/
[DL]: https://en.wikipedia.org/wiki/Description_logic
[OWL]: https://en.wikipedia.org/wiki/Web_Ontology_Language
[FOL]: https://en.wikipedia.org/wiki/First-order_logic
[Casati1999]: https://mitpress.mit.edu/books/parts-and-places
[Grau2008]: http://www.cs.ox.ac.uk/boris.motik/pubs/ghmppss08next-steps.pdf
[OWL2_Primer]: https://www.w3.org/TR/owl2-primer/
[OWL_Reference]: https://www.w3.org/TR/owl-ref/
[Manchester_OWL]: http://ceur-ws.org/Vol-216/submission_9.pdf
[universal_restriction]: https://en.wikipedia.org/wiki/Universal_quantifier
[existential_restriction]: https://en.wikipedia.org/wiki/Universal_quantifier
[Protege]: https://protege.stanford.edu/

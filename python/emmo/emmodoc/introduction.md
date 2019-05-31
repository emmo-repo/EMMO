# Introduction

EMMO is a multidisciplinary effort to develop a standard
representational framework (the ontology) based on current materials
modelling knowledge, including physical sciences, analytical
philosophy and information and communication technologies.
This multidisciplinarity is illustrated by the figure on the title page.
It provides the connection between the physical world, materials
characterisation world and materials modelling world.

![EMMO provides the connection between the physical world, materials
characterisation world and materials modelling world.](html_files/emmo-three_worlds.png){ width=620px }

EMMO is based on and is consistent with the [Review of Materials
Modelling][RoMM], [CEN Workshop Agreement][CWA] and [MODA
template][MODA].  However, while these efforts are written for humans,
EMMO is defined using the [Web Ontology Language (OWL)][OWL], which is
machine readable and allows for machine reasoning.  In terms of
semantic representation, EMMO brings everything to a much higher level.

As illustrated in the figure below, EMMO covers all aspects of
materials modelling and characterisation, including:

  - the **material** itself, which must be described in a rigorous way
  - the **observation process** involving an observer that percieves the
    real world
  - the **properties** that is measured or modelled
  - the **physics laws** that describes the material behaviour
  - the **physical models** that approximate the physics laws
  - the **solver** including the numerical discretisation method that
    leads to a solvable mathematical representation under certain
    simplifying assumptions
  - the **numerical solver** that performs the calculations
  - the **post processing** of experimental or simulated data

![The aspects of materials modelling and characterisation covered by EMMO.](html_files/emmo-scope.png){ width=260px }

<!--
ADD MAIN FEATURES OF EMMO FROM GERHARDS SLIDE
-->



## What is an ontology
In short, an ontology is a specification of a conceptualization.  The
word *ontology* has a long history in philosophy, in which it refers
to the subject of existence.  The so-called [ontological
argument][ontological_argument] for the existence of God was proposed
by Anselm of Canterbury in 1078. He defined God as *"that than which
nothing greater can be thought"*, and argued that *"if the greatest
possible being exists in the mind, it must also exist in reality. If
it only exists in the mind, then an even greater being must be
possible -- one which exists both in the mind and in reality"*. Even
though this example has little to do with todays use of ontologies
in computer science, it illustrates the basic idea;  the ontology
defines some basic premises (concepts and relations between them) from
which it is possible reason to gain new knowledge.

For a more elaborated and modern definition of the ontology we refer
the reader to the one provided by [Tom Gruber (2009)][Gruber2009].
Another useful introduction to ontologies is the paper [Ontology
Development 101: A Guide to Creating Your First Ontology][Ontology101]
by Noy and McGuinness (2001), which is based on the [Protege][Protege]
sortware, with which EMMO has been developed.

A taxonomy is a hierarchical representation of classes and subclasses
connected via `is_a` relations.  Hence, it is a subset of the ontology
excluding all, but the `is_a` relations.  The main use of taxonomies
are for classifications.  The figure shows a simple example of a
taxonomy illustrating a categorisation of four classes into a
hierarchy of more higher of levels of generality.

![Example of a taxonomy.](html_files/animal.png){ width=240px }

In EMMO is the taxonomy a rooted directed acyclic graph (DAG).  This
is an important since many classification methods relies on this
property, see e.g. [Valentini (2014)][Valentini2014] and [Robison et
al (2015)][Robison2015].  Note, that EMMO is a DAG does not prevent
some classes from having more than one parent.  A `quantitative_property`
is for instance both `formed` and an `objective_property`.  See
[appendix][Appendix] for the full EMMO taxonomy.


## Primitive elements in EMMO

![The primitive building blocks of EMMO.](html_files/emmo-primitives.png){ width=620px }

### Individuals
Individuals are the basic, "ground level" components of EMMO.  They
may include concrete objects such as cars, flowers, stars, persons and
molecules, as well as abstract individuals such as a measured height,
a specific equation and software programs.

<!--
They are a logical picture of the real world entity they represent.

    Remove this for now, since Anne thinks this sentence no longer
    ahere to realism since we make a distinction between individuals
    and the real world.
-->

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

The simplest form of a class axiom is a class description that just
states the existence of the class and gives it an unique identifier.
In order to provide more knowledge about the class, class axioms
typically contain additional components that state necessary
and/or sufficient characteristics of the class. OWL contains three
language constructs for combining class descriptions into class
axioms:

* `rdfs:subClassOf` allows one to say that the class extension of a
  class description is a subset of the class extension of another
  class description.

* `owl:equivalentClass` allows one to say that a class description has
  exactly the same class extension as another class description.

* `owl:disjointWith` allows one to say that the class extension of a
  class description has no members in common with the class extension
  of another class description.

See the section about [Description logic](#description-logic) for more
information about these language constructs.  Axioms are also used to
define relations between relations. These are further detailed in the
chapter on [Relations].




## Theoretical foundations
EMMO build upon several theoretical frameworks.

### Semiotics
Semiotics is the study of meaning-making.  It is the dicipline
of formulating something that possibly can exists in a defined
space and time in the real world. It is introdused in EMMO via the
`semion` class and used as a way to reduce the complexity of a
physical to a simple sign (symbol).  A `semion` is a physical
entity that represents an abstract object.

<!--
ADD FIGURE
-->


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

Since it is essential to have a basic notion of OWL and DL, we
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

Except for the first, all of these refer to *defined classes*.  The
table below shows the notation in OWL, DL and the [Manchester OWL
syntax][Manchester_OWL], all commonly used for the definitions.  The
Manchester syntax is used by [Protege][Protege] and is designed to not
use DL symbols and to be easy and quick to read and write.  Several
other syntaxes exists for DL.  An interesting example is the pure
Python syntax proposed by [Lamy (2017)][Lamy2017], which is used in
the open source [Owlready2][Owlready2] Python package.

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

owl:minCardinality $\leq n R.A$     R min n A                              *Minimum cardinality restriction*

owl:maxCardinality $\geq n R.A$     R max n A                              *Minimum cardinality restriction*

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
Individuals of the complement of a class, are all individuals that are not
member of the class.

Not a man:

  **DL:** `female` $\equiv$ $\lnot$ `male`

  **Manchester:** `female equivalent_to not male`



## EMMO Structure

EMMO is structures in a hierarchical set of modules covering all
aspects materials modelling.  The modules and their interdependencies
are shows in the figure below.  Each module correspond to a separate
OWL file.  The special module `emmo-all.owl` includes all of EMMO.

![EMMO modules.](html_files/emmo-structure.png){ width=400px }


### EMMO Core
EMMO core contains three levels as illustrated in the figure below.

![Toplevel structure of EMMO Core.](html_files/emmo-core.png){ width=180px }

  - **The abstract conceptual level** makes a clear separation
    between `set` (set theory) and `item` (mereotopology).

  - **The geometric/topological level** contains the space (3D) and time
    (1D) in which all items unfolds.

  - **The physical level** holds the 4D `spacetime` in which all real
    world entities exists.  A `spacetime` that can be perceived by
    (interact with) the interpreater is a `physical`.  If the
    `spacetime` entity is empty in terms of perception, it is a
    `void`.

EMMO defines a parthood hierachy under `physical` by introducing the
following concepts (illustrated in the figure below):

  - **`elementary`** is the fundamental, non-divisible constituent of entities

  - **`state`** is a `physical`whose parts have a constant cardinality
    during its life time

  - **`existent`** is a succession of states

![Parthood hierachy under `physical`.](html_files/physical.png){ width=500px }

Via the mereological direct parthood relation, EMMO can describe
entities made of parts at different levels of granularity.  This is
paramount for cross scale interoperability.  Every material in EMMO is
placed on a granularity level and the ontology gives information about
the direct upper and direct lower level classes using
the non-transitive direct parthood relations.

![Direct parthood.](html_files/emmo-direct_part.png){ width=220px }


### EMMO Materials
EMMO Material contains a first draft of a materials ontology.  It
relies on direct parthood to identify granularity levels.  It is
generic and flexible enough to represent both classical and quantum
mechanical systems in a way that is compatible with different
interpretations (e.g. the Copenhagen and De Broglie-Bohm
interpretations of quantum mechanics) and levels of approximations
(e.g. classical physics and Born-Oppenheimer approximation).


### EMMO Semiotics

The semiotics module introduces three connected branches, `symbolic`,
`semiosis` and `semiotic_role` in addition to the
`has_sign`/`stands_for` family of relations.



Since the EMMO must represent models and properties (which are signs
that stand for a physical entity), the semiotic process must be
described also within the EMMO itself.  The concepts of Peirce
semiotics (interpreter, object, sign) are included in the semiotic
branch, together with the semiosis process.


### EMMO Formal languages




### EMMO Data formats

### EMMO Math

### EMMO Properties

### EMMO Models

### EMMO Characterisation



## How to read this document

### Annotations

All entities and relations in EMMO have some attributes, called
*annotations*.  In many cases, only the necessary *IRI* and *relations* are
provided.  However, more descriptive annotations, like *elucidation*
and *comment* will be added with time.  Possible annotations are:

<!--
- **Definition** is a human readable definition of the class.  Definition
  annotations are currently not used in EMMO.

- **Axiom**
  Currently not used in EMMO.

- **Theorem**
  Currently not used in EMMO.
-->

- **Elucidation** is a human readable explanation and clearification
  of the documented class or relation.

<!--
- **Domain**
  Currently not used in EMMO.

- **Range**
  Currently not used in EMMO.
-->

- **Example** clearifies the elucidation through an example.  A class may
  have several examples, each addressing different aspects.

- **Comment** is a clearifying note complementing the definition and
  elucidation.  A class may have several comments, each clearifying
  different aspects.

- **IRI** stands for *international resource identifier*.  It is an
  identifier that uniquely identifies the class or relation.  IRIs are
  similar to URIs, but are not restricted to the ASCII character set.
  Even though the IRIs used in EMMO appears to be URLs, they currently
  do not point to any existing content. This might change in the
  future.

- **Relations** is a list of relations applying to the current class
  or relation.  The relations for relations are special and will be
  elaborated on in the introduction to chapter [Relations].  Some of
  the listed relations are defined in the OWL sources, while other are
  inferred by the reasoner.

  The relations are using the Manchester OWL syntax introduced in section
  [Description logic](#description-logic).


### Graphs
The generated graphs borrows some syntax from the [Unified Modelling
Language (UML)][UML], which is a general purpose language for software
design and modelling.  The table below shows the style used for the
different types of relations and the concept they corresponds to in
UML.

Relation           UML arrow     UML concept
-------------      -----------   -----------
is-a               ![img][isa]   inheritance
disjoint_with      ![img][djw]   association
equivalent_to      ![img][eqt]   association
encloses           ![img][rel]   aggregation
has_abstract_part  ![img][rel]   aggregation
has_abstraction    ![img][rel]   aggregation
has_representation ![img][rel]   aggregation
has_member         ![img][rel]   aggregation
has_property       ![img][rel]   aggregation

Table: Notation for arrow styles used in the graphs.  Only active
relations are listed. Corresponding passive relations uses the same
style.

[isa]: html_files/arrow-is_a.png "inheritance"
[djw]: html_files/arrow-disjoint_with.png "association"
[eqt]: html_files/arrow-equivalent_to.png "association"
[rel]: html_files/arrow-relation.png "aggregation"


All relationships have a direction.  In the graphical visualisations,
the relationships are represented with an arrow pointing from the
subject to the object.  In order to reduce clutter and limit the size
of the graphs, the relations are abbreviated according to the
following table:

Relation                        Abbreviation
--------                        ------------
has_part only                   hp-o
is_part_of only                 ipo-o
has_member some                 hm-s
is_member_of some               imo-s
has_abstraction some            ha-s
is_abstraction_of some          iao-s
has_abstract_part only          pap-o
is_abstract_part_of only        iapo-o
has_space_slice some            hss-s
is_space_slice_of some          isso-s
has_time_slice some             hts-s
is_time_slice_of some           itso-s
has_projection some             hp-s
is_projection_of some           ipo-s
has_proper_part some            hpp-s
is_proper_part_of some          ippo-s
has_proper_part_of some         hppo-s
has_spatial_direct_part min     hsdp-m
has_spatial_direct_part some    hsdp-s
has_spatial_direct_part exactly hsdp-e

Table: Abbriviations of relations used in the graphical representation
of the different subbranches.


UML represents classes as a box with three compartment; name, attributes
and operators.  However, since the classes in EMMO have no operators and
it gives little meaning to include the OWL annotations as attributes,
we simply represent the classes as boxes.

As already mentioned, defined classes are colored orange, while
undefined classes are yellow.


<!--
## Further work

-->




[RoMM]: https://publications.europa.eu/en/publication-detail/-/publication/ec1455c3-d7ca-11e6-ad7c-01aa75ed71a1
[CWA]: https://www.cen.eu/news/workshops/Pages/WS_2016-013.aspx
[MODA]: https://emmc.info/moda-workflow-templates/
[ontological_argument]: https://en.wikipedia.org/wiki/Ontological_argument
[Valentini2014]: https://arxiv.org/abs/1406.4472
[Robison2015]: https://www.google.no/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0ahUKEwi_2vv-8tXbAhUFiiwKHVRdD4EQFgg1MAE&url=https%3A%2F%2Fwww.springer.com%2Fcda%2Fcontent%2Fdocument%2Fcda_downloaddocument%2F9783319202471-c2.pdf%3FSGWID%3D0-0-45-1510685-p177420182&usg=AOvVaw39c3v4a5PfVMEYDulWpF3w
[Gruber2009]: http://tomgruber.org/writing/ontology-definition-2007.htm
[Ontology101]: http://www.ksl.stanford.edu/people/dlm/papers/ontology-tutorial-noy-mcguinness-abstract.html
[DL]: https://en.wikipedia.org/wiki/Description_logic
[OWL]: https://en.wikipedia.org/wiki/Web_Ontology_Language
[FOL]: https://en.wikipedia.org/wiki/First-order_logic
[Casati1999]: https://mitpress.mit.edu/books/parts-and-places
[Grau2008]: http://www.cs.ox.ac.uk/boris.motik/pubs/ghmppss08next-steps.pdf
[OWL2_Primer]: https://www.w3.org/TR/owl2-primer/
[OWL_Reference]: https://www.w3.org/TR/owl-ref/
[Manchester_OWL]: http://ceur-ws.org/Vol-216/submission_9.pdf
[Owlready2]: https://pythonhosted.org/Owlready2/
[Lamy2017]: http://www.lesfleursdunormal.fr/_downloads/article_owlready_aim_2017.pdf
[universal_restriction]: https://en.wikipedia.org/wiki/Universal_quantifier
[existential_restriction]: https://en.wikipedia.org/wiki/Universal_quantifier
[Protege]: https://protege.stanford.edu/
[UML]: http://www.uml.org/

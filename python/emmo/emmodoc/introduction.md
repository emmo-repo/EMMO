# Introduction

EMMO is a multidisciplinary effort to develop a standard
representational framework (the ontology) based on current materials
modelling knowledge, including physical sciences, analytical
philosophy and information and communication technologies.

![Multidisciplinary aspects of EMMO.](html_files/emmo-multidisciplinary.png){ width=400px }

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
  - the **physical quantity** defined by physics laws that is measured
    or modelled
  - the **solver** including the numerical discretisation method that
    leads to a solvable mathimatical representation under certain
    simplifying assumptions
  - the **numerical solver** that performs the calculations
  - the **post processing** of experimental or modelled data

![The aspects of materials modelling and characterisation covered by EMMO.  **FIXME - add observation/characterisation**](html_files/emmo-scope.png){ width=260px }



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
entity branch below, *set* and *abstract* are defined classes.  *set*
is defined via the *has_member* relationship, while *abstract* is
defined via the *has_abstract_part* relationship.

Non-defined classes are defined as an abstract group of objects,
whos members are defined as belonging to the class.  They are yellow
in the graphical representations.

![Example of the top-level entity branch.](html_files/entity_branch.png){ width=246px }


### Axioms
Axioms are propositions in a logical framework that define the
relations between the individuals and classes.  They are used to
categorise individuals in classes and to define *defined* classes.



## Theoretical foundations
EMMO is build upon several theoretical frameworks, including:

  - **Semiotics** is the study of meaning-making.  It is the dicipline
    of formulating something that possibly can exists in a defined
    space and time in the real world. It is introdused in EMMO via the
    *semion* class and used as a way to reduce the complexity of a
    physical to a simple sign (symbol).  A *semion* is a physical
    entity that represents an abstract object.

  - **Set theory** is the theory of membership. This is introduced via
    the *set* class, representing the collection of all individuals
    (signs) that represents a collection of items.  Sets are defined
    via the *has_member* / *is_member_of* relations.

  - **Mereology** is the science of parthood.  It is introdused via
    the *item* class and based on the mereological *has_part* /
    *is_part_of* relations.

    EMMO makes a strong distinction between membership and parthood
    relations.  In contrast to sets, items can only have parts that
    are themselves itmes.  This means for instance that parthood is
    only between substrates of the same dimensionality.  Hence, the
    boundary of an item is not a part of the item since it has a lower
    dimensionality.

  - **Topology** is the study of geometrical properties and spatial
    (and time-wise) relations.  It is introdused in combination with
    mereology (and therefore often referred to as **mereotopology**) via
    the *substrate* class, which represents the place in space and
    time in which every real world item exists.  Substrates in EMMO
    are always topologically connedted in space and time.

    Mereotopological relationships are defined with the *encloses* /
    *is_enclosed_by* relations.

  - **Metrology** is the science of measurements.  It is used to
    introduce units and link them to properties.



## Mereological composition

### Spacetime
EMMO represents real world entities as subclasses of *spacetime*.
A *spacetime* is valid for all reference systems (as required by the
theory of relativity).


### Elementary
The basic assumption of decomposition in EMMO, is that the most basic
manifestation of *matter* is represented by a subclass of *spacetime*
called *elementaty*.

The *elementary* class defines the "atomic" (undividable) level in EMMO.
A generic *matter* can always be decomposed in proper parts down to the
*elementary* level using proper parthood.  However, an *elementary* can
still be decomposed in temporal parts, that are themselves *elementary*.

Example of elementaries are electron, photon and quarks.


### Vacuum
In order to describe the real world, we must also take into account
the vacuum between the *elementary* that composes a higher granularity
level entity (e.g. an atom).

In EMMO *vacuum* is defined as a *spacetime* that has no *elementary* parts.


### Matter
*matter* is used to represent a group of *elementary* in an enclosing
*spacetime*.  As illustrated in the figure, a *matter* is an *elementary*
or a composition of other *matter* and *vacuum*.

![Matter.](html_files/emmo-matter.png){ width=540px }

In EMMO is *matter* always a 4D spacetime.  This is a fundamental difference
between EMMO and most other ontologies.


### State
A *state* is matter in a particular configurational state.  It is
defined as having spatial direct parts that persists (do not change)
throughout the lifetime of the *state*.  Hence, a *state* is like a
snapshot of a physical in a finite time interval.

![A physical can always be decomposed into a sequence of finite *states*.](html_files/emmo-state.png){ width=440px }

The use of spatial direct parthood in the definition of *state* means that
a *state* cannot overlap in space with another *state*.

An important feature of states, that follows from the fact that they are
*spacetime*, is that they constitute a finite time interval.


## Granularity - direct parthood
Granularity is a central concept of EMMO, which allows the user to
percieve the world at different levels of details (granularity) that
follows physics and materials science perspectives.

![Different levels of granularity.](html_files/emmo-granularity2.png){ width=660px }

Every material in EMMO is placed on a granularity level and the
ontology gives information about the direct upper and direct lower
level classes.  This is done with the non-transitive *is_direct_part_of*
relation.

![Direct parthood.](html_files/emmo-direct_part.png){ width=220px }

Granularity is a defined class and is useful sine a reasoner
automatically can put the individuals defined by the user under a
generic class that clearly expresses the types of its compositional
parts.


## Mathematical entities
The class *mathematical_entities* represents fundamental elements of
mathematical expressions, like numbers, variables, unknowns and
equations.  Mathematical entities are pure mathematical and have no
physical unit.


## Natural law
A *natural_law* is an abstraction for a series of experiments that
tries to define a common cause and effect of the time evolution of a
set of interacting participants.  It is (by definition) a
pre-mathematical entity.

The *natural_law* class is defined as

    is_abstraction_for sime experiment

It can be represented e.g. as a thought in the mind of the
experimentalist, a sketch and textual description in a book of
science.

*physical_law* and *material_law* are, according to the [RoMM][RoMM]
and [CWA][CWA], the laws behind physical equations and material
relations, respectively.


## Properties
Properties are abstracts that are related to a specific material
entity with the relation *has_property*, but that depends on a
**specific observation process**, participated by a **specific
observer**, who catch the physical entity behaviour that is abstracted
as a property.

Properties enables to connect a measured property to the measurement
process and the measurement instrument.


[RoMM]: https://publications.europa.eu/en/publication-detail/-/publication/ec1455c3-d7ca-11e6-ad7c-01aa75ed71a1
[CWA]: https://www.cen.eu/news/workshops/Pages/WS_2016-013.aspx
[MODA]: https://emmc.info/moda-workflow-templates/

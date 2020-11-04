## Important concepts


### Mereotopological composition

<!--
ADD OVERVIEW IMAGE/GRAPH
-->

#### Substrate

A `substrate` represents the place (in general sense) in which every
real world item exists. It provides the dimensions of existence for
real world entities.  This follows from the fact that everything that
exists is placed somewhere in space and time. Hence, its space and
time coordinates can be used to identify it.

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

In EMMO `matter` is always a 4D spacetime.  This is a fundamental difference
between EMMO and most other ontologies.

In order to describe the real world, we must also take into account
the vacuum between the elementaries that composes higher granularity
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
defined as having spatial direct parts that persist (do not change)
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
called `elementary`.

The `elementary` class defines the "atomic" (undividable) level in EMMO.
A generic `matter` can always be decomposed in proper parts down to the
`elementary` level using proper parthood.  An `elementary` can
still be decomposed in temporal parts, that are themselves `elementary`.

Example of elementaries are electrons, photons and quarks.

![Elementary.](html_files/emmo-elementary.png){ width=320px }


### Granularity - direct parthood
Granularity is a central concept of EMMO, which allows the user to
percieve the world at different levels of detail (granularity) that
follow physics and materials science perspectives.

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
The class `mathematical_entity` represents fundamental elements of
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
entity with the relation *has_property*, but that depend on a
**specific observation process**, participated by a **specific
observer**, who catch the physical entity behaviour that is abstracted
as a property.

Properties enable us to connect a measured property to the measurement
process and the measurement instrument.

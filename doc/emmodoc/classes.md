%%
%% This file
%% This is Markdown file, except of lines starting with %% will
%% be stripped off.
%%

%HEADER "EMMO Classes"    level=1

*emmo* is a class representing the collection of all the individuals
(signs) that are used in the ontology. Individuals are declared by the
EMMO users when they want to apply the EMMO to represent the world.


%BRANCHHEAD EMMO
The root of all classes used to represent the world.  It has two children;
*collection* and *item*.

*collection* is the class representing the collection of all the
individuals (signs) that represents a collection of non-connected real world
objects.

*item* Is the class that collects all the individuals that are members
of a set (it's the most comprehensive set individual).  It is the
branch of mereotopology.

%% - based on *has_part* mereological relation that can be axiomatically defined
%% - a fusion is the sum of its parts (e.g. a car is made of several
%%   mechanical parts, an molecule is made of nuclei and electrons)
%% - a fusion is of the same entity type as its parts (e.g. a physical
%%   entity is made of physical entities parts)
%% - a fusion can be partitioned in more than one way
%BRANCH EMMO


%BRANCHDOC Elementary
%BRANCHDOC Perspective


%BRANCHDOC Holistic
%BRANCHDOC Semiotic
%BRANCHDOC Sign
%BRANCHDOC Interpreter
%BRANCHDOC Object
%BRANCHDOC Conventional
%BRANCHDOC Property
%BRANCHDOC Icon
%BRANCHDOC Process


%BRANCHDOC Perceptual
%BRANCHDOC Graphical
%BRANCHDOC Geometrical
%BRANCHDOC Symbol
%BRANCHDOC Mathematical
%BRANCHDOC MathematicalSymbol
%BRANCHDOC MathematicalModel
%BRANCHDOC MathematicalOperator
%BRANCHDOC Metrological
%BRANCHDOC PhysicalDimension     rankdir=RL
%BRANCHDOC PhysicalQuantity
%BRANCHDOC Number
%BRANCHDOC MeasurementUnit
%BRANCHDOC UTF8
%BRANCHDOC SIBaseUnit
%BRANCHDOC SISpecialUnit        rankdir=RL
%BRANCHDOC PrefixedUnit
%BRANCHDOC MetricPrefix         rankdir=RL
%BRANCHDOC Quantity
%BRANCHDOC BaseQuantity
%BRANCHDOC DerivedQuantity      rankdir=RL
%BRANCHDOC PhysicalConstant


%BRANCHDOC Reductionistic
%BRANCHDOC Expression

%BRANCHDOC Physicalistic
%BRANCHDOC ElementaryParticle
%BRANCHDOC Subatomic
%BRANCHDOC Matter
%BRANCHDOC Fluid
%BRANCHDOC Mixture
%BRANCHDOC StateOfMatter

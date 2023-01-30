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


%BRANCHDOC Data
%BRANCHDOC NonEncodedData
%BRANCHDOC EncodedData
%BRANCHDOC Information
%BRANCHDOC DigitalData
%BRANCHDOC Symbolic
%BRANCHDOC MathematicalModel


%BRANCHDOC Holistic
%BRANCHDOC Whole
%BRANCHDOC Role
%BRANCHDOC Fundamental
%BRANCHDOC Redundant
%BRANCHDOC IntentionalProcess
%BRANCHDOC HolisticSystem


%BRANCHDOC Perceptual
%BRANCHDOC Graphical
%BRANCHDOC Geometrical

%BRANCHDOC Chemical
%BRANCHDOC ChemicalComposition
%BRANCHDOC ChemicalFormula
%BRANCHDOC Mathematical
%BRANCHDOC Equation
%BRANCHDOC ProgrammingLanguage
%BRANCHDOC Metrological

%BRANCHDOC Symbol
%BRANCHDOC MathematicalSymbol
%BRANCHDOC MetrologicalSymbol
%BRANCHDOC ChemicalElement




%BRANCHDOC PhysicalDimension     rankdir=RL
%BRANCHDOC PhysicalQuantity
%BRANCHDOC StandardizedPhysicalQuantity
%BRANCHDOC CategorizedPhysicalQuantity
%BRANCHDOC MeasurementUnit
%BRANCHDOC PrefixedUnit
%BRANCHDOC MetricPrefix          rankdir=RL
%BRANCHDOC Quantity
%BRANCHDOC BaseQuantity
%BRANCHDOC DerivedQuantity       rankdir=RL
%BRANCHDOC PhysicalConstant      rankdir=RL


%BRANCHDOC Persistence
%BRANCHDOC Object
%BRANCHDOC Process


%BRANCHDOC Physicalistic
%BRANCHDOC ElementaryParticle
%BRANCHDOC Matter
%BRANCHDOC Fluid
%BRANCHDOC Mixture
%BRANCHDOC StateOfMatter
%BRANCHDOC Material
%BRANCHDOC MolecularEntity
%BRANCHDOC ChemicalSubstance
%BRANCHDOC Atom

%BRANCHDOC GasMixture
%BRANCHDOC SolidMixture
%BRANCHDOC Suspension
%BRANCHDOC Solution
%BRANCHDOC Colloid


%BRANCHDOC Reductionistic


%BRANCHDOC Semiotics
%BRANCHDOC Semiosis

%BRANCHDOC Interpreter
%BRANCHDOC SemioticObject
%BRANCHDOC Sign

%BRANCHDOC Conventional
%BRANCHDOC Subjective
%BRANCHDOC Objective
%BRANCHDOC Icon

%BRANCHDOC Simulation
%BRANCHDOC Declared           rankdir=RL

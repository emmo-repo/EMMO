%%
%% This file
%% This is Markdown file, except of lines starting with %% will
%% be stripped off.
%%

%HEADER "EMMO Relations"    level=1

In the language of OWL, relations are called *properties*.  However,
since relations describe relations between classes and individuals and
since [properties](#Properties) has an other meaning in EMMO, we only call
them *relations*.

[Resource Description Framework (RDF)][RDF] is a W3C standard that is
widely used for describing informations on the web and is one of the
standards that OWL builds on.  RDF expresses information in form of
*subject-predicate-object* triplets.  The subject and object are
resources (aka items to describe) and the predicate expresses a
relationship between the subject and the object.

In OWL are the subject and object classes or individuals (or data)
while the predicate is a relation.  An example of an relationship is
the statement *dog is_a animal*.  Here `dog` is the subject, `is_a`
the predicate and `animal` the object.

%%We distinguish between
%%`active relations` where the subject is acting on the object and
%%`passive relations` where the subject is acted on by the object.

OWL distingues between *object properties*, that link classes or
individuals to classes or individuals, and *data properties* that link
individuals to data values.  Since EMMO only deals with classes, we
will only be discussing object properties.  However,
in actual simulation or characterisation applications build on EMMO,
datatype propertyes will be important.

The characteristics of the different properties are described by
the following *property axioms*:

- `rdf:subPropertyOf` is used to define that a property is a
  subproperty of some other property.  For instance, in the figure
  below showing the relation branch, we see that `active_relation` is
  a subproperty or `relation`.
  The `rdf:subPropertyOf` axioms forms a taxonomy-like tree for relations.

- `owl:equivalentProperty` states that two properties have the same
  property extension.

- `owl:inverseOf` axioms relate active relations to their corresponding
  passive relations, and vice versa. The root relation `relation` is its
  own inverse.

- `owl:FunctionalProperty` is a property that can have only one
  (unique) value y for each instance x, i.e. there cannot be two
  distinct values y1 and y2 such that the pairs (x,y1) and (x,y2) are
  both instances of this property. Both object properties and datatype
  properties can be declared as "functional".

- `owl:InverseFunctionalProperty`

- `owl:TransitiveProperty` states that if a pair (x,y) is an instance
  of P, and the pair (y,z) is instance of P, then we can infer that
  the pair (x,z) is also an instance of P.

- `owl:SymmetricProperty` states that if the pair (x,y) is an instance of P,
  then the pair (y,x) is also an instance of P.
  A popular example of a symmetric property is the `siblingOf` relation.

- `rdfs:domain` specifies which classes the property applies to. Or
  said differently, the valid values of the *subject* in a
  *subject-predicate-object* triplet.

- `rdfs:range` specifies the property extension, i.e. the valid values
  of the *object* in a *subject-predicate-object* triplet.




%HEADER "Root of EMMO relations"      level=2
%BRANCHFIG EMMORelation   caption="Top-level of the EMMO relation hierarchy."
%ENTITY EMMORelation


%%BRANCHDOC mereotopological
%BRANCHHEAD mereotopological
%BRANCH mereotopological


%BRANCHDOC connected

%BRANCHDOC hasPart

%BRANCHDOC semiotical





[RDF]: https://en.wikipedia.org/wiki/Resource_Description_Framework

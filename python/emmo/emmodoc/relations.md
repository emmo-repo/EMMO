;
; This file
; This is Markdown file, except of lines starting with a semi-colon will
; be stripped off.
;

In the language of OWL, relations are called *properties*.  However,
since relations describe relations between classes and individuals and
since [properties](#Properties) has an other meaning in EMMO, we call
them *relations* here.

[Resource Description Framework (RDF)][RDF] is a W3C standard that is
widely used for describing informations on the web and is one of the
standards that OWL builds on.  RDF expresses information in form of
*subject-predicate-object* triplets.  The subject and object are
resources (aka items to describe) and the predicate expresses a
relationship between the subject and the object.

In EMMO, are the subject and object classes or individuals (or data)
while the predicate is a relation.  An example of an relationship is
the statement *dog is_a animal*.  Here is `dog` the subject, `is_a`
the predicate and `animal` the object.  We distinguish between
`active relations` where the subject is acting on the object and
`passive relations` where the subject is acted on by the object.

OWL distingues between `owl:ObjectProperty` that link classes or
individuals to classes or individuals and `owl:DatatypeProperty` that
links individuals to data values.  Since EMMO only deals with classes,
we will only be discussing object properties.  However, in actual
applications build on EMMO, datatype propertyes will be important.

The characteristics of the different properties is described by
the following *property axioms*:

- `rdf:subPropertyOf` is used to define that a property is a
  subproperty of some other property.  For instance, in the figure
  below showing the relation branch, we see that `active_relation` is
  a subproperty or `relation`.

  The `rdf:subPropertyOf` axioms forms a taxonomy-like tree for relations.

<!--
- `rdfs:domain` is not used in EMMO.

- `rdfs:range` is not used in EMMO.
-->

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
  of P, and the pair (y,z) is also instance of P, then we can infer
  the the pair (x,z) is also an instance of P.

- `owl:SymmetricProperty` states that if the pair (x,y) is an instance of P,
  then the pair (y,x) is also an instance of P.

  A popular example of a symmetric property is the `friend_of` relation.



## relation

## encloses

## has_sign

## has_member


## is_enclosed_by

## stands_for

## is_member_of



[RDF]: https://en.wikipedia.org/wiki/Resource_Description_Framework

Tips
====

* Never end a literal annotation with a double quote character.

  At least owlapi escapes the end quote, but not the start quote, in
  literals ending with a double quote when serialising to turtle. That
  makes the quotes in the literal not matching, confusing editors and
  other tools.  The solution is to end literals with something else than
  a double quote (or escape them explicitely).

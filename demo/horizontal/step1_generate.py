import os

from emmo2meta import EMMO2Meta


ontopath = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'vertical', 'case_ontology.owl'))



#e = EMMO2Meta(ontology=ontopath, collid='ASE_Atoms')
e = EMMO2Meta(ontology=ontopath, classes='ASE_Atoms', collid='ASE_Atoms')
e.save('json', 'horizontal.json', 'mode=w')
onto = e.onto

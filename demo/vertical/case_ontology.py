#!/usr/bin/env python3
"""An example script that uses EMMO to describe a vertical use case on
welding aluminium to steel and how the thin layer of intermetallic
that are formed at the interface is influencing the overall
properties.  Based on TEM observations using scanning precision
electron diffraction (SPED) the following (simplified) sequence of
intermetallic phases could be established:

    Al | alpha-AlFeSi | Fe4Al13 | Fe2Al5 | Fe

which is consistent with phase stability when the Fe-concentration is
increasing when going from left to right.

In this case study three scales are considered:

  - Macroscopic scale: predicts the overall mechanical behaviour of
    the welded structure during deformation.

  - Microscopic scale: a local crystal plasticity model of a small
    part of the interface.  The constitutive equations were based on
    the results from DFT.  The results from this model was used to
    calibrate decohesion elements for the macroscopic scale.

  - Electronic scale: elastic properties of the individual phases as
    well work of decohesion within and at the interfaces between the
    phases were calculated with DFT [1].  The calculation of work of
    decohesion was performed as a series of rigid steps, providing
    stress-strain relations in both tensile and shear.

References
----------
[1] Khalid et al. Proc. Manufact. 15 (2018) 1407

"""
from emmo import get_ontology

import ase


# Load EMMO and run reasoner (currently this also includes the materials branch)
emmo = get_ontology('emmo.owl')
emmo.load()
#emmo.sync_reasoner()

# Create a new ontology with out extensions that imports EMMO
onto = get_ontology('onto.owl')
onto.imported_ontologies.append(emmo)
onto.base_iri = 'http://www.emmc.info/emmc-csa/demo#'

# Add new classes and object/data properties needed by the use case
with onto:

    # Relations
    class has_unit(emmo.has_convention):
        label = ['has_unit']

    class is_unit_for(emmo.is_convention_for):
        label = ['is_unit_for']
        inverse_property = has_unit

    #
    # Units
    # -----
    class SI_unit(emmo.measurement_unit):
        """Base class for all SI units."""
        label = ['SI_unit']

    class jourle(SI_unit):
        # To allow the reasoner to help us, we could add an
        # equivalent_to to the mathematical expression kg*m^2/s^2,
        # but it seems a rather complicated thing to do in DL.
        label = ['jourle']

    class square_meter(SI_unit):
        label = ['square_meter']

    class jourle_per_square_meter(SI_unit):
        label = ['jourle_per_square_meter']

    #
    # Properties
    # ----------
    class area(emmo.physical_quantity):
        """Area of a surface."""
        label = ['area']
        is_a = [has_unit.exactly(1, square_meter)]

    class energy(emmo.physical_quantity):
        """Energy."""
        label = ['energy']
        is_a = [has_unit.exactly(1, jourle)]

    class work_of_separation(energy):
        """The work required to separate two materials per boundary area."""
        label = ['work_of_separation']
        is_a = [has_unit.exactly(1, jourle_per_square_meter)]

    class atomic_number(emmo.physical_quantity):
        label = ['atomic_number']

    class atomic_mass(emmo.physical_quantity):
        label = ['atomic_mass']

    class position(emmo.physical_quantity):
        label = ['position']

    #
    # Material classes
    # ----------------
    class boundary(emmo.state):
        """A boundary is a 4D region of spacetime shared by two material
        entities.
        """
        label = ['boundary']
        equivalent_to = [emmo.has_spatial_direct_part.exactly(2, emmo.state)]

    class boundary_surface(emmo.surface):
        """A 2D surface associated with a boundary.

        Commonly referred to as "interface area".
        """
        label = ['boundary_surface']
        is_a = [emmo.has_property.exactly(1, area)]

    class unit_cell(emmo.descriptive_property):
        """Describes a unit cell in a crystal.  Three cell vectors."""
        label = ['unit_cell']

    #
    # Crystallography-related classes
    # -------------------------------
    class crystal(emmo.solid):
        """A periodic crystal structure."""
        label = ['crystal']

    class ASE_Atom(emmo.atom):
        """Representation of a periodic Atoms class in ASE."""
        label = ['ASE_Atom']
        is_a = [emmo.has_property.exactly(1, atomic_number),
                emmo.has_property.exactly(1, atomic_mass),
                emmo.has_property.exactly(1, position),
        ]

    class ASE_Atoms(crystal):
        """Representation of a periodic Atoms class in ASE."""
        label = ['ASE_Atoms']
        is_a = [emmo.has_spatial_direct_part.some(ASE_Atom),
                emmo.has_property.exactly(1, unit_cell)]

    # Add some properties to our atoms
    #emmo.atom.is_a.append(emmo.has_property.exactly(1, atomic_number))
    #emmo.atom.is_a.append(emmo.has_property.exactly(1, atomic_mass))
    #emmo.atom.is_a.append(emmo.has_property.exactly(1, position))




    #class unit_cell(emmo.intensive_property):
    #    """Describes a unit cell in a crystal.  Essentially the three cell vectors."""
    #    pass
    #
    #class PeriodicAtoms(emmo.crystal):
    #    """Representation of a periodic Atoms class in ASE.  This essential
    #    corresponds to a crystal in EMMO."""
    #    equivalent_to = [emmo.has_spatial_direct_part.some(emmo.atom) &
    #                     emmo.has_property.exactly(1, unit_cell)]
    #
    #class atomic_number(emmo.intensive_property):
    #    pass
    #
    #class atomic_mass(emmo.intensive_property):
    #    pass
    #
    #class position(emmo.intensive_property):
    #    pass
    #
    #emmo.atom.equivalent_to.append(emmo.has_property.exactly(1, atomic_number))
    #emmo.atom.equivalent_to.append(emmo.has_property.exactly(1, atomic_mass))
    #emmo.atom.equivalent_to.append(emmo.has_property.exactly(1, position))


    #class crystal_structure(property):
    #    """Represents a simple crystal structure, like fcc, bcc, etc."""
    #    pass
    #
    #class spacegroup(abstract):  # FIXME - be more specific
    #    """A class representing a crystallographic space group."""
    #    pass
    #
    #class has_spacegroup_number(spacegroup >> int):
    #    """A data property for specifying a space group using its number in
    #    International Tables of Crystallography."""
    #    pass


# Save our new extended version of EMMO
onto.save('case_ontology.owl')

graph = onto.get_dot_graph(list(onto.classes()), relations=True)
graph.write_pdf('case_ontology.pdf')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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


# Load EMMO
emmo = get_ontology()
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
        """Associates a unit to a property."""
        label = ['has_unit']

    class is_unit_for(emmo.is_convention_for):
        """Associates a property to a unit."""
        label = ['is_unit_for']
        inverse_property = has_unit

    class has_type(emmo.has_convention):
        """Associates a type (symbol, number...) to a property."""
        label = ['has_type']

    class is_type_of(emmo.is_convention_for):
        """Associates a property to a type (symbol, number...)."""
        label = ['is_type_of']
        inverse_property = has_type

    #
    # Types
    # -----
    class integer(emmo.number):
        label = ['integer']

    class real(emmo.number):
        label = ['real']

    class string(emmo.symbol):
        label = ['string']

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
        is_a = [has_unit.exactly(1, square_meter),
                has_type.exactly(1, real)]

    class energy(emmo.physical_quantity):
        """Energy."""
        label = ['energy']
        is_a = [has_unit.exactly(1, jourle),
                has_type.exactly(1, real)]

    class work_of_separation(energy):
        """The work required to separate two materials per boundary area."""
        label = ['work_of_separation']
        is_a = [has_unit.exactly(1, jourle_per_square_meter),
                has_type.exactly(1, real)]

    class atomic_number(emmo.physical_quantity):
        """Number of protons in the nucleus of an atom."""
        label = ['atomic_number']
        is_a = [has_type.exactly(1, integer)]

    class atomic_mass(emmo.physical_quantity):
        label = ['atomic_mass']
        is_a = [has_type.exactly(1, real)]

    class position(emmo.physical_quantity):
        label = ['position']
        is_a = [has_type.exactly(3, real)]

    class lattice_vector(emmo.physical_quantity):
        """A vector that participitates defining the unit cell."""
        label = ['lattice_vector']
        is_a = [has_type.exactly(3, real)]

    class spacegroup(emmo.descriptive_property):
        """A spacegroup is the symmetry group off all symmetry operations
        that apply to a crystal structure.

        It is typically represented by its Hermann-Mauguin symbol or
        space group number (and setting) from the International tables of
        Crystallography.
        """
        label = ['spacegroup']
        is_a = [has_type.exactly(1, string)]

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


    #
    # Crystallography-related classes
    # -------------------------------

    class crystal_unit_cell(emmo.mesoscopic):
        """A volume defined by the 3 unit cell vectors.  It contains the atoms
        constituting the unit cell of a crystal."""
        label = ['crystal_unit_cell']
        is_a = [emmo.has_spatial_direct_part.some(emmo['e-bonded_atom']),
                emmo.has_property.exactly(3, lattice_vector)]

    class crystal(emmo.solid):
        """A periodic crystal structure."""
        label = ['crystal']
        is_a = [emmo.has_spatial_direct_part.only(crystal_unit_cell),
                emmo.has_property.exactly(1, spacegroup)]


    # Add some properties to our atoms
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, atomic_number))
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, atomic_mass))
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, position))



# Save our new extended version of EMMO
onto.save('case_ontology.owl')

# Create graphs
ontoclasses = set(onto.classes())
graph = onto.get_dot_graph(ontoclasses, relations=True, abbreviations=None)
graph.write_pdf('case_ontology.pdf')

parents = {e.mro()[1] for e in ontoclasses}
classes = ontoclasses.union(parents)
graph2 = onto.get_dot_graph(classes, relations=True)
graph2.write_pdf('case_ontology-parents.pdf')

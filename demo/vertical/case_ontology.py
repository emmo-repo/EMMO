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

    #
    # Relations
    # =========
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
    # =====
    class integer(emmo.number):
        label = ['integer']

    class real(emmo.number):
        label = ['real']

    class string(emmo.symbol):
        label = ['string']

    #
    # Units
    # =====
    class SI_unit(emmo.measurement_unit):
        """Base class for all SI units."""
        label = ['SI_unit']

    class joule(SI_unit):
        # To allow the reasoner to help us, we could add an
        # equivalent_to to the mathematical expression kg*m^2/s^2,
        # but it seems a rather complicated thing to do in DL.
        label = ['joule']

    class square_meter(SI_unit):
        label = ['square_meter']

    class cubic_meter(SI_unit):
        label = ['cubic_meter']

    class pascal(SI_unit):
        label = ['pascal']

    class joule_per_square_meter(SI_unit):
        label = ['joule_per_square_meter']

    class kilogram_per_cubic_meter(SI_unit):
        label = ['kilogram_per_cubic_meter']

    class radian(SI_unit):
        label = ['radian']

    #
    # Properties
    # ==========
    class area(emmo.physical_quantity):
        """Area of a surface."""
        label = ['area']
        is_a = [has_unit.exactly(1, square_meter),
                has_type.exactly(1, real)]

    class measured_volume(emmo.physical_quantity):
        """Volume.  We call it a measured volume to not mix up with the
        `volume` defined in EMMO Core."""
        label = ['measured_volume']
        is_a = [has_unit.exactly(1, cubic_meter),
                has_type.exactly(1, real)]

    class orientation(emmo.physical_quantity):
        """Orientation characterised by three Euler angles."""
        label = ['orientation']
        is_a = [has_unit.exactly(1, radian),
                has_type.exactly(3, real)]

    class density(emmo.physical_quantity):
        """Density."""
        label = ['density']
        is_a = [has_unit.exactly(1, kilogram_per_cubic_meter),
                has_type.exactly(1, real)]

    class energy(emmo.physical_quantity):
        """Energy."""
        label = ['energy']
        is_a = [has_unit.exactly(1, joule),
                has_type.exactly(1, real)]

    class energy_per_area(emmo.physical_quantity):
        label = ['energy_per_area']
        is_a = [has_unit.exactly(1, joule_per_square_meter),
                has_type.exactly(1, real)]

    class pressure(emmo.physical_quantity):
        """The force applied perpendicular to the surface of an object per
        unit area."""
        label = ['pressure']
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(1, real)]

    class elastic_tensor(pressure):
        """The stiffness tensor is a property of a continuous elastic material
        that relates stresses to strains (Hooks's law)."""
        label = ['elastic_tensor']
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(81, real)]

    class plasticity(emmo.physical_quantity):
        """Describes Yield stress and material hardening."""
        label = ['plasticity']
        is_a = [has_unit.exactly(1, pascal),
                has_type.min(2, real)]

    #class youngs_modulus(pressure):
    #    """The extent to which an object resists deformation in respnse to an
    #    applied force.
    #    """
    #    label = ['youngs_module']
    #    is_a = [has_unit.exactly(1, pascal),
    #            has_type.min(1, real)]
    #
    #class poissons_ratio(emmo.physical_quantity):
    #    """A measure for "Poissons effect" - the phenomena that a material
    #    that is stretched in one direction, tends to contract in the
    #    directions perpendicular to the stretching direction.
    #
    #    It is defined as the negative of the ratio of (signed)
    #    transverse strain to (signed) axial strain."""
    #    label = ['poissons_ratio']
    #    is_a = [has_type.exactly(1, real)]

    class work_of_separation(energy_per_area):
        """The work required to separate two materials per boundary area."""
        label = ['work_of_separation']
        is_a = [has_unit.exactly(1, joule_per_square_meter),
                has_type.exactly(1, real)]

    class traction_separation(pressure):
        """The work required to separate two materials per boundary area."""
        label = ['force_of_separation']
        is_a = [has_unit.exactly(1, pascal),
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
    # ================

    # Crystallography-related classes
    # -------------------------------
    class crystal_unit_cell(emmo.mesoscopic):
        """A volume defined by the 3 unit cell vectors.  It contains the atoms
        constituting the unit cell of a crystal."""
        label = ['crystal_unit_cell']
        is_a = [emmo.has_spatial_direct_part.some(emmo['e-bonded_atom']),
                emmo.has_property.exactly(3, lattice_vector),
                emmo.has_property.exactly(1, elastic_tensor)]

    class crystal(emmo.solid):
        """A periodic crystal structure."""
        label = ['crystal']
        is_a = [emmo.has_spatial_direct_part.only(crystal_unit_cell),
                emmo.has_property.exactly(1, spacegroup)]

    # Add some properties to our atoms
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, atomic_number))
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, atomic_mass))
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, position))


    #
    #
    class interface(emmo.surface):
        """A 2D surface associated with a boundary.

        Commonly referred to as "interface".
        """
        label = ['interface']
        is_a = [emmo.has_property.exactly(1, area),
                emmo.has_property.exactly(1, work_of_separation),
                emmo.has_property.exactly(1, traction_separation)]

    class boundary(emmo.state):
        """A boundary is a 4D region of spacetime shared by two material
        entities.
        """
        label = ['boundary']
        is_a = [emmo.has_spatial_direct_part.exactly(2, emmo.state),
                emmo.has_space_slice.exactly(1, interface)]

    class phase(emmo.mesoscopic):
        label = ['phase']
        is_a = [emmo.has_property.exactly(1, elastic_tensor),
                emmo.has_property.exactly(1, density),
                emmo.has_property.exactly(1, plasticity)]

    class fem_unit_cell(emmo.mesoscopic):
        label = ['fem_unit_cell']
        is_a = [emmo.has_property.exactly(1, measured_volume),
                emmo.has_spatial_direct_part.exactly(1, phase),
                emmo.has_space_slice.exactly(1, interface)]

    class cohesive_element(fem_unit_cell):
        label = ['cohesive_element']
        is_a = [boundary,
                emmo.has_property.exactly(1, measured_volume),
                emmo.has_spatial_direct_part.exactly(1, phase),
                emmo.has_space_slice.exactly(1, interface)]

    class bulk_element(fem_unit_cell):
        label = ['bulk_element']
        is_a = [emmo.has_property.exactly(1, measured_volume),
                emmo.has_property.exactly(1, phase)]

    class rve(emmo.mesoscopic):
        """The minimum volume that represents the system in question."""
        label = ['rve']
        is_a = [emmo.has_spatial_direct_part.only(fem_unit_cell)]

    #class grain(crystal):
    #    """The complexity with subgrains is ignored here..."""
    #    label = ['grain']
    #    is_a = [emmo.has_property.exactly(1, orientation),
    #            emmo.has_property.exactly(1, measured_volume),
    #    ]

    #






#onto.sync_reasoner()

# Save our new extended version of EMMO.  It seems that owlready by default
# is appending to the existing ontology.  To avoid that, we simply delete
# the owl file if it already exists.
owlfile = 'case_ontology.owl'
import os
if os.path.exists(owlfile):
    os.remove(owlfile)
onto.save(owlfile)

# Save graph with our new classes
ontoclasses = set(onto.classes())
graph = onto.get_dot_graph(ontoclasses, relations=True)
graph.write_pdf('case_ontology.pdf')
#graph.write_pdf('case_ontology.pdf', prog='fdp')

# Also include the parents of our new classes (this graph becomes
# rather large...)
parents = {e.mro()[1] for e in ontoclasses}
classes = ontoclasses.union(parents)
graph2 = onto.get_dot_graph(classes, relations=True, style='uml',
                            edgelabels=True)
graph2.write_pdf('case_ontology-parents.pdf')

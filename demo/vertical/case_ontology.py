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
        pass

    class is_unit_for(emmo.is_convention_for):
        """Associates a property to a unit."""
        inverse_property = has_unit

    class has_type(emmo.has_convention):
        """Associates a type (symbol, number...) to a property."""
        pass

    class is_type_of(emmo.is_convention_for):
        """Associates a property to a type (symbol, number...)."""
        inverse_property = has_type

    #
    # Types
    # =====
    class integer(emmo.number):
        pass

    class real(emmo.number):
        pass

    class string(emmo.symbol):
        pass

    #
    # Units
    # =====
    class SI_unit(emmo.measurement_unit):
        """Base class for all SI units."""
        pass

    class meter(SI_unit):
        label = ['m']

    class square_meter(SI_unit):
        label = ['m²']

    class cubic_meter(SI_unit):
        label = ['m³']

    class kilogram(SI_unit):
        label = ['kg']

    class pascal(SI_unit):
        label = ['Pa']

    class joule_per_square_meter(SI_unit):
        label = ['J/m²']

    class kilogram_per_cubic_meter(SI_unit):
        label = ['kg/m³']

    class radian(SI_unit):
        label = ['rad']

    #
    # Properties
    # ==========
    class position(emmo.physical_quantity):
        is_a = [has_unit.exactly(1, meter),
                has_type.exactly(3, real)]

    class area(emmo.physical_quantity):
        """Area of a surface."""
        is_a = [has_unit.exactly(1, square_meter),
                has_type.exactly(1, real)]

    class mass(emmo.physical_quantity):
        is_a = [has_unit.exactly(1, kilogram),
                has_type.exactly(1, real)]

    class measured_volume(emmo.physical_quantity):
        """Volume.  We call it a measured volume to not mix up with the
        `volume` defined in EMMO Core."""
        is_a = [has_unit.exactly(1, cubic_meter),
                has_type.exactly(1, real)]

    class orientation(emmo.physical_quantity):
        """Orientation characterised by three Euler angles."""
        is_a = [has_unit.exactly(1, radian),
                has_type.exactly(3, real)]

    class density(emmo.physical_quantity):
        """Density."""
        is_a = [has_unit.exactly(1, kilogram_per_cubic_meter),
                has_type.exactly(1, real)]

    class energy_per_area(emmo.physical_quantity):
        is_a = [has_unit.exactly(1, joule_per_square_meter),
                has_type.exactly(1, real)]

    class pressure(emmo.physical_quantity):
        """The force applied perpendicular to the surface of an object per
        unit area."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(1, real)]

    class elastic_tensor(pressure):
        """The stiffness tensor $c_{ijkl}$ is a property of a continuous
        elastic material that relates stresses to strains (Hooks's
        law) according to

            $\sigma_{ij} = c_{ijkl} \epsilon_{kl}$

        Due to symmetry and using the Voight notation, the stiffness
        tensor can be represented as a symmetric 6x6 matrix

            / c_1111  c_1122  c_1133  c_1123  c_1131  c_1112 \\
            | c_2211  c_2222  c_2233  c_2223  c_2231  c_2212 |
            | c_3311  c_3322  c_3333  c_3323  c_3331  c_3312 |
            | c_2311  c_2322  c_2333  c_2323  c_2331  c_2312 |
            | c_3111  c_3122  c_3133  c_3123  c_3131  c_3112 |
            \\ c_1211  c_1222  c_1233  c_1223  c_1231  c_1212 /

        """
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(36, real)]

    class plasticity(emmo.physical_quantity):
        """Describes Yield stress and material hardening."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.min(2, real)]

    class work_of_separation(energy_per_area):
        """The work required to separate two materials per boundary area."""
        is_a = [has_unit.exactly(1, joule_per_square_meter),
                has_type.exactly(1, real)]

    class traction_separation(pressure):
        """The work required to separate two materials per boundary area."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(1, real)]

    class atomic_number(emmo.physical_quantity):
        """Number of protons in the nucleus of an atom."""
        is_a = [has_type.exactly(1, integer)]

    class lattice_vector(emmo.physical_quantity):
        """A vector that participitates defining the unit cell."""
        is_a = [has_unit.exactly(1, meter),
                has_type.exactly(3, real)]

    class spacegroup(emmo.descriptive_property):
        """A spacegroup is the symmetry group off all symmetry operations
        that apply to a crystal structure.

        It is typically represented by its Hermann-Mauguin symbol or
        space group number (and setting) from the International tables of
        Crystallography.
        """
        is_a = [has_type.exactly(1, string)]

    #
    # Material classes
    # ================

    # Crystallography-related classes
    # -------------------------------
    class crystal_unit_cell(emmo.atomic):
        """A volume defined by the 3 unit cell vectors.  It contains the atoms
        constituting the unit cell of a crystal."""
        is_a = [emmo.has_spatial_direct_part.some(emmo['e-bonded_atom']),
                emmo.has_property.exactly(3, lattice_vector),
                emmo.has_property.exactly(1, elastic_tensor)]

    class crystal(emmo.solid):
        """A periodic crystal structure."""
        is_a = [emmo.has_spatial_direct_part.only(crystal_unit_cell),
                emmo.has_property.exactly(1, spacegroup)]

    # Add some properties to our atoms
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, atomic_number))
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, mass))
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

    # Aassign `measured_volume` as a property of `emmo.volume`
    emmo.volume.is_a.append(emmo.has_property.exactly(1, measured_volume))

    class boundary(emmo.state):
        """A boundary is a 4D region of spacetime shared by two material
        entities.
        """
        is_a = [emmo.has_spatial_direct_part.exactly(2, emmo.state),
                emmo.has_space_slice.exactly(1, interface)]

    class phase(emmo.solid):
        """A phase in a bulk material.

        Other properties, like compositions etc. would normally be
        assigned to a phase, are omitted here because they are not
        essential for this case study."""
        is_a = [emmo.has_property.exactly(1, elastic_tensor),
                emmo.has_property.exactly(1, density),
                emmo.has_property.exactly(1, plasticity)]

    class vertex(emmo.point):
        """A vertex in a finite element unit cell."""
        is_a = [emmo.has_property.exactly(1, position)]

    class fem_unit_cell(emmo.solid):
        """A volume of a real world entity that is represented as a finite
        element unit cell in FEM."""
        is_a = [emmo.has_space_slice.exactly(1, emmo.volume)]

    class cohesive_element(fem_unit_cell):
        is_a = [boundary,
                emmo.has_spatial_direct_part.exactly(2, phase),
                emmo.has_space_slice.min(6, vertex),
                emmo.has_space_slice.exactly(1, interface)]

    class bulk_element(fem_unit_cell):
        is_a = [emmo.has_spatial_direct_part.exactly(1, phase),
                emmo.has_space_slice.min(4, vertex)]

    class rve(emmo.solid):
        """The minimum volume that represents the system in question."""
        is_a = [emmo.has_spatial_direct_part.only(fem_unit_cell)]

    #class grain(crystal):
    #    """The complexity with subgrains is ignored here..."""
    #    label = ['grain']
    #    is_a = [emmo.has_property.exactly(1, orientation),
    #            emmo.has_property.exactly(1, measured_volume),
    #    ]

    #


# Sync attributes to make sure that all classes get a `label` and to
# include the docstrings in the comments
onto.sync_attributes()


# Sync the reasoner - FIXME: figure out how to use Pellet instead of HermiT
#onto.sync_reasoner()


# Save our new EMMO-based ontology.
#
# It seems that owlready2 by default is appending to the existing
# ontology.  To get a clean version, we simply delete the owl file if
# it already exists.
owlfile = 'case_ontology.owl'
import os
if os.path.exists(owlfile):
    os.remove(owlfile)
onto.save(owlfile)


#
# Visualise our new EMMO-based ontology
# =====================================

# Save graph with our new classes
graph = onto.get_dot_graph(list(onto.classes()), relations=True,
                           style='uml', constraint=None)
graph.write_png('figs/case_ontology.png')


# Categories of classes
units = [c for c in onto.classes() if issubclass(c, onto.SI_unit)]
properties = [c for c in onto.classes()
              if issubclass(c, onto.property) and not c in units]
leaf_prop = [c for c in properties if len(c.descendants()) == 1]
materials = [c for c in onto.classes() if issubclass(c, (
    emmo.subatomic, emmo.atomic, emmo.mesoscopic, emmo.continuum))]
subdimensional = [c for c in onto.classes() if issubclass(c, (
    emmo.point, emmo.line, emmo.surface, emmo.volume))]
types = [c for c in onto.classes() if issubclass(c, (
    emmo.number, emmo.symbol))]

# Update the uml-stype to generate
onto._uml_style['graph']['rankdir'] = 'BT'

# Units and properties
#graph = onto.get_dot_graph([onto.SI_unit] + leaf_prop, relations=True,
graph = onto.get_dot_graph([onto.SI_unit] + properties, relations=True,
                           style='uml', constraint=None)
graph.write_png('figs/units+properties.png')

# Types and properties
graph = onto.get_dot_graph(types + leaf_prop, relations=True, style='uml',
                           constraint=None)
graph.write_png('figs/types+properties.png')

# Properties and materials
items = [
    emmo.physical_quantity, emmo['e-bonded_atom']] + materials + subdimensional
graph = onto.get_dot_graph(items, relations=True, style='uml', constraint=None)
graph.write_png('figs/properties+materials.png')

# Material
#items = [emmo.atomic, emmo.continuum, onto.boundary]
items = [emmo.state] + materials
leafs = ['symbolic', 'subatomic', 'mesoscopic', 'standalone_atom']
graph = onto.get_dot_graph(items, leafs=leafs, relations=True,
                           parents=False, style='uml')
graph.write_png('figs/materials.png')

# Also include the parents of our new classes (this graph becomes
# rather large...)
parents = {e.mro()[1] for e in onto.classes()}
classes = list(parents.union(onto.classes())) + [emmo.space]
onto._uml_style['graph']['rankdir'] = 'RL'
graph = onto.get_dot_graph(classes, relations=True, style='uml',
                            edgelabels=True)
graph.write_png('figs/case_ontology-parents.png')

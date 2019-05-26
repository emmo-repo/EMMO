#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dlite

coll = dlite.Collection('json://horizontal.json?mode=r#crystal', True)

Atoms = dlite.Instance('json://atoms.json?mode=r')
atoms = dlite.Instance('json', 'horizontal.json', 'mode=r', 'atoms_Al-Fe4Al13')

#!/usr/bin/env/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# LICENSE
#
# Copyright (c) 2010-2013, GEM Foundation, G. Weatherill, M. Pagani,
# D. Monelli.
#
# The Hazard Modeller's Toolkit is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>
#
# DISCLAIMER
# 
# The software Hazard Modeller's Toolkit (hmtk) provided herein
# is released as a prototype implementation on behalf of
# scientists and engineers working within the GEM Foundation (Global
# Earthquake Model).
#
# It is distributed for the purpose of open collaboration and in the
# hope that it will be useful to the scientific, engineering, disaster
# risk and software design communities.
#
# The software is NOT distributed as part of GEM's OpenQuake suite
# (http://www.globalquakemodel.org/openquake) and must be considered as a
# separate entity. The software provided herein is designed and implemented
# by scientific staff. It is not developed to the design standards, nor
# subject to same level of critical review by professional software
# developers, as GEM's OpenQuake software suite.
#
# Feedback and contribution to the software is welcome, and can be
# directed to the hazard scientific staff of the GEM Model Facility
# (hazard@globalquakemodel.org).
#
# The Hazard Modeller's Toolkit (hmtk) is therefore distributed WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# The GEM Foundation, and the authors of the software, assume no
# liability for use of the software.

# -*- coding: utf-8 -*-
'''
Tests the construction and methods of the 
:class: hmtk.sources.source_model.mtkSourceModel
'''

import unittest
from hmtk.sources.source_model import mtkSourceModel
from hmtk.sources.point_source import mtkPointSource

class TestSourceModel(unittest.TestCase):
    '''
    Module to test the :class: hmtk.sources.source_model.mtkSourceModel
    '''
    def setUp(self):
        self.source_model = None
        
    def test_core_instantiation(self):
        '''
        Simple test to ensure the class is correctly instantiated
        '''
        self.source_model = mtkSourceModel('101', 'Model Name')
        self.assertEqual(self.source_model.id, '101')
        self.assertEqual(self.source_model.name, 'Model Name')
        # No sources on input
        self.assertEqual(self.source_model.get_number_sources(), 0)
        
        # Input correctly
        good_model = [mtkPointSource('101', 'Point 1'), 
                      mtkPointSource('102', 'Point 2')]
        self.source_model = mtkSourceModel('1001', 'Good Model', good_model)
        self.assertEqual(self.source_model.get_number_sources(), 2)
        
        # Input incorrectly - source not as list
        with self.assertRaises(ValueError) as ver:
            self.source_model = mtkSourceModel('1002', 'Bad Model', 
                mtkPointSource('103', 'Point 3'))
            self.assertEqual(ver.exception.message, 
                             'Sources must be input as list!')


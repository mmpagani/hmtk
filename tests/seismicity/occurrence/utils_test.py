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
# License as published by the Free Software Foundation, either version 
# 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>
#
# DISCLAIMER
# 
# The software Hazard Modeller's Toolkit (hmtk) provided herein 
# is released as a prototype implementation on behalf of 
# scientists and engineers working within the GEM Foundation (Global 
# Earthquake Model). 
#
# It is distributed for the purpose of open collaboration and in the 
# hope that it will be useful to the scientific, engineering, disaster
# risk and software design communities. 
# 
# The software is NOT distributed as part of GEM’s OpenQuake suite 
# (http://www.globalquakemodel.org/openquake) and must be considered as a 
# separate entity. The software provided herein is designed and implemented 
# by scientific staff. It is not developed to the design standards, nor 
# subject to same level of critical review by professional software 
# developers, as GEM’s OpenQuake software suite.  
# 
# Feedback and contribution to the software is welcome, and can be 
# directed to the hazard scientific staff of the GEM Model Facility 
# (hazard@globalquakemodel.org). 
# 
# The Hazard Modeller's Toolkit (hmtk) is therefore distributed WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.
# 
# The GEM Foundation, and the authors of the software, assume no 
# liability for use of the software. 

import os
import unittest
import numpy as np

import hmtk.seismicity.occurrence.utils as rec_utils

class RecurrenceTableTestCase(unittest.TestCase):
    """ 
    Unit tests for .
    """
    
    BASE_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')    
    
    def setUp(self):
        """
        """
        # Read initial dataset  
        filename = os.path.join(self.BASE_DATA_PATH, 
                                'completeness_test_cat.csv')
        test_data = np.genfromtxt(filename, delimiter=',', skip_header=1)
        # Create the catalogue A
        self.catalogueA = {'year': test_data[:,3], 
                          'magnitude': test_data[:,17]}

        # Read initial dataset  
        filename = os.path.join(self.BASE_DATA_PATH, 
                                'recurrence_test_cat_B.csv')
        test_data = np.genfromtxt(filename, delimiter=',', skip_header=1)
        # Create the catalogue A
        self.catalogueB = {'year': test_data[:,3], 
                          'magnitude': test_data[:,17]}

        # Read the verification table A
        filename = os.path.join(self.BASE_DATA_PATH, 
                                'recurrence_table_test_A.csv')
        self.true_tableA = np.genfromtxt(filename, delimiter = ',')

        # Read the verification table A
        filename = os.path.join(self.BASE_DATA_PATH, 
                                'recurrence_table_test_B.csv')
        self.true_tableB = np.genfromtxt(filename, delimiter = ',')

    def test_recurrence_table_A(self):
        """
        Basic recurrence table test
        """
        magnitude_interval = 0.1
        self.assertTrue( np.allclose(self.true_tableA, 
            rec_utils.recurrence_table(self.catalogueA['magnitude'], 
                                       magnitude_interval,
                                       self.catalogueA['year'])) )

    def test_recurrence_table_B(self):
        """
        Basic recurrence table test
        """
        magnitude_interval = 0.1
        self.assertTrue( np.allclose(self.true_tableB, 
            rec_utils.recurrence_table(self.catalogueB['magnitude'], 
                                       magnitude_interval,
                                       self.catalogueB['year'])) )

    def test_input_checks_raise_error(self):
        fake_completeness_table = np.zeros((10,10))
        catalogue = {}
        config = {}
        self.assertRaises(ValueError, rec_utils.input_checks, catalogue, 
                config, fake_completeness_table)

    def test_input_checks_simple_input(self):
        completeness_table = [[1900, 2.0]]
        catalogue = {'magnitude': [5.0, 6.0], 'year': [2000, 2000]}
        config = {}
        rec_utils.input_checks(catalogue, config, completeness_table)

    def test_input_checks_use_a_float_for_completeness(self):
        fake_completeness_table = 0.0
        catalogue = {'year': [1900]}
        config = {}
        rec_utils.input_checks(catalogue, config, fake_completeness_table)

    def test_input_checks_use_reference_magnitude(self):
        fake_completeness_table = 0.0
        catalogue = {'year': [1900]}
        config = {'reference_magnitude' : 3.0}
        cmag, ctime, ref_mag, dmag = rec_utils.input_checks(catalogue, 
                config, fake_completeness_table)
        self.assertEqual(3.0, ref_mag)

    def test_input_checks_sets_magnitude_interval(self):
        fake_completeness_table = 0.0
        catalogue = {'year': [1900]}
        config = {'magnitude_interval' : 0.1}
        cmag, ctime, ref_mag, dmag = rec_utils.input_checks(catalogue, 
                config, fake_completeness_table)
        self.assertEqual(0.1, dmag)

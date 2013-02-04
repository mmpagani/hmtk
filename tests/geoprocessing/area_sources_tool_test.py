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

""" Module containing tests for the area sources tools
"""

import unittest
import numpy as np
import shapely.wkt
from shapely.geometry import Polygon
from nrml.models import SourceModel, AreaSource, AreaGeometry
from hmtk.seismicity.catalogue import Catalogue
from hmtk.geoprocessing.area_sources_tool import _find_mid_point, \
        select_earthquakes_in_area_sources

class TestAreaSourceTools(unittest.TestCase):
    """
    """
    def setUp(self):
        sources = []
        # Create a Seismic Source Model with one Area Source
        area_source = AreaSource()
        area_source.geometry = AreaGeometry()
        area_source.name = 'test source'
        polygon = Polygon([(10., 45.), (11., 45.), (11., 46.), (10., 46.)])
        area_source.geometry.wkt = shapely.wkt.dumps(polygon)
        sources.append(area_source)
        # Seismic source model 
        self.source_model = SourceModel(name="test", sources=sources)
        # Catalogue
        datc = np.array([[10.0001, 45.5, 5.0],[9.9999, 45.5, 6.0],
            [11.0001, 46.0001, 7.0]])

        keys = ['longitude','latitude','magnitude']
        self.cat = Catalogue()
        self.cat.load_from_array(keys, datc)

    def test_find_mid_point(self):
        coo = _find_mid_point(self.source_model)
        self.assertEqual(10.5,coo[0])
        self.assertEqual(45.5,coo[1])

    def test_select_earthquakes_in_area_sources(self):
        print self.cat
        select_earthquakes_in_area_sources(self.source_model, self.cat)
        self.assertEqual(1,0)

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

""" This module contains tools helping in geoprocessing operations 
involving area sources.
"""

import numpy as np
import shapely.wkt
from shapely.geometry import asMultiPoint
from nrml.models import AreaSource 
from pyproj import Proj

from shapely import speedups
speedups.enable()

def _find_mid_point(seismic_source_model):
    """ This compute the mean coordinates (lon and lat) of all the vertexes
    of the area source polygons 
    """
    cnt = 0
    los = 0.0
    las = 0.0
    for source in seismic_source_model.sources:
        if isinstance(source, AreaSource):
            print 'Area source:',source.name
            polygon = shapely.wkt.loads(source.geometry.wkt)
            for i in range(0,len(polygon.exterior.coords)-1):
                los += polygon.exterior.coords[i][0]
                las += polygon.exterior.coords[i][1]
                cnt += 1
    return los/cnt, las/cnt

def _get_earthquakes_projected_coords(projection, cat):
    """
    :parameter projection:
        Proj object
    :parameter catalogue:
        An instance of ...
    """
    coop = np.zeros((len(cat.data['longitude']),2))
    print coop
    cnt = 0
    for lon, lat in zip(cat.data['longitude'], cat.data['latitude']):
        x, y = projection(lon,lat)
        coop[cnt,0] = x 
        coop[cnt,1] = y 
        cnt += 1
    return coop

def _find_earthquakes_inside_area_sources(projection, seismic_source_model, 
        eqs_coo):
    """
    :parameter projection:
        AA
    :parameter seismic_source_model:
        AA
    :parameter eqs_coo:
        AA
    """
    mp = asMultiPoint(eqs_coo)
    print mp
    for source in seismic_source_model.sources:
        if isinstance(source, AreaSource):
            print 'Area source:',source.name
            polygon = shapely.wkt.loads(source.geometry.wkt)
            aa = polygon.contains(mp)
            print aa

def select_earthquakes_in_area_sources(seismic_source_model, catalogue):
    """
    For each area source in the catalogue this creates an instance of
    catalogue in a list which is returned as an output

    :parameter seismic_source_model:
        An instance of ...
    :parameter catalogue:
        An instance of ...
    """
    loc, lac = _find_mid_point(seismic_source_model)
    # Set projection
    projection = Proj('+proj=laea +lon_0={0:.4f} +lat_0={0:.4f}'.
            format(loc,lac))  
    # Project all the epicentres in the catalogue
    eqk_coop = _get_earthquakes_projected_coords(projection, catalogue)
    # 
    _find_earthquakes_inside_area_sources(projection, seismic_source_model,
            eqk_coop)

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 color_attribute
                                 A QGIS plugin
 Create a new colum in the layer to hold the color of the feature
                             -------------------
        begin                : 2014-03-04
        copyright            : (C) 2014 by Jordi Castells
        email                : jordi.kstells@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load color_attribute class from file color_attribute
    from color_attribute import color_attribute
    return color_attribute(iface)

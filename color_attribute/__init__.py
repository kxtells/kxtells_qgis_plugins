# -*- coding: utf-8 -*-
"""
/***************************************************************************
 color_attribute
                                 A QGIS plugin
 A description here
                             -------------------
        begin                : 2012-06-22
        copyright            : (C) 2012 by Jordi Castells Sala
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
def name():
    return "Color_to_attribute"
def description():
    return "A description here"
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load color_attribute class from file color_attribute
    from color_attribute import color_attribute
    return color_attribute(iface)

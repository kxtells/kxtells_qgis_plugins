# -*- coding: utf-8 -*-
"""
/***************************************************************************
 color_attributeDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_color_attribute import Ui_color_attribute

# create the dialog for zoom to point
class color_attributeDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_color_attribute()
        self.ui.setupUi(self)



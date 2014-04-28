# -*- coding: utf-8 -*-
"""
/***************************************************************************
 color_attributeDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_color_attribute import Ui_color_attribute
# create the dialog for zoom to point


class color_attributeDialog(QtGui.QDialog, Ui_color_attribute):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

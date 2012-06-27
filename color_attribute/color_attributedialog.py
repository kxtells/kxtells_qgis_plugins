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
    new_attribute = False
    progress_dialog = None

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_color_attribute()
        self.ui.setupUi(self)


    def activate_deactivate_newname(self,index):
        textedit = self.ui.attrNewName

        if index == 0:
            textedit.setEnabled(True)
            self.new_attribute = True
        else:
            textedit.setDisabled(True)
            self.new_attribute = False

    def create_progress_dialog(self,nfeatures):
        self.progress_dialog = QtGui.QProgressDialog("Adding Color Values", "Abort", 0, nfeatures, self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)

    def setProgressValue(self,val):
        self.progress_dialog.setValue(val)

    def finish_progress_dialog(self):
        self.progress_dialog.setValue(self.progress_dialog.maximum())

    def isProgressCanceled(self):
        return self.progress_dialog.wasCanceled()

    def isNewAttribute(self):
        return self.new_attribute

    def getAttributeText(self):
        return self.ui.attrNewName.text()

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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from color_attributedialog import color_attributeDialog

# Use pdb for debugging
import pdb

class color_attribute:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # Create the dialog and keep reference
        self.dlg = color_attributeDialog()
        QObject.connect(self.dlg.ui.layerBox, SIGNAL("currentIndexChanged(int)"), self.on_layerCombo_currentIndexChanged)

        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/color_attribute"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/color_attribute_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
   

    def initGui(self):
        print "color_attribute.py::initGui"
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/color_attribute/icon.png"), \
            u"Color_to_attribute", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Color_to_attribute", self.action)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Color_to_attribute",self.action)
        self.iface.removeToolBarIcon(self.action)

    def check_and_create_attribute(self,layer):
        print "color_attribute.py::check_and_create_attribute"
        # APP breakpoint
        #pyqtRemoveInputHook();pdb.set_trace()

    def fill_color_attribute(self,layer):
        print "color_attribute.py::fill_color_attribute"

    def on_layerCombo_currentIndexChanged(self,g):
        print "color_attribute.py::CurrentIndexChanged ", g
        layercombobox = self.dlg.ui.layerBox
        attributesbox = self.dlg.ui.colorBox
        attributesbox.clear()

        selected_layer = layercombobox.itemData(layercombobox.currentIndex()).toPyObject()
        provider = selected_layer.dataProvider()
        columns = provider.fields()
        
        for key,value in columns.items():
            attributesbox.addItem(value.name(),QVariant(value))

    # run method that performs all the real work
    def run(self):
        print "color_attribute.py::run"
        layercombobox = self.dlg.ui.layerBox
        attributesbox = self.dlg.ui.colorBox

        # APP breakpoint
        #pyqtRemoveInputHook()
        #pdb.set_trace()

        #Fill the combo box
        for layer in self.iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                layercombobox.addItem(layer.name(),QVariant(layer))

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            print "ok pressed: Run!"
            selected_layer = layercombobox.itemData(layercombobox.currentIndex())
            self.check_and_create_attribute(selected_layer)
            self.fill_color_attribute(selected_layer)


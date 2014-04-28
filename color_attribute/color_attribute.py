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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from color_attributedialog import color_attributeDialog
from color_attribute_exceptions import *
import os.path

import re

class color_attribute:
    renderer = None


    #Constants
    NOCOLOR = "#FF00FF"

    def __init__(self, iface):
        # By default do not use visual feedback
        # Fun to see (select, deselect). But slow as an old mule
        self.visual_feedback = False

        # Save reference to the QGIS interface
        self.iface = iface

        # Create the dialog and keep reference
        self.dlg = color_attributeDialog()
        QObject.connect(self.dlg.ui.layerBox, 
                        SIGNAL("currentIndexChanged(int)"), 
                        self.on_layerCombo_currentIndexChanged)


        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'color_attribute_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/color_attribute/icon.png"),
            u"color to attribute", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&color_attribute", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&color_attribute", self.action)
        self.iface.removeToolBarIcon(self.action)

    ##################################################################
    #
    #
    # Plugin functions dealing with the colors of the renderers
    #
    #
    ##################################################################

    def check_and_create_attribute(self,layer,newattrtext):
        """ 
            Creates a new String attribute for the layer 
            Returns the new QgsField.
            Raises exceptions for any possible error
        """
        newattrindex = -1 
        qgsfield = None
        
        if not re.match("^[A-Za-z0-9_-]*$", newattrtext):
            raise InvalidAttributeName
        if len(newattrtext)==0:
            raise EmptyAttributeName

        try:
            caps = layer.dataProvider().capabilities()
            
            if caps & QgsVectorDataProvider.AddAttributes: #Is that something good?
                #layer.startEditing()
                qgsfield = QgsField(newattrtext, QVariant.String)

                layer.dataProvider().addAttributes([qgsfield])
                #layer.updateFieldMap()
                layer.reload()
                #newattrindex = layer.dataProvider().fieldNameIndex(newattrtext)

                layer.commitChanges()
        
        except Exception as e:
            raise e

        return qgsfield

    def fill_color_attribute_custom_renderer(self,renderer):
        reply = QMessageBox.information(self.dlg, 'Message',""
                                       ("This layer uses a custom renderer."
                                        " This is currently not supported by the plugin")
                                        ,""
                                       )

    def fill_color_attribute_singlesymbol_renderer(self,renderer):
        """ Set the single color into each of the features """
        layer = self.layer
        attribute = self.attribute
        colorstr = str(renderer.symbol().color().name())
        provider = layer.dataProvider()
        feat = QgsFeature()

        newattrs = { attribute : colorstr}

        #layer.selectAll()

        layer.startEditing()

        iter = layer.getFeatures()
        step = 0
        for feat in iter:
            if self.dlg.isProgressCanceled():
                break;

            fid = feat.id()
            provider.changeAttributeValues({ fid : newattrs })
            #layer.deselect(fid) #Not sure
            
            self.dlg.setProgressValue(step)
            step += 1
        
        self.dlg.finish_progress_dialog()
        layer.commitChanges()

    def fill_color_attribute_rendererV2(self):
        """ Fill the color attribute using a renderer V2"""

        renderer = self.renderer
        rtype = type(renderer)
        if rtype == QgsSingleSymbolRendererV2:
            self.fill_color_attribute_singlesymbol_renderer(renderer)
        elif rtype == QgsCategorizedSymbolRendererV2:
            pass
            #self.fill_color_attribute_categorizedsymbol_renderer(renderer)
        elif rtype == QgsGraduatedSymbolRendererV2:
            pass
            #self.fill_color_attribute_graduatedsymbol_renderer(renderer)
        else:
            pass
            #self.fill_color_attribute_custom_renderer(renderer)

    def fill_color_attribute(self):
        layer = self.layer
        
        self.renderer = layer.rendererV2()
        self.fill_color_attribute_rendererV2()

    ##################################################################
    #
    #
    # GUI data fillers
    #
    #
    ##################################################################

    def on_layerCombo_currentIndexChanged(self,g):
        """ Fill the attributes combo box with the current layer attributes """
        layercombobox = self.dlg.ui.layerBox
        attributesbox = self.dlg.ui.colorBox
        selected_layer = layercombobox.itemData(layercombobox.currentIndex())
        
        if selected_layer == None: return
        attributesbox.clear()

        provider = selected_layer.dataProvider()
        columns = provider.fields()
        
        attributesbox.addItem("New Attribute",None)
        attributesbox.insertSeparator(1000)
        for qgsfield in columns:
            attributesbox.addItem(qgsfield.name(),qgsfield)



    # run method that performs all the real work
    def run(self):
        layercombobox = self.dlg.ui.layerBox
        attributesbox = self.dlg.ui.colorBox

        layercombobox.clear()
        attributesbox.clear()

        # APP breakpoint
        #pyqtRemoveInputHook()
        #pdb.set_trace()

        #Fill the combo box
        for layer in self.iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                layercombobox.addItem(layer.name(),layer)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        if result == 1:
            selected_layer = layercombobox.itemData(layercombobox.currentIndex())
            self.layer = selected_layer
            self.layer.setReadOnly(False)
            
            if self.dlg.isNewAttribute():
                newattname = self.dlg.getAttributeText()
                selected_attribute = self.check_and_create_attribute(self.layer,newattname)
                
                if selected_attribute <0:
                    reply = QMessageBox.critical(self.dlg, 'Error',""
                                                "Problem adding new attribute",""
                                                ) 
                    return
            else:
                selected_attribute = attributesbox.itemData(attributesbox.currentIndex())
            
            self.attribute = layer.dataProvider().fields().indexFromName(selected_attribute.name())
            self.dlg.create_progress_dialog(self.layer.featureCount())
            self.fill_color_attribute()


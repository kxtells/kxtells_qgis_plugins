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

import re

# Use pdb for debugging
import pdb

class color_attribute:
    renderer = None
    layer = None
    attribute = None

    #Constants
    NOCOLOR = "#FF00FF"

    ##################################################################
    #
    #
    # Initializations and plugin load/unload functions
    #
    #
    ##################################################################
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
            returns new attribute index (-1 if no new attribute is created)
        """
        newattrindex = -1 
        
        if not re.match("^[A-Za-z0-9_-]*$", newattrtext):
            return -1
        if len(newattrtext)==0:
            return -1

        try:
            caps = layer.dataProvider().capabilities()
            
            if caps & QgsVectorDataProvider.AddAttributes:
                layer.dataProvider().addAttributes( [ QgsField(newattrtext, QVariant.String) ] )
                layer.updateFieldMap()
                newattrindex = layer.dataProvider().fieldNameIndex(newattrtext)
        
        except:
            pass

        return newattrindex

    def fill_color_attribute_custom_renderer(self,renderer):
        reply = QMessageBox.information(self.dlg, 'Message',""
                                       "This layer uses a custom renderer. This is currently not supported by the plugin",""
                                       )

    def fill_color_attribute_singlesymbol_renderer(self,renderer):
        """ Set the single color into each of the features """
        layer = self.layer
        attribute = self.attribute
        colorstr = str(renderer.symbol().color().name())
        provider = layer.dataProvider()
        feat = QgsFeature()

        newattrs = { attribute : QVariant(colorstr)}

        provider.select(provider.attributeIndexes())
        step = 0
        while provider.nextFeature(feat):
            if self.dlg.isProgressCanceled():
                break;

            fid = feat.id()
            provider.changeAttributeValues({ fid : newattrs })
            
            self.dlg.setProgressValue(step)
            step += 1
        
        self.dlg.finish_progress_dialog()
    

    def fill_color_attribute_graduatedsymbol_renderer(self,renderer):
        """ Set the color with a graduated symbol renderer """
        layer = self.layer
        attribute = self.attribute
        provider = layer.dataProvider()
        attrvalindex = provider.fieldNameIndex(renderer.classAttribute())
        feat = QgsFeature()

        provider.select(provider.attributeIndexes())
        step = 0
        while provider.nextFeature(feat):
            if self.dlg.isProgressCanceled():
                break;

            fid = feat.id()
            attribute_map = feat.attributeMap()
            value = float(attribute_map[attrvalindex].toString())
            
            colorval = self.NOCOLOR
            
            for r in renderer.ranges():
                if value >= r.lowerValue() \
                    and value <= r.upperValue() \
                    and colorval == self.NOCOLOR:
                        colorval = r.symbol().color().name()

            newattrs = { attribute : QVariant(colorval)}
            provider.changeAttributeValues({ fid : newattrs })

            self.dlg.setProgressValue(step)
            step += 1

        self.dlg.finish_progress_dialog()


    def fill_color_attribute_categorizedsymbol_renderer(self,renderer):
        """ Set the color with a categorized symbol renderer """
        layer = self.layer
        attribute = self.attribute
        provider = layer.dataProvider()
        attrvalindex = provider.fieldNameIndex(renderer.classAttribute())
        feat = QgsFeature()
        categories = renderer.categories()

        provider.select(provider.attributeIndexes())
        step = 0

        while provider.nextFeature(feat):
            if self.dlg.isProgressCanceled():
                break;

            fid = feat.id()
            attribute_map = feat.attributeMap()

            catindex = renderer.categoryIndexForValue(attribute_map[attrvalindex].toString())
            
            if catindex != -1: 
                colorval = categories[catindex].symbol().color().name()
            else: 
                colorval = self.NOCOLOR

            newattrs = { attribute : QVariant(colorval)}
            provider.changeAttributeValues({ fid : newattrs })
            
            self.dlg.setProgressValue(step)
            step += 1
        
        self.dlg.finish_progress_dialog()

    def fill_color_attribute_rendererV2(self):
        """ Fill the color attribute using a renderer V2"""

        renderer = self.renderer
        rtype = type(renderer)
        if rtype == QgsSingleSymbolRendererV2:
            self.fill_color_attribute_singlesymbol_renderer(renderer)
        elif rtype == QgsCategorizedSymbolRendererV2:
            self.fill_color_attribute_categorizedsymbol_renderer(renderer)
        elif rtype == QgsGraduatedSymbolRendererV2:
            self.fill_color_attribute_graduatedsymbol_renderer(renderer)
        else:
            self.fill_color_attribute_custom_renderer(renderer)

    def fill_color_attribute_rendererV1(self):
        """ Fill the color attribute using a renderer V1"""
        reply = QMessageBox.information(self.dlg, 'Message',"",
                                       "This layer uses an old simbology renderer. This is currently not supported by the plugin",""
                                       )

    def fill_color_attribute(self):
        layer = self.layer
        
        if layer.isUsingRendererV2():
            self.renderer = layer.rendererV2()
            self.fill_color_attribute_rendererV2()

        else:
            self.renderer = layer.renderer()
            self.fill_color_attribute_rendererV1()


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
        selected_layer = layercombobox.itemData(layercombobox.currentIndex()).toPyObject()
        
        if selected_layer == None: return
        attributesbox.clear()

        provider = selected_layer.dataProvider()
        columns = provider.fields()
        
        attributesbox.addItem("New Attribute",None)
        attributesbox.insertSeparator(1000)
        for key,value in columns.items():
            attributesbox.addItem(value.name(),QVariant(key))



    ##################################################################
    #
    #
    # MAIN Method
    #
    #
    ##################################################################
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
                layercombobox.addItem(layer.name(),QVariant(layer))

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        if result == 1:
            selected_layer = layercombobox.itemData(layercombobox.currentIndex()).toPyObject()
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
                selected_attribute = attributesbox.itemData(attributesbox.currentIndex()).toPyObject()
            
            self.attribute = selected_attribute
            self.dlg.create_progress_dialog(self.layer.featureCount())
            self.fill_color_attribute()


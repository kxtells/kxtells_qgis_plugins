# -*- coding: utf-8 -*-
"""
/***************************************************************************
 color_attribute
                                 A QGIS plugin
  Create a new colum in the layer to hold the color of the feature
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Jordi Castells
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
import re

from qgis.PyQt.QtCore import (QSettings, QTranslator, qVersion, QCoreApplication, QObject, Qt, QVariant)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QWidget, QProgressBar,
    QPushButton, QApplication, QAction)

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .color_attribute_dialog import color_attributeDialog
from .color_attribute_exceptions import *
import os.path

from qgis.core import (QgsProject, Qgis, QgsMessageLog, QgsVectorDataProvider, QgsField, QgsFeature,
                       QgsSingleSymbolRenderer, QgsCategorizedSymbolRenderer, QgsGraduatedSymbolRenderer)

class color_attribute:
    """QGIS Plugin Implementation."""

    NOCOLOR = "#FF00FF"

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'color_attribute_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ColorToAttribute')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        self.new_attribute = False

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('color_attribute', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/color_attribute/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'color to attribute'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ColorToAttribute'),
                action)
            self.iface.removeToolBarIcon(action)

    ##################################################################
    #
    # Basic progress bar
    #
    ##################################################################

    def start_progress_bar(self, maxval, message):
        """ Create a progress bar into the messagebar """
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        progressMessageBar = self.iface.messageBar().createMessage(message)
        self.progress.setMaximum(maxval)
        progressMessageBar.layout().addWidget(self.progress)

        self.iface.messageBar().pushWidget(progressMessageBar,
                                           Qgis.Info)

    def set_progress_value(self, value):
        """ update a previously created progress bar.
            Ignore if there is no progress bar
        """
        if self.progress is None:
            return  # TODO do something here?
        self.progress.setValue(value)

    def cancel_progress_bar(self):
        """ Cancel the progress bar """
        self.progress_cancelled = True
        raise InvalidAttributeName


    def load_combobox_layers(self):
        """ Loads the combobox with existing layers """

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()
        # Clear the contents of the comboBox from previous runs
        self.dlg.layer_combobox.clear()
        # Populate the comboBox with names of all the loaded layers
        for layer in layers:
            self.dlg.layer_combobox.addItem(layer.name(), layer)

    def on_layer_combobox_currentIndexChanged(self, g):
        """ Fill the attributes combo box with the current layer attributes """
        layercombobox = self.dlg.layer_combobox
        attributesbox = self.dlg.attribute_combobox

        selected_layer = layercombobox.itemData(layercombobox.currentIndex()).layer()

        if selected_layer is None:
            #Maybe add an error message here
            return

        attributesbox.clear()

        attributesbox.addItem("New Attribute", None)
        attributesbox.insertSeparator(1000)
        for field in selected_layer.fields():
            attributesbox.addItem(field.name(), field)

    def on_attribute_combobox_currentIndexChanged(self, idx):
        """
            When attribute changes enables or disables the line
            edit, and marks if this is a new_attribute or not
        """
        if idx == 0:
            self.dlg.lineEdit.setEnabled(True)
            self.new_attribute = True
        else:
            self.dlg.lineEdit.setDisabled(True)
            self.new_attribute = False

    def check_and_create_attribute(self, layer, newattrtext):
        """
            Creates a new String attribute for the layer
            Returns the new QgsField. Or None if it was not
            created
        """
        qgsfield = None

        if not re.match("^[A-Za-z0-9_-]*$", newattrtext):
            raise InvalidAttributeName
        if len(newattrtext) == 0:
            raise EmptyAttributeName

        # If it already exists, return the existing index
        layer_fields = layer.fields()
        existing_index = layer_fields.indexFromName(newattrtext)
        if existing_index != -1:
            QgsMessageLog.logMessage("Using existing field. It will be overwritten",
                                     'color_attribute', level=Qgis.Warning)
            return layer_fields[existing_index]

        try:
            caps = layer.dataProvider().capabilities()

            QgsMessageLog.logMessage(str(caps), 'color_attribute', level=Qgis.Info)

            if caps & QgsVectorDataProvider.AddAttributes:  # Is that something good?
                qgsfield = QgsField(newattrtext, QVariant.String)
                layer.setReadOnly(False)


                layer.dataProvider().addAttributes([qgsfield])
                layer.reload()

                #layer.commitChanges()

        except Exception as e:
            raise e

        return qgsfield

    def fill_color_attribute_singlesymbol_renderer(self, layer, attribute):
        """
            Set the single color into each of the features
            layer : QgsVectorDataProvider
            attribute : QgsField
        """
        renderer = layer.renderer()
        colorstr = str(renderer.symbol().color().name())
        provider = layer.dataProvider()
        attribute_index = layer.dataProvider().fields().indexFromName(attribute.name())

        if attribute_index < 0:
            raise InternalPluginError

        newattrs = {attribute_index: colorstr}

        step = 0
        for feat in layer.getFeatures():
            fid = feat.id()
            provider.changeAttributeValues({fid: newattrs})

            self.set_progress_value(step)
            step += 1

        #layer.commitChanges()

    def fill_color_attribute_categorizedsymbol_renderer(self, layer, attribute):
        """ Set the color with a categorized symbol renderer """
        renderer = layer.renderer()
        provider = layer.dataProvider()
        attribute_index = layer.dataProvider().fields().indexFromName(attribute.name())
        attrvalindex = provider.fieldNameIndex(renderer.classAttribute())
        categories = renderer.categories()

        if attribute_index < 0:
            raise InternalPluginError

        step = 0
        for feat in layer.getFeatures():
            fid = feat.id()
            attribute_map = feat.attributes()

            catindex = renderer.categoryIndexForValue(attribute_map[attrvalindex])

            if catindex != -1:
                colorval = categories[catindex].symbol().color().name()
            else:
                colorval = self.NOCOLOR

            newattrs = {attribute_index: colorval}
            provider.changeAttributeValues({fid: newattrs})

            self.set_progress_value(step)
            step += 1

        #layer.commitChanges()

    def fill_color_attribute_graduatedsymbol_renderer(self, layer, attribute):
        """ Set the color with a graduated symbol renderer """
        renderer = layer.renderer()
        provider = layer.dataProvider()
        attribute_index = layer.dataProvider().fields().indexFromName(attribute.name())
        attrvalindex = provider.fieldNameIndex(renderer.classAttribute())
        feat = QgsFeature()

        if attribute_index < 0:
            raise InternalPluginError

        step = 0
        for feat in layer.getFeatures():

            fid = feat.id()
            attribute_map = feat.attributes()
            value = float(attribute_map[attrvalindex])

            colorval = self.NOCOLOR

            for r in renderer.ranges():
                if value >= r.lowerValue() \
                   and value <= r.upperValue() \
                   and colorval == self.NOCOLOR:
                        colorval = r.symbol().color().name()

            newattrs = {attribute_index: colorval}
            provider.changeAttributeValues({fid: newattrs})

            self.set_progress_value(step)
            step += 1

        #layer.commitChanges()

    def fill_color_attribute(self, layer, attribute):
        """ Fill the color attribute using the proper QgsVectorDataProvider renderer """

        renderer = layer.renderer()
        rtype = type(renderer)


        if rtype == QgsSingleSymbolRenderer:
            self.fill_color_attribute_singlesymbol_renderer(layer, attribute)
        elif rtype == QgsCategorizedSymbolRenderer:
            self.fill_color_attribute_categorizedsymbol_renderer(layer, attribute)
        elif rtype == QgsGraduatedSymbolRenderer:
            self.fill_color_attribute_graduatedsymbol_renderer(layer, attribute)
        else:
            raise UnimplementedRenderer(renderer.__class__.__name__)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = color_attributeDialog()

        self.dlg.layer_combobox.currentIndexChanged.connect(self.on_layer_combobox_currentIndexChanged)
        self.dlg.attribute_combobox.currentIndexChanged.connect(self.on_attribute_combobox_currentIndexChanged)

        self.load_combobox_layers()

        layercombobox = self.dlg.layer_combobox
        attributesbox = self.dlg.attribute_combobox


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        if not result:
            return # ok was not pressed


        try:
            selected_layer = layercombobox.itemData(layercombobox.currentIndex()).layer()
            selected_attribute = attributesbox.itemData(attributesbox.currentIndex())

            if selected_layer is None:
                # TODO error message here
                raise NoLayerSelected

            can_edit = selected_layer.startEditing()
            if not can_edit:
                raise ROLayer

            # Get a QgsField to edit
            if self.new_attribute:
                new_attr_name = self.dlg.lineEdit.text()

                #self.iface.messageBar().pushMessage(new_attr_name) #TODO delete
                QgsMessageLog.logMessage("New Attribute", 'color_attribute', level=Qgis.Info)
                selected_attribute = self.check_and_create_attribute(selected_layer, new_attr_name)

                if not selected_attribute:
                    # TODO raise exception here too?
                    self.iface.messageBar().pushMessage("Could not create new attribute on : ",
                                                        selected_layer.name(),
                                                        level=Qgis.Critical)
            else:
                # TODO pending test
                selected_attribute = attributesbox.itemData(attributesbox.currentIndex())

            if selected_attribute.type() != QVariant.String:
                raise InvalidAttributeType

            #attribute = self.layer.dataProvider().fields().indexFromName(selected_attribute.name())

            self.start_progress_bar(selected_layer.featureCount(), "Color To Attribute")

            try:
                self.fill_color_attribute(selected_layer, selected_attribute)
            finally:
                self.iface.messageBar().clearWidgets()  # Do not let the bar stay there

            success = selected_layer.commitChanges()
            if not success:
                raise CommitFailed

        except ColorAttributeException as exc:
            selected_layer.rollBack() # Cancel any changes made

            self.iface.messageBar().pushMessage(exc.msg, exc.level)

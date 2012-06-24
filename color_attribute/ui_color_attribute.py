# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_color_attribute.ui'
#
# Created: Sun Jun 24 18:59:13 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_color_attribute(object):
    def setupUi(self, color_attribute):
        color_attribute.setObjectName(_fromUtf8("color_attribute"))
        color_attribute.resize(533, 150)
        self.formLayout = QtGui.QFormLayout(color_attribute)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(color_attribute)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.layerBox = QtGui.QComboBox(color_attribute)
        self.layerBox.setObjectName(_fromUtf8("layerBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.layerBox)
        self.label_2 = QtGui.QLabel(color_attribute)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.colorBox = QtGui.QComboBox(color_attribute)
        self.colorBox.setObjectName(_fromUtf8("colorBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.colorBox)
        self.attrNewName = QtGui.QLineEdit(color_attribute)
        self.attrNewName.setEnabled(False)
        self.attrNewName.setObjectName(_fromUtf8("attrNewName"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.attrNewName)
        self.label_3 = QtGui.QLabel(color_attribute)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.buttonBox = QtGui.QDialogButtonBox(color_attribute)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(color_attribute)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), color_attribute.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), color_attribute.reject)
        QtCore.QObject.connect(self.colorBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), color_attribute.activate_deactivate_newname)
        QtCore.QMetaObject.connectSlotsByName(color_attribute)

    def retranslateUi(self, color_attribute):
        color_attribute.setWindowTitle(QtGui.QApplication.translate("color_attribute", "color_attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("color_attribute", "Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("color_attribute", "Color attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("color_attribute", "Attribute name", None, QtGui.QApplication.UnicodeUTF8))


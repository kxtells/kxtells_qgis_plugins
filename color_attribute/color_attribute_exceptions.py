from qgis.gui import QgsMessageBar

class ColorAttributeException(Exception):
    title = None
    level = QgsMessageBar.CRITICAL
    msg   = None
    
class InvalidAttributeName(ColorAttributeException):
    title = "Invalid"
    level = QgsMessageBar.CRITICAL
    msg = "The attribute name contains invalid characters"

class EmptyAttributeName(ColorAttributeException):
    title = "Empty"
    level = QgsMessageBar.CRITICAL
    msg = "The attribute name is empty"

class InternalPluginError(ColorAttributeException):
    title = "ColorAttribute Error"
    level = QgsMessageBar.CRITICAL
    msg = "Something bad happened"

class AttributeAlreadyExists(ColorAttributeException):
    title = "Empty"
    level = QgsMessageBar.WARNING
    msg = "The specified name is already an attribute. It is overwritten"

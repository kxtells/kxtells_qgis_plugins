from qgis.gui import QgsMessageBar

class ColorAttributeException(Exception):
    title = None
    level = QgsMessageBar.CRITICAL
    msg   = None
    
class InvalidAttributeName(ColorAttributeException):
    title = "Invalid"
    level = QgsMessageBar.CRITICAL
    msg = "The attribute name contains invalid characters"

class InvalidAttributeType(ColorAttributeException):
    title = "Invalid Type"
    level = QgsMessageBar.CRITICAL
    msg = "The attribute is not of type String"

class EmptyAttributeName(ColorAttributeException):
    title = "Empty"
    level = QgsMessageBar.CRITICAL
    msg = "The attribute name is empty"

class InternalPluginError(ColorAttributeException):
    title = "ColorAttribute Error"
    level = QgsMessageBar.CRITICAL
    msg = "Something bad happened"

class InvalidCustomRenderer(ColorAttributeException):
    title = "Error"
    level = QgsMessageBar.WARNING
    msg = "Can't obtain the color from a custom renderer"

class AttributeAlreadyExists(ColorAttributeException):
    title = "Empty"
    level = QgsMessageBar.WARNING
    msg = "The specified name is already an attribute. It is overwritten"

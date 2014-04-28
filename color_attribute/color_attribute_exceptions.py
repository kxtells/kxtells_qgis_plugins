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

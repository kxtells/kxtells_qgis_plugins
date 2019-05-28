from qgis.gui import QgsMessageBar
from qgis.core import Qgis

class ColorAttributeException(Exception):
    title = None
    level = Qgis.Critical
    msg   = None

class InvalidAttributeName(ColorAttributeException):
    title = "Invalid"
    level = Qgis.Critical
    msg = "The attribute name contains invalid characters"

class InvalidAttributeType(ColorAttributeException):
    title = "Invalid Type"
    level = Qgis.Critical
    msg = "The attribute is not of type String"

class EmptyAttributeName(ColorAttributeException):
    title = "Empty"
    level = Qgis.Critical
    msg = "The attribute name is empty"

class InternalPluginError(ColorAttributeException):
    title = "ColorAttribute Error"
    level = Qgis.Critical
    msg = "Something bad happened"

class InvalidCustomRenderer(ColorAttributeException):
    title = "Error"
    level = Qgis.Warning
    msg = "Can't obtain the color from a custom renderer"

class AttributeAlreadyExists(ColorAttributeException):
    title = "Empty"
    level = Qgis.Warning
    msg = "The specified name is already an attribute. It is overwritten"

class ROLayer(ColorAttributeException):
    title = "RO Layer"
    level = Qgis.Critical
    msg = "Layer is Read Only and can't be edited"

class NoLayerSelected(ColorAttributeException):
    title = "No Layer Selected"
    level = Qgis.Info
    msg = "No Layer was selected to process"

class CommitFailed(ColorAttributeException):
    title = "Saving Changes Failed"
    level = Qgis.Critical
    msg = "Saving Changes to the layer failed"

class UnimplementedRenderer(ColorAttributeException):
    title = "Unimplemented Renderer"
    level = Qgis.Warning
    msg = "Renderer not implemented"

    def __init__(self, renderer_name):
        self.msg = "renderer {0} is not implemented".format(renderer_name)



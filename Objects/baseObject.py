"""
This is the base object class, it is supposed to have a variety of objects extend from this
This class will have the base objects functions and properties
There will be no need to create an instance of this
Created by Sam Parker
"""
class BaseObject:

    clipThrough = False
    xSize = 0
    ySize = 0
    angle = 0
    width = 0
    height = 0

    shape = "rectangle"

    name = ""

    coordinates = []

    colour = []

    def __init__(self, coordinates, name):
        self.coordinates = coordinates

    def getCoordinates(self):
        return self.coordinates

    def getClipThrough(self):
        return self.clipThrough

    def get_name(self):
        """Gets the objects unique name/id"""
        return self.name

    def get_colour(self):
        """Functions returns the objects colour"""
        return self.colour

    def get_coordinates(self):
        """Returns the objects coordinates"""
        return self.coordinates

    def get_angle(self):
        """Returns the objects angle"""
        return self.angle

    def get_width(self):
        """Returns the objects size"""
        return self.width

    def get_height(self):
        """Returns the objects height"""
        return self.height

    def get_shape(self):
        """Returns the shape of the object to draw"""
        return self.shape

    def action(self):
        """
        object does its action
        for a bar this could be serve or something
        """
        return True

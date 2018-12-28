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
    coordinates = []

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def getCoordinates(self):
        return self.coordinates

    def getClipThrough(self):
        return self.clipThrough
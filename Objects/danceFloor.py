"""Class Dance Floor
Created by Sam Parker
"""

from Objects.baseObject import BaseObject

class DanceFloor(BaseObject):

    def __init__(self, coordinates, xSize, ySize):
        self.coordinates = coordinates
        self.xSize = xSize
        self.ySize = ySize

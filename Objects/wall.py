
from Objects.baseObject import BaseObject

class Wall(BaseObject):

    colour = (0, 0, 0)

    def __init__(self, coordinates, xSize, ySize):
        self.coordinates = coordinates
        self.xSize = xSize
        self.ySize = ySize

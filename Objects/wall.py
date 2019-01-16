
from Objects.baseObject import BaseObject


class Wall(BaseObject):

    colour = (0, 0, 0)

    def __init__(self, coordinates, xSize, ySize):
        self.coordinates = coordinates
        # self.xSize = xSize
        # self.ySize = ySize
        self.width = xSize
        self.height = ySize

    # def get_xSize(self):
    #     return self.xSize

    def get_coordinates(self):
        return self.coordinates

    # def get_ySize(self):
    #     return self.ySize

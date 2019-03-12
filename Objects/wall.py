
from Objects.baseObject import BaseObject


class Wall(BaseObject):

    colour = [0, 0, 0]


    def __init__(self, coordinates, width, height):
        self.coordinates = coordinates
        self.width = width
        self.height = height
        self.clipThrough = False


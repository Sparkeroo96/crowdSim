"""Class Dance Floor
Created by Sam Parker
"""
import random

from Objects.baseObject import BaseObject

class DanceFloor(BaseObject):



    def __init__(self, coordinates, name, width, height):
        self.coordinates = coordinates
        self.width = width
        self.height = height

        # Should the bar have a fixed width? And you make multiple instances of it
        # Nope and yes

        self.name = name
        self.colour = (0, 255, 0)
        self.get_dancefloor_area()
        self.clipThrough = True

    def get_dancefloor_area(self):
        """
        Gets the area cords for the dancefloor
        :return: 
        """
        cords = []

        x1 = self.coordinates[0]
        y1 = self.coordinates[1]
        x2 = self.coordinates[0] + self.width
        y2 = self.coordinates[1] + self.height
        if self.width <= 0:
            x1, x2 = x2, x1
        if self.height <= 0:
            y1, y2 = y2, y1

        for x in range(x1, x2):
            for y in range(y1, y2):
                if x % 20 == 0 and y % 20 == 0:
                    cords.append([x, y])
        return cords

    def get_random_dance_area(self):
        open_space = self.get_dancefloor_area()
        random_node = random.randint(0, (len(self.get_dancefloor_area()) - 1))
        return open_space[random_node]


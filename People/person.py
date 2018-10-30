# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018
from random import randint


class Person:
    coordinates = []
    # map is None
    map = 0

    def __init__(self):
        print("Creating Person")

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]

    def action(self):
        """What the person is going to do"""
        return self.move()

    def move(self):
        """Person moving randomly around the course"""

        randomNumber = randint(0, 11)
        # print("Person should move " + str(randomNumber))
        if randomNumber <= 2: #person move up
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]

        elif randomNumber <= 4: #Person move down
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]

        elif randomNumber <= 6: #person move right
            newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]

        elif randomNumber <= 8: #Person move left
            newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]

        elif randomNumber <= 10:
            print("Person stay")

        # if newCoordinates is not None:
        if isinstance(newCoordinates, list):
            if self.map.check_coordinates(newCoordinates) == True:
                self.map.add_to_map(newCoordinates)
                self.map.remove_from_map(self.coordinates)
                self.coordinates = newCoordinates

        print("person at coordinates " + self.coordinates[0] + "," + self.coordinates[1])
        return self.coordinates;

    def store_coordinates(self, coordinates):
        """Storing a set of coordinates"""
        self.coordinates = coordinates

    def get_coordinates(self):
        """Getting stored coordinates"""
        return self.coordinates

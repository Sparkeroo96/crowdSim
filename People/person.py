# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018

class Person:
    coordinates = [];

    def __init__(self):
        print("Creating Person")

    def startingLoc(self):
        return [2,3]

    def action(self):
        self.move()

    def move(self):
        print("Person should move")

    def store_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates
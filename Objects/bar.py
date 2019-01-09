"""
The bar object
Created by Sam Parker
"""
from Objects.baseObject import BaseObject


class Bar(BaseObject):

    freeBarStaff = [];
    #Colour is Blue
    colour = [0, 0, 153]

    def __init__(self, coordinates, name,  width, height):
        self.coordinates = coordinates
        self.width = width
        self.height = height

        #Should the bar have a fixed width? And you make multiple instances of it


        self.name = name

    def barStaffWait(self, barStaff):
        """
        Bar Staff will have to serve people
        Not sure how yet
        """
        self.freeBarStaff.append(barStaff)

    def orderDrink(self):
        """
        Functiopn will return true if someone has a drink
        :return: true if getting a drink
        """
        #Do stuff here to actually determine it
        return True

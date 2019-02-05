"""
The bar object
Created by Sam Parker
"""
from Objects.baseObject import BaseObject


class Bar(BaseObject):

    freeBarStaff = [];
    #Colour is Blue
    colour = (0, 0, 153)

    drinksQueue = []

    def __init__(self, coordinates, name,  width, height):
        self.coordinates = coordinates
        self.width = width
        self.height = height

        #Should the bar have a fixed width? And you make multiple instances of it
        # Nope and yes


        self.name = name

    def action(self):
        """
        Functions serves drinks if there is bar staff and customers
        Just having it serve one at a time now
        :return:
        """
        self.serve_drink()

    def barStaffWait(self, barStaff):
        """
        Bar Staff will have to serve people
        Not sure how yet
        """
        self.freeBarStaff.append(barStaff)

    def orderDrink(self, customer):
        """
        Functiopn will return true if someone has a drink
        :return: true if getting a drink
        """
        #Do stuff here to actually determine it

        self.drinksQueue.append(customer)

        return True

    def serve_drink(self):
        """
        Serves a drink to the first customer in the orders list
        :return: 1 on serving, 0 if no one waiting and -1 if no servers
        """

        if self.drinksQueue:
            customer = self.drinksQueue.pop(0)

            customer.served_drink()
            return 1

        elif not self.drinksQueue:
            return 0

        return -1

"""
The bar object
Created by Sam Parker
"""
from Objects.baseObject import BaseObject


class Bar(BaseObject):

    maxStaffSize = 0
    staffWorking = []
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

        if width > height:
            self.auto_set_max_staff_size(width)
        else:
            self.auto_set_max_staff_size(height)

    def action(self):
        """
        Functions serves drinks if there is bar staff and customers
        Just having it serve one at a time now
        :return:
        """
        self.serve_drink()

    def staff_start_working_here(self, barStaff):
        """
        Staff member adds themselves to the
        """
        if self.check_free_staff_space() is not False:
            self.staffWorking.append(barStaff)
            return True

        return False

    def get_staff_working(self):
        """
        Returns the saff working
        :return: The array
        """
        return self.staffWorking

    def check_free_staff_space(self):
        """
        Checks to see if there is free space in the bar to work
        :return: An int of the free space
        """

        staffSize = len(self.staffWorking)
        remainingSpace = self.maxStaffSize - staffSize

        if remainingSpace > 0:
            return remainingSpace

        return False

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

    def auto_set_max_staff_size(self, barLength):
        """Automatically set the max staff size of a bar based on its size, average diameter of a person is 10 pixels
        going to use 20 as a divider as they're gonna want space to move
        :param barLength: The greatest size of the bar, either width or height
        :return: int of auto generated workers minimum 1
        """

        staffNumber = int(barLength / 20)

        if staffNumber == 0:
            staffNumber = 1

        self.maxStaffSize = staffNumber
        return staffNumber

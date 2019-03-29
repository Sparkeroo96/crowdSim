"""
The bar object
Created by Sam Parker
"""
from Objects.baseObject import BaseObject


class Bar(BaseObject):

    #Colour is Blue
    colour = (0, 0, 153)




    def __init__(self, coordinates, name,  width, height):
        self.coordinates = coordinates
        self.width = width
        self.height = height
        self.clipThrough = False
        #Should the bar have a fixed width? And you make multiple instances of it
        # Nope and yes

        self.name = name
        self.maxStaffSize = 0
        self.staffWorking = []
        self.drinksQueue = []
        # This allows you to control the number of virtual servers
        self.wait_timers = []

        staffSize = 0
        if width > height:
            staffSize = self.auto_set_max_staff_size(width)
        else:
            staffSize = self.auto_set_max_staff_size(height)

        self.initiate_wait_timers(staffSize)

    def action(self):
        """
        Functions serves drinks if there is bar staff and customers
        Just having it serve one at a time now
        :return:
        """
        self.decrease_wait_timers()

        self.serve_drink()


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
        freeWaitTimers = self.count_free_wait_timers()

        usedWaitTimers = 0

        if self.drinksQueue:

            x = 0
            for x in range(freeWaitTimers):
                if not self.drinksQueue:
                    break

                customer = self.drinksQueue.pop(0)
                # To show how long the server has to wait for
                waitTime = customer.served_drink()
                self.set_wait_timer(waitTime)
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

    def initiate_wait_timers(self, staffSize):
        """
        Sets the number of people who can be served at once
        :param staffSize: The number of virtual servers
        :return:
        """

        x = 0

        for x in range(staffSize):
            self.wait_timers.append(0)

    def decrease_wait_timers(self):
        """
        Decreases every active wait timer by 1
        To link the person being served a drink wait time with the serving
        :return:
        """

        x = 0

        while x < len(self.wait_timers):
            if self.wait_timers[x] > 0:
                self.wait_timers[x] -= 1

            x += 1


    def count_free_wait_timers(self):
        """
        COunts the number of wait timers at 0
        :return: Number of free wait timers
        """

        freeWaitTimers = 0
        x = 0

        while x < len(self.wait_timers):
            if int(self.wait_timers[x]) == 0:
                freeWaitTimers += 1

            x += 1

        return  freeWaitTimers

    def set_wait_timer(self, waitTime):
        """
        Sets a wait timer
        :param waitTime: The ticks to set it to
        :return: True on success
        """

        x = 0
        while x < len(self.wait_timers):
            if int(self.wait_timers[x]) == 0:
                self.wait_timers[x] = waitTime
                return True
            x += 1

        return False

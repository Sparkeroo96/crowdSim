"""
Toilet Class
Created by Sam Parker
"""

from Objects.baseObject import BaseObject


class Toilet(BaseObject):

    # This colour is orange
    colour = (255, 128, 0)

    #Flag to say if toilet is free
    personUsing = []

    def __init__(self, coordinates, name, width, height):
        self.coordinates = coordinates
        self.name = name
        self.width = width
        self.height = height
        self.userNumber = 1

        self.clipThrough = False

        if abs(width) > abs(height):
            self.auto_set_max_users_size(width)
        else:
            self.auto_set_max_users_size(height)

        print("creating object " + name)

    def person_use_toilet(self, person):
        """
        Sets inUse to True if it is free
        :return: returns True on success
        """

        # if self.personUsing is False or self.personUsing == []:
        if len(self.personUsing) < self.userNumber:
            # self.personUsing = person
            self.personUsing.append(person)
            return True

        else:
            return False

    def person_stop_using_toilet(self, person):
        """
        Sets inUse to False
        :return: True on successful stop using
        """

        if person in self.personUsing:
            # self.personUsing = False
            self.personUsing.remove(person)
            return True

        return False

    def check_person_using_toilet(self, person):
        """Checks to see if a person is using the toilet"""
        if person in self.personUsing:
            return True

        return False

    def get_person_using_toilet(self):
        """Returns personUsing"""
        return self.personUsing

    def auto_set_max_users_size(self, toiletLength):
        """Automatically set the max staff size of a bar based on its size, average diameter of a person is 10 pixels
        going to use 20 as a divider as they're gonna want space to move
        :param barLength: The greatest size of the bar, either width or height
        :return: int of auto generated workers minimum 1
        """

        userNumber = int(abs(toiletLength) / 20)

        if userNumber == 0:
            userNumber = 1

        self.userNumber = userNumber
        return userNumber

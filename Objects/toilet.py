"""
Toilet Class
Created by Sam Parker
"""

from Objects.baseObject import BaseObject


class Toilet(BaseObject):

    # This colour is dark grey
    colour = (255, 128, 0)

    #Flag to say if toilet is free
    personUsing = False

    def person_use_toilet(self, person):
        """
        Sets inUse to True if it is free
        :return: returns True on success
        """

        if self.personUsing is False:
            self.personUsing = person
            return True

        else:
            return False

    def person_stop_using_toilet(self, person):
        """
        Sets inUse to False
        :return: True on successful stop using
        """

        if person == self.personUsing:
            self.personUsing = False
            return True

        return False

    def get_person_using_toilet(self):
        """Returns personUsing"""
        return self.personUsing

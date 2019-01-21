"""
Toilet Class
Created by Sam Parker
"""

from Objects.baseObject import BaseObject


class Toilet(BaseObject):

    # This colour is dark grey
    colour = (255, 128, 0)

    def useToilet(self):
        return True

"""
Toilet Class
Created by Sam Parker
"""

from Objects.baseObject import BaseObject

class Toilet(BaseObject):

    # This colour is dark grey
    colour = [169, 169, 169]

    def useToilet(self):
        return True

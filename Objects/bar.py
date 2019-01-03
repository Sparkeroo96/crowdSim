from Objects.base_object import BaseObject

"""May look to initialise the bar object details in init after. """


class Bar(BaseObject):

    def __init__(self):
        self.set_id('id: 3')
        self.set_env_object_name('Drinks Bar')
        self.set_coordX(400)
        self.set_coordY(100)
        self.set_angle(60)
        self.set_width(20)

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

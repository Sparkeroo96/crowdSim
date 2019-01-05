from Environment.env_object import EnvObject

"""May look to initialise the bar object details in init after. """


class BarObject(EnvObject):

    def __init__(self):
        self.set_id('id: 3')
        self.set_env_object_name('Drinks Bar')
        self.set_coordX(400)
        self.set_coordY(100)
        self.set_angle(60)
        self.set_width(20)





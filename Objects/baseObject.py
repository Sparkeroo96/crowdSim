"""
This is the base object class, it is supposed to have a variety of objects extend from this
This class will have the base objects functions and properties
There will be no need to create an instance of this
Created by Sam Parker
"""
class BaseObject:


    angle = 0
    width = 0
    height = 0

    shape = "rectangle"

    name = ""

    colour = ()

    rejectionStrength = 1

    coordinates = []
    envObjectName = ""
    id = ""
    coordX = 0
    coordY = 0
    angle = 0
    width = 0



    def __init__(self, coordinates, name, width, height):
        self.coordinates = coordinates
        self.name = name
        self.width = width
        self.height = height

        self.clipThrough = False

        print("creating object " + name)

    def get_details(self):
        return ([self.envObjectName, self.id, self.coordX, self.coordY, self.angle, self.width])

    def get_clip_through(self):
        return self.clipThrough

    """Returns what object it is"""
    def get_env_object_name(self):
        return self.envObjectName

    def get_id(self):
        return self.id

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle

    def set_width(self, width):
        self.width = width

    def get_name(self):
        """Gets the objects unique name/id"""
        return self.name

    def get_colour(self):
        """Functions returns the objects colour"""
        return self.colour

    def get_coordinates(self):
        """Returns the objects coordinates"""
        return self.coordinates

    def get_width(self):
        """Returns the objects size"""
        return self.width

    def get_height(self):
        """Returns the objects height"""
        return self.height

    def get_shape(self):
        """Returns the shape of the object to draw"""
        return self.shape

    def action(self):
        """
        object does its action
        for a bar this could be serve or something
        """
        return True

    def set_shape(self, shape):
        shape = self.shape

    def get_rejection_strength(self):
        """Reutrns the rejectionStrength"""
        return self.rejectionStrength


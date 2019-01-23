"""
This is the base object class, it is supposed to have a variety of objects extend from this
This class will have the base objects functions and properties
There will be no need to create an instance of this
Created by Sam Parker
"""
class BaseObject:

    envObjectName = ""
    id = ""
    coordX = 0
    coordY = 0
    angle = 0
    width = 0
    shape = "rectangle"
    colour = (0, 255, 0)
    height = 20

    def __init__(self, id, name, coords, angle, width, shape):
        self.id = id
        self.envObjectName = name
        if coords:
            self.coordX = coords[0]
            self.coordY = coords[1]
        self.angle = angle
        self.width = width
        self.shape = shape


    def get_details(self):
        return ([self.envObjectName, self.id, self.coordX, self.coordY, self.angle, self.width])
    """Cords"""
    def get_coordinates(self):
        cords = [self.coordX, self.coordY]
        return cords

    """Returns what object it is"""
    def get_env_object_name(self):
        return self.envObjectName

    def action(self):
        return ("")

    def get_colour(self):
        return self.colour

    def get_shape(self):
        return self.shape

    def set_shape(self, shape):
        shape = self.shape

    def get_id(self):
        return self.id

    def get_angle(self):
        return self.angle

    def get_width(self):
        return self.width

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    def set_env_object_name(self, name):
        self.envObjectName = name

    def set_id(self, newID):
        self.id = newID

    def set_coordX(self, coordX):
        self.coordX = coordX

    def set_coordY(self, coordY):
        self.coordY = coordY

    def set_angle(self, angle):
        self.angle = angle

    def set_width(self, width):
        self.width = width

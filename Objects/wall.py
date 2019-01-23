
from Objects.baseObject import BaseObject

class Wall(BaseObject):

    colour = [0, 0, 0]
    shape = "wall"

    def __init__(self, id, name, coords, angle, width, shape):
        self.set_id(id)
        self.set_env_object_name(name)
        self.set_coordX(coords[0])
        self.set_coordY(coords[1])
        self.set_angle(angle)
        self.set_width(width)
        self.set_shape(shape)



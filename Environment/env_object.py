class EnvObject:

    envObjectName = ""
    id = ""
    coordX = 0
    coordY = 0
    angle = 0
    width = 0

    def get_details(self):
        return ([self.envObjectName, self.id, self.coordX, self.coordY, self.angle, self.width])
    """Cords"""
    def get_cords(self):
        cords = [self.coordX, self.coordY]
        return cords

    """Returns what object it is"""
    def get_env_object_name(self):
        return self.envObjectName

    def get_id(self):
        return self.id

    def get_angle(self):
        return self.angle

    def get_width(self):
        return self.width

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







    # def add_map(self, newMap, newCoordinates):
    #     """Storing the generated map"""
    #     self.map = newMap
    #     self.coordinates = newCoordinates
    #     # print(self.coordinates)

    # def store_coordinates(self, coordinates):
    #     """Storing a set of coordinates the object is positioned in"""
    #     self.coordinates = coordinates
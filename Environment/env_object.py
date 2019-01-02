class EnvObject:
    coordinates = [6, 4]
    map = 2
    envObjectName = "Base Object"

    def __init__(self):
        print("Creating Object")

    def set_cords(self):
        return self.coordinates

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates
        # print(self.coordinates)

    def store_coordinates(self, coordinates):
            """Storing a set of coordinates the object is positioned in"""
            self.coordinates = coordinates

    def env_object_name(self):
        """Returns what object it is"""
        return self.envObjectName

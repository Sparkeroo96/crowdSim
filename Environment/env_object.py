class EnvObject:
    coordinates = []
    map = 2
    envObjectName = ""

    def __init__(self):
        print("Creating Object")

    def get_cords(self):
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

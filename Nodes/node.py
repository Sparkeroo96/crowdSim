class Node:
    idCoordinates = []
    actualCoordinates = []
    """Value determines if the node is empty, occupied or has an object"""
    value = ""

    def __init__(self, idCoords, value):
        self.idCoordinates = idCoords
        self.value = value

    def get_actual_coords(self):
        return self.actualCoordinates

    def set_actual_coords(self, cords):
            self.actualCoordinates = cords

    def get_idCoords(self):
        return self.idCoordinates

    def set_idCoords(self, cords):
            self.idCoordinates = cords

    """Value determines if the node is empty, occupied or has an object"""
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

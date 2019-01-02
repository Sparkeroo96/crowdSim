from Environment.env_object import EnvObject
from Environment.bar_object import BarObject

class EnvironmentLocations:
    """all locations of objects"""
    locations = []

    def set_locations(self):
        envObject = EnvObject()
        barObject = BarObject()
        self.locations.append(envObject)
        self.locations.append(barObject)


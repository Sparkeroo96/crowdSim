from Environment.toilet_object import ToiletObject
from Environment.bar_object import BarObject

class EnvironmentLocations:
    """all objects"""
    environment = []
    """ all locations of the env objects"""
    locations = []
    toiletObject = ToiletObject()
    barObject = BarObject()

    def __init__(self):
        """add the env locations into the locations array"""
        self.env_locations()
        self.env_array()

    def get_array(self):
        return self.environment

    """appends the cordinates to the locations array"""
    def env_locations(self):
        self.locations.append(self.toiletObject.get_cords())
        self.locations.append(self.barObject.get_cords())

    """finds a specific location"""
    def location_array(self, x):
        return self.locations[x]

    """appends the env objects to the environment array"""
    def env_array(self):
        self.environment.append(self.toiletObject)
        self.environment.append(self.barObject)

    """finds a specific env object """
    def environment_array(self, x):
        return self.environment[x]





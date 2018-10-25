#Main Map class that should handle the init and management of the map
# Created by Sam Parker 23/10/2018

class MapMain:

    map = [];

    def __init__(self):
        """Initiates the Map class"""
        print("Created Map")

    def sizeHeight(self):
        return 1000

    def sizeWidth(self):
        return 1000

    def mapExample(self):
        array = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]
        return array

    def map_generate(self,xLength, yLength):
        """Generates a map on given x and y lengths"""
        x = 0
        while x < xLength:
            arrayTemp = []
            y = 0

            while y < yLength:
                arrayTemp.append(1)

            self.map.append(arrayTemp)
            x += 1

    def get_map(self):
        """Returns the map"""
        return self.map

    def get_map_length(self):
        """Gets the length of the map"""
        return len(self.map)

    def get_map_height(self):
        """Works out the greatest height of the map"""
        mapHeight = 0

        for column in self.map:
            if len(column) > mapHeight:
                mapHeight = len(column)

        return mapHeight

    def check_coordinates(self, arrayCoordinates):
        """Returns what exists at arrays coordinates"""
        return self.map[arrayCoordinates[0]][arrayCoordinates[1]]

    def add_to_map(self, object, arrayCoordinates):
        """Adds an element to the map at the given coordinates"""
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = object

    def remove_from_map(self, arrayCoordinates):
        """Removes an element from the map by the given coordinates"""
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = 1

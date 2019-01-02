#Main Map class that should handle the init and management of the map
# Created by Sam Parker 23/10/2018

mapArray = [[1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]]
class MapMain:

    map = [];
    def __init__(self):
        """Initiates the Map class"""
        print("Created Map")

    def sizeHeight(self):
        return 1000

    def sizeWidth(self):
        return 1000

    def set_map(self):
        array = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]
        mapArray = array

    def get_map(self):
        return mapArray

# Does the maths to see how big the canvas has to be and how many grids to make
    def grid_size(self,mapArray):
        num_rows = 0
        num_cols = 0
        working_rows = 0
        for i in range(len(mapArray)):
            num_cols = num_cols + 1
            working_rows = 0
            for j in range(len(mapArray[i])):
                working_rows = working_rows + 1
                if working_rows > num_rows:
                    num_rows = working_rows
                    
        return [num_rows, num_cols]

    def map_generate(self, xLength, yLength):
        """Generates a map on given x and y lengths"""
        x = 0
        while x < xLength:
            arrayTemp = []
            y = 0

            while y < yLength:
                arrayTemp.append(0)
                y += 1

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
        if arrayCoordinates[0] < 0 or arrayCoordinates[0] >= self.get_map_length():
            print("x out of array")
            return False
        if arrayCoordinates[1] < 0 or arrayCoordinates[1] >= self.get_map_height():
            print("y out of array")
            return False



        if self.map[arrayCoordinates[0]][arrayCoordinates[1]] == 0:
            return True
        return False
        # return self.map[arrayCoordinates[0], arrayCoordinates[1]]

    def add_to_map(self, object, arrayCoordinates):
        """Adds an element to the map at the given coordinates"""
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = 1

    """Adds the environment objects into the grid"""
    def add_env_objects_to_map(self, object, arrayCoordinates):
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = 2

    def remove_from_map(self, arrayCoordinates):
        """Removes an element from the map by the given coordinates"""
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = 0

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

    def get_min_max_x(self,x, radius):
        """Gets the min max coordinates for x in a given value, returns in an array 0 being lowest 1 being highest"""
        arrayX = []
        arrayX[0] = x - radius
        if arrayX[0] < 0:
            arrayX[0] = 0

        arrayX[1] = x + radius
        if arrayX[1] > self.get_map_length():
            arrayX[1]= self.get_map_length()

        return arrayX

    def get_min_max_y(self, y, radius):
        """Gets min max coordinates for y value, returns an array 0 being lowest 1 being highest"""
        arrayY = []
        arrayY[0] = y - radius
        if arrayY[0] < 0:
            arrayY[0] = 0

        arrayY[1] = y + radius
        if arrayY[1] > self.get_map_height():
            arrayY[1] = self.get_map_height()

        return arrayY

    def check_coordinates(self, arrayCoordinates):
        """Returns whether something exists at arrays coordinates"""
        if arrayCoordinates[0] < 0 or arrayCoordinates[0] >= self.get_map_length():
            print("x out of array")
            return False

        if arrayCoordinates[1] < 0 or arrayCoordinates[1] >= self.get_map_height():
            print("y out of array")
            return False

        if self.map[arrayCoordinates[0]][arrayCoordinates[1]] == 0:
            return True
        return False

    def return_object_at_coordinates(self, arrayCoordinates):
        """Returns whats at coordinates"""
        if arrayCoordinates[0] < 0 or arrayCoordinates[0] >= self.get_map_length():
            print("x out of array")
            return False

        if arrayCoordinates[1] < 0 or arrayCoordinates[1] >= self.get_map_height():
            print("y out of array")
            return False

        return self.map[arrayCoordinates[0]][arrayCoordinates[1]]

    def get_objects_in_range(self, objectInstance, arrayCoordinates, radius):
        """gets objects of a given type in a certain range, if object = None retrieves everything"""
        arrayObjects = []
        xCoordinates = self.get_min_max_x(arrayCoordinates[0])
        yCoordinates = self.get_min_max_y(arrayCoordinates[1])

        x = xCoordinates[0]

        while x <= xCoordinates[1]:
            y = yCoordinates[0]

            while y <= yCoordinates[1]:
                if x == arrayCoordinates[0] and y == arrayCoordinates[1]:
                    continue

                checkCoords = [x, y]
                obj = self.return_object_at_coordinates(checkCoords)

                if obj == 0 or obj == False:
                    continue

                arrayTemp = []
                arrayTemp['object'] = obj
                arrayTemp['coordinates'] = checkCoords

                if objectInstance == None or isinstance(obj, objectInstance):
                    arrayObjects.append(arrayTemp)

                y += 1

            x += 1

        return arrayObjects


    def add_to_map(self, object, arrayCoordinates):
        """Adds an element to the map at the given coordinates"""
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = object

    def remove_from_map(self, arrayCoordinates):
        """Removes an element from the map by the given coordinates"""
        self.map[arrayCoordinates[0]][arrayCoordinates[1]] = 0

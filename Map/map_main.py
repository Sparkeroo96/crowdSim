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
    def __init__(self):
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

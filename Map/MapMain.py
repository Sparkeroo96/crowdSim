#Main Map class that should handle the init and management of the map
# Created by Sam Parker 23/10/2018

class MapMain:

    def __init__(self):
        print "Created Map"

    def sizeHeight(self):
        return 1000

    def sizeWidth(self):
        return 1000

    def mapExample(self):
        array = [[0,1,0],
                 [0,0,1,2,5],
                 [1,0,0,5,3,2]]
        return array


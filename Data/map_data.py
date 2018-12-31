# Main Map class that should handle the init and management of the map
# Created by Chris Clark 11/12/2018
import random as rand

class map_data:
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]
    mapDefult = [['person','id:1',[100,500],90,10],['person','id:2',[200,300],180,10],['wall',[10,10],[100,10]]]

    def __init__(self):
        print("Map_data Object Created")

    def getMap(self):
        # Returns the map
        return self.mapDefult

    def addPerson(self,name,cordinateX,cordinateY,angle,width):
        array = self.mapDefult
        array.append('person',name,[cordinateX,cordinateY],angle,width)

    def moveRandomly(self):
        map = self.getMap()
        x = rand.randint(0,4)
        # Example of how to go UP!
        if x == 0:
            map[0][2][1] -= 1
        # Example of how to go DOWN!
        if x == 1:
            map[0][2][1] += 1
        # Example of going RIGHT!
        if x == 3:
            map[0][2][0] += 1
        # Example of going LEFT!
        if x == 4:
            map[0][2][0] -= 1
        # print(map[0][2][1])

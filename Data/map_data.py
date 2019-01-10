"""
Main Map class that should handle the init and management of the map
Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import random as rand
import math
from People import *
from Objects import *

class map_data:
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]
    # mapDefult = [['person','id:1',[150,350],30,10],['person','id:2',[200,300],30,10],['wall',[10,10],[100,10]]]

    mapData = []
    def __init__(self):
        print("Map_data Object Created")

    def map_default(self):
        """Getting default map data"""

        self.add_people_to_map(10)

        return self.mapData

    def add_people_to_map(self, peopleCount):
        """Adding people to map"""
        x = 0
        while x < peopleCount:
            coords = [50 * (x + 1), 50 * (x + 1)]

            newPerson = person.Person("person " + str(len(self.mapData)), coords, 20, rand.randint(0,360))

            newPerson.add_map(self, coords)
            self.mapData.append(newPerson)

            x += 1
    def add_wall_to_map(self, cords,width, height):
            newWall = wall.Wall(cords,width,height)
            self.mapData.append(newWall)

    def check_space_unoccupied(self, coordinates, object_size, object_name, object_shape):
        """Checks to see if a set of coordinates is occupied by an object or person
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the object that is the size of the object currently checking coords, if it has a width and height give it as a list
        :param object_name is the name of the object doing checking so it doesnt check itself
        """

        ranges = self.__get_coordinates_range(coordinates, object_size)

        for object in self.mapData:
            if object.get_name() == object_name:
                continue

            if isinstance(object, "Person"):
                print("In Person")

    def __get_coordinates_range(self, coordinates, object_size):
        """ Function gets the range of spaces used by a set of coordinates
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the object that is the size of the object currently checking coords, if it has a width and height give it as a list
        """
        xCoord = coordinates[0]
        yCoord = coordinates[1]
        if isinstance(object_size, list):
            # If there is a width and height give it as a list
            print("list")
            xSize = object_size[0]
            ySize = object_size[1]

        else:
            # For when you just give the width, most likely gonna be for a person
            print("int")
            xSize = object_size
            ySize = object_size

        # X Coordinate ranges
        if xCoord - xSize < 0:
            lowX = 0
        else:
            lowX = xCoord - xSize

        highX = xCoord + object_size

        # Y Coordinate ranges
        if yCoord - ySize < 0:
            lowY = 0
        else:
            lowY = yCoord - ySize

        highY = yCoord + object_size

        xRanges = [lowX, highX]
        yRanges = [lowY, highY]
        return [xRanges, yRanges]


    def whichPerson(self,cords):
        """This function checks to see if a cordiante is within another person and returns their id
        :Pram cords the cordinates of the person they are looking at
        :return the Id of the person they are looking at
        """
        map = self.mapData
        for people in map:
            if people.get_shape() == "circle":
                x = people.coordinates[0]
                y = people.coordinates[1]
                radias = people.width / 2
                x1 = cords[0]
                y1 = cords[1]
                # This is pythagorous and works out if the point is within the circle
                distance = math.pow(x1 - x,2) + math.pow(y1 - y,2)
                distanceRoot = math.sqrt(distance)
                if distanceRoot <= radias:
                    return people.name

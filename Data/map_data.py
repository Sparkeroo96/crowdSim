"""
Main Map class that should handle the init and management of the map
Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import random as rand
import math
from People import *
from Objects import *

# Seems to need these for allowing isinstance(example, Person), doesnt work with the above import
from People.person import Person
from People.flockingPerson import FlockingPerson

from Objects.bar import Bar

class map_data:
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]
    # mapDefult = [['person','id:1',[150,350],30,10],['person','id:2',[200,300],30,10],['wall',[10,10],[100,10]]]

    mapData = []
    gui = None

    def __init__(self, gui):
        print("Map_data Object Created")
        self.gui = gui

    def map_default(self):
        """Getting default map data"""

        self.add_people_to_map(10)
        self.add_bar_to_map(0)

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
        """Checks to see if a set of coordinates is occupied by an obj or person
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the obj that is the size of the obj currently checking coords, if it has a width and height give it as a list
        :param object_name is the name of the obj doing checking so it doesnt check itself
        """

        ranges = self._get_coordinates_range(coordinates, object_size)

        for obj in self.mapData:
            if obj.get_name() == object_name:
                continue

            if isinstance(obj, "Person"):
                print("In Person")

    def add_bar_to_map(self, barCount):
        """Adds a number of bars to the map"""
        x = 0
        while x < barCount:
            coords = [100 * (x + 1), 100 * (x + 1)]
            newBar = bar.Bar(coords, "bar " + str(len(self.mapData)), 100, 20)

            self.mapData.append(newBar)

            x += 1

    def _get_coordinates_range(self, coordinates, object_size):
        """ Function gets the range of spaces used by a set of coordinates
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the obj that is the size of the obj currently checking coords, if it has a width and height give it as a list
        """
        xCoord = coordinates[0]
        yCoord = coordinates[1]
        if isinstance(object_size, list):
            # If there is a width and height give it as a list
            xSize = object_size[0]
            ySize = object_size[1]

        else:
            # For when you just give the width, most likely gonna be for a person
            xSize = object_size
            ySize = object_size

        # X Coordinate ranges
        if xCoord - xSize < 0:
            lowX = 0
        else:
            lowX = xCoord - xSize

        highX = xCoord + xSize

        # Y Coordinate ranges
        if yCoord - ySize < 0:
            lowY = 0
        else:
            lowY = yCoord - ySize

        highY = yCoord + ySize

        xRanges = [lowX, highX]
        yRanges = [lowY, highY]
        returnValue = {
            "X" : xRanges,
            "Y" : yRanges
        }
        # return [xRanges, yRanges]
        return returnValue

    def get_object_colour_code(self, objectType):
        """
        Gets an obj colour code
        :param objectType: The obj type you are looking for
        :return: Returns an RGB array, false if no such obj type exists
        """

        for obj in self.mapData:
            print("objType: " + str(type(obj)))
            # if type(obj) == objectType:
            searchString = "." + objectType + "'"
            if searchString in str(type(obj)):
                return obj.get_colour()

        return False


    def whichPerson(self,cords):
        """This function checks to see if a cordiante is within another person and returns their id
        :Pram cords the cordinates of the person they are looking at
        :return the Id of the person they are looking at
        """
        map = self.get_map()
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
                    return people

    def export(self,file_name,save_name):
        """Function that outputs the map in a saveable format"""
        map = self.get_map()
        data = []
        file = open(file_name, 'r')
        line_num = 1
        num_lines = 1
        saved_data = []
        for line in file:
            num_lines = num_lines + 1
            saved_data.append(line)
        print(saved_data)
        file.close()
        file = open(file_name,'w+')
        for line in saved_data:
            file.write(line)
        file.write("#####" + "\n")
        file.write(save_name + "\n")
        for obj in map:
            if isinstance(obj,Person):
                obj_type = 'Person'
                coords = obj.get_coordinates()
                angle = obj.get_angle()
                width = obj.get_width()
                data = [obj_type,coords,width,angle]
            elif isinstance(obj, wall):
                obj_type = 'Wall'
                coords = obj.get_coordinates()
                width = obj.get_width()
                height = obj.get.height
                data = [obj_type,coords,width,height]
            str1 = '/'.join(str(e) for e in data)
            # print(str1)
            file.write(str1 + "\n")
        file.close()


    def import_from_file(self,file,save_name):
        file = open(file,'r')
        # print(file.read())
        print(save_name)
        x = 1
        for line in file:
            result = [x.strip() for x in line.split('/')]
            if result == "######":
                print("End of Document")
            elif result[0] == 'Person':
                coords = [x.strip() for x in result[1].split(",")]
                coordX = coords[0].translate({ord("'"): None})
                coordY = coords[1].translate({ord("'"): None})
                coordX = coordX.translate({ord("["): None})
                coordY = coordY.translate({ord("]"): None})
                coords = [int(coordX),int(coordY)]
                newPerson = person.Person("person " + str(len(self.mapData)), coords, int(result[2]), int(result[3]))
                self.mapData.append(newPerson)
            elif result[0] == 'Wall':
                newWall = wall.Wall(coords,int(result[1]),int(result[2]))
                self.mapData.append(newWall)

        file.close()

    def get_map(self):
        return self.mapData

    def clear_map(self):
        self.get_map() == []

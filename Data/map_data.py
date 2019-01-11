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
        self.gui = gui

    def map_default(self):
        """Getting default map data"""

        self.add_people_to_map(3)
        # self.add_bar_to_map(1)

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

    def add_bar_to_map(self, barCount):
        """Adds a number of bars to the map"""
        x = 0
        while x < barCount:
            coords = [150 * (x + 1), 150 * (x + 1)]
            newBar = bar.Bar(coords, "bar " + str(len(self.mapData)), 100, 20)

            self.mapData.append(newBar)

            x += 1

    def get_object_colour_code(self, objectType):
        """
        Gets an object colour code
        :param objectType: The object type you are looking for
        :return: Returns an RGB array, false if no such object type exists
        """

        for obj in self.mapData:
            print("objType: " + str(type(obj)))
            # if type(obj) == objectType:
            searchString = "." + objectType + "'"
            if searchString in str(type(obj)):
                return obj.get_colour()


        return False

    def person_look_for_object(self, coordinates, angle, vision, colourCode):
        """
        DEFUNCT
        Returns an array with references to given object
        :param coordinates: Persons coordinates given as [x, y]
        :param angle: Persons viewing angle
        :param vision: Persons vision range
        :return: Array of objects
        """

        visionCoordinates = self.personVision(coordinates[0], coordinates[1], angle, vision)

        coordinatesWithColour = self.gui.check_coordinates_for_colour(visionCoordinates, colourCode)

    def personVision(self, x1, y1, angle, vision):
        """This function gets an person and returns an array of the cordinates of their vision"""
        # # How far a person can see
        if vision is None:
            vision = 100

        # Number the vision starts from, this stops the person from seeing themselves
        x = 12
        # This is the amount of rays that they produce
        rays = 10
        # The itorating number of rays
        i = 0
        angle = angle - 25
        if angle <= 0:
            angle = angle + 360
        # saves the starting angle
        originalAngle = angle
        # results array for all the newCoordinates
        resultArray = []
        while i <= rays:
            # increases the angles by 5 each intoration
            angle = originalAngle + (i * 5)
            # this is an if statement that stops the number being more than 360 and less than 0
            if angle > 360:
                angle = angle - 360
            # this then produces the cordiantes for each line and adds them to the array
            while vision >= x:
                value = self.angleMath(angle,x1,y1,x)
                value = [x1 + value[0],y1 + value[1]]
                resultArray.append(value)
                x = x + 1
            i = i + 1
            x = 12
            # print(resultArray)
            # print( )
        return resultArray

    def angleMath(self, angle, xcord, ycord,vision):
        """This is the maths that returns the amount the x and y cordianes need to change to produce the cordinates
        of the new loaction """
        # These variables will be chnaged into number to change
        veritcal = 0
        horizontal = 0
        # The math.sin and cos works in radians so this converts the number to radians
        angle1 = math.radians(angle)
        #These 4 if statements do the maths that takes the lengh of their vision, and the angle that they are directionLooking
        # then returns the value that the point would have to change

        if 1 <= angle and angle <= 90:
            veritcal = math.floor(vision * math.sin(math.radians(90) - angle1))
            veritcal = veritcal * -1
            # print(veritcal)
            horizontal = math.floor(vision * math.cos(math.radians(90) - angle1))
            # print(horizontal)
        if 90 < angle and angle <= 180:
            # print("BR")
            veritcal = math.floor(vision * math.sin(angle1 - math.radians(90)))
            horizontal = math.floor(vision * math.cos(angle1 - math.radians(90)))
        if 180 < angle and angle <= 270:
            # print("BL")
            veritcal = math.floor(vision * math.sin(math.radians(270) - angle1))
            horizontal = math.floor(vision * math.cos(math.radians(270) - angle1))
            horizontal = horizontal *-1
        if 270 < angle and angle <=360:
            # print('TL')
            veritcal = math.floor(vision * math.cos(math.radians(360)- angle1))
            veritcal = veritcal * -1
            horizontal = math.floor(vision * math.sin(math.radians(360) - angle1))
            horizontal = horizontal * -1
        return [veritcal, horizontal]


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

    def add_bar_to_map(self, barCount):
        """Adds a number of bars to the map"""
        x = 0
        while x < barCount:
            coords = [100 * (x + 1), 100 * (x + 1)]
            newBar = bar.Bar(coords, "bar " + str(len(self.mapData)), 100, 20)

            self.mapData.append(newBar)

            x += 1

    def __get_coordinates_range(self, coordinates, object_size):
        """ Function gets the range of spaces used by a set of coordinates
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the object that is the size of the object currently checking coords, if it has a width and height give it as a list
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
        Gets an object colour code
        :param objectType: The object type you are looking for
        :return: Returns an RGB array, false if no such object type exists
        """

        for obj in self.mapData:
            print("objType: " + str(type(obj)))
            # if type(obj) == objectType:
            searchString = "." + objectType + "'"
            if searchString in str(type(obj)):
                return obj.get_colour()

        return False


    def what_object(self, coords):
        """This function checks to see if a cordiante is within another person and returns a reference to the object"""
        print("what obj")
        for obj in self.map_default():
            if obj.get_shape() == "circle":
                x = obj.coordinates[0]
                y = obj.coordinates[1]
                radias = obj.width / 2
                x1 = coords[0]
                y1 = coords[1]
                # This is pythagorous and works out if the point is within the circle
                distance = math.pow(x1 - x,2) + math.pow(y1 - y,2)
                distanceRoot = math.sqrt(distance)
                if distanceRoot <= radias:
                    return obj

            else:
                width = obj.get_width()
                height = obj.get_height()

                coordsRange = self.__get_coordinates_range(coords, [width, height])

                if self.point_in_coordinates_range(coords, coordsRange):
                    return obj

        # map = self.mapData
        # for people in map:
        #     if people.get_shape() == "circle":
        #         x = people.coordinates[0]
        #         y = people.coordinates[1]
        #         radias = people.width / 2
        #         x1 = cords[0]
        #         y1 = cords[1]
        #         # This is pythagorous and works out if the point is within the circle
        #         distance = math.pow(x1 - x,2) + math.pow(y1 - y,2)
        #         distanceRoot = math.sqrt(distance)
        #         if distanceRoot <= radias:
        #             return people

    def point_in_coordinates_range(self, coordinates, range):
        """
        Finds out if a given point exists within a range of other coordinates
        :param coordinates: The point to check
        :param range: the range to check given as {X: [lowX, highX], Y: [lowY, highY]}
        :return: True if it is contained within the ranges
        """

        x = coordinates[0]
        y = coordinates[1]

        if x >= range["X"][0] and x <= range["X"][1] and y >= range["Y"][0] and y <= range["Y"][1]:
            return True

        return False





    def person_eyes(self, cords, angle, radias):
        angle_left = angle - 25
        if angle_left <= 0:
            angle_left = angle_left + 360

        angle_right = angle + 25

        if angle_right > 360:
            angle_right = angle_right - 360

        # THis is the maths for the eyes
        left_eye = self.angleMath(angle_left,cords[0],cords[1],radias-3)
        right_eye = self.angleMath(angle_right,cords[0],cords[1],radias-3)
        left_eye = [cords[0] + left_eye[0], cords[1] + left_eye[1]]
        right_eye = [cords[0] + right_eye[0], cords[1] + right_eye[1]]

        return [left_eye,right_eye]

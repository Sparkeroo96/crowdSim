"""
Main Map class that should handle the init and management of the map
Created by Chris Clark cc604
"""
import random as rand
import math
from People import *
from Objects import *

class map_data:
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]
    mapDefult = [['person','id:1',[150,350],30,10],['person','id:2',[200,300],30,10],['wall',[10,10],[100,10]]]

    mapData = []

    def __init__(self):
        print("Map_data Object Created")

    def map_default(self):
        """Getting default map data"""

        self.add_people_to_map(1)

        return self.mapData

    def add_people_to_map(self, peopleCount):
        """Adding people to map"""
        x = 0
        while x < peopleCount:
            coords = [50 * (x + 1), 50 * (x + 1)]

            newPerson = person.Person("person " + str(len(self.mapData)), coords, None)

            newPerson.add_map(self, coords)
            self.mapData.append(newPerson)

            x += 1

    def personVision(self,id):
        """This function gets an person and returns an array of the cordinates of their vision"""
        # How far a person can see
        vision = 100
        # The angle of the vision
        angleOfVison = 30
        # check to see if the id it was passed exisits
        found = False
        #For loop that goes though the map array and finds the person that is doing the looking
        for person in self.mapDefult:
            if person[0] == 'person':
                if person[1] == id:
                    # Saves the data of the person who is looking
                    xCord = person[2][0]
                    yCord = person[2][1]
                    # Starting angle of the vision
                    angle1 = person[3] - (angleOfVison/2)
                    # If statements to stop the angle being highter than 360 and lower than 0
                    if angle1 <= 0:
                        angle1 = angle1 + 360
                    if angle1 > 360:
                        angle1 = angle1 - 360
                    found = True
                    break
        # If the Id wasn't found then it prints an error
        if found == False:
            print("Error finding %s" % id)
            return 0
        # Number the vision starts from, this stops the person from seeing themselves
        x = 12
        #This will hold the people that they see
        resultArray = []
        # This is the amount of rays that they produce
        rays = 10
        # The itorating number of rays
        i = 0
        # saves the starting angle
        originalAngle = angle1
        while i <= rays:
            # increases the angles by 5 each intoration
            angle1 = originalAngle + (i * 5)
            # this is an if statement that stops the number being more than 360 and less than 0
            if angle1 <= 0:
                angle1 = angle1 + 360
            if angle1 > 360:
                angle1 = angle1 - 360
            # this then produces the cordiantes for each line and adds them to the array
            while vision >= x:
                value = self.angleMath(angle1,xCord,yCord,x)
                value = [xCord + value[0],yCord + value[1]]
                resultArray.append(value)
                x = x + 1
            i = i + 1
            x = 12
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

    def check_coordinates_for_person(self, check_coords, radius, name, edgeCoordinates):
        """Check to see if a person can move into a space
        :param check_coords The new coordinates to check
        :param edge_coordinates The persons edge coordinates
        :param radius the persons width
        :param name the persons id, so it doesnt do check against itself
        """

        for obj in self.mapData:
            # Checking to see how close each object is
            if obj.get_name() == name:
                # So we dont check the same object
                continue

            if isinstance(obj, "Person"):
                # Object is person get their edge coordinates
                person1 = {
                    "radius" : radius,
                    "xCoord" : check_coords[0],
                    "yCoord" : check_coords[1]
                }
                person2 = {
                    "radius" : obj.get_width(),
                    "xCoord" : obj.get_coordinates()[0],
                    "yCoord" : obj.get_coordinates()[1]
                }

                if self.check_circle_touch(person1, person2) == 0:
                    #Circles overlap
                    return False

            else:
                # Object is instance of baseObject, i.e. Bar
                width = object.get_width()
                height = object.get_height()
                rectangleCoordRanges = self.__get_coordinates_range(object.get_coordinates(), [width, height])

                if self.check_circle_overlap_rectangle(edgeCoordinates, rectangleCoordRanges):
                    print("good")

        #Coordinates are fine to move to
        return True


    def check_circle_touch(self, person1, person2):
        """Checks to see if two circles have either coordinates overlap
        Reference: https://www.geeksforgeeks.org/check-two-given-circles-touch-intersect/
        Author: Smitha Dinesh Semwal
        :returns 1 if touching, -1 if not touching and 0 if there is an overlap
        """

        distSq = (person1["xCoord"] - person2["xCoord"]) * (person1["xCoord"] - person2["xCoord"]) + (person1["yCoord"] - person2["yCoord"]) * (person1["yCoord"] - person2["yCoord"]);
        radSumSq = (person1["radius"] + person2["radius"]) * (person1["radius"] + person2["radius"]);
        if (distSq == radSumSq):
            # Circles are touching
            return 1
        elif (distSq > radSumSq):
            #Circles are not touching
            return -1
        else:
            #Circles overlap
            return 0

    def check_circle_overlap_rectangle(self, circleEdge, rectangle):
        """
        Checks to see if a circle and rectangle intersect
        :param circle: properties
        :param rectangle: rectangle properties
        :return: True if overlap
        """
        for edge in circleEdge:
            if rectangle["X"][0] < edge[0] and edge[0] < rectangle["X"][1] and rectangle["Y"][0] < edge[1] and edge[1] < rectangle["Y"][1]
                return False
        return True


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
        returnValue = {
            "X" : xRanges,
            "Y" : yRanges
        }
        # return [xRanges, yRanges]
        return returnValue

    def getMap(self):
        # Returns the map
        return self.mapDefult

    def addPerson(self,name,cordinateX,cordinateY,angle,width):
        """adds a person to the array"""
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

    def whichPerson(self,cords):
        """This function checks to see if a cordiante is within another person and returns their id"""
        map = self.getMap()
        for people in map:
            if people[0] == "person":
                x = people[2][0]
                y = people[2][1]
                radias = people[4]
                x1 = cords[0]
                y1 = cords[1]
                # This is pythagorous and works out if the point is within the circle
                distance = math.pow(x1 - x,2) + math.pow(y1 - y,2)
                distanceRoot = math.sqrt(distance)
                if distanceRoot <= radias:
                    return people[1]

    def rotatePerson(self,newAngle):
        map = self.getMap()
        map[0][3] = newAngle
        # print(map[0][3])

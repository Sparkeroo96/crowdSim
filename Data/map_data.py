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
from Objects.wall import Wall
from People.flockingPerson import FlockingPerson

from Objects.bar import Bar

class map_data:

    mapData = []
    gui = None
    tick_rate = 0

    def __init__(self, gui, tick_rate):
        self.gui = gui
        self.tick_rate = tick_rate

    def map_default(self):
        """Getting default map data"""

        self.add_people_to_map(1)
        self.add_bar_to_map(1)
        self.add_toilet_to_map(1)

        return self.mapData

    def add_people_to_map(self, peopleCount):
        """Adding people to map"""
        x = 0
        while x < peopleCount:
            coords = [50 * (x + 1), 50 * (x + 1)]

            newPerson = person.Person("person " + str(len(self.mapData)), coords, 20, rand.randint(0,360), self.tick_rate)

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

    def add_toilet_to_map(self, toiletCount):
        """
        Adds a number of toilets to the map
        :param toiletCount: the number to add
        :return:
        """
        x = 0
        while x < toiletCount:
            coords = [100 * (x + 1), 50]
            newToilet = toilet.Toilet(coords, "toilet " + str(len(self.mapData)), 20, 20)

            self.mapData.append(newToilet)

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
        """Checks to see if a set of coordinates is occupied by an obj or person
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the obj that is the size of the obj currently checking coords, if it has a width and height give it as a list
        :param object_name is the name of the obj doing checking so it doesnt check itself
        """

        ranges = self.get_coordinates_range(coordinates, object_size)

        for obj in self.mapData:
            if obj.get_name() == object_name:
                continue

            if isinstance(obj, "Person"):
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

            if isinstance(obj, Person):
                # Object is person get their edge coordinates
                person1 = {
                    "radius": radius,
                    "xCoord": check_coords[0],
                    "yCoord": check_coords[1]
                }
                person2 = {
                    "radius": obj.get_width(),
                    "xCoord": obj.get_coordinates()[0],
                    "yCoord": obj.get_coordinates()[1]
                }

                if self.check_circle_touch(person1, person2) == 0:
                    # Circles overlap
                    return obj

            else:
                # Object is instance of baseObject, i.e. Bar
                # width = obj.get_width()
                # height = obj.get_height()
                objSize = [obj.get_width(), obj.get_height()]
                objCoords = obj.get_coordinates()
                rectangleCoordRanges = self.get_coordinates_range(objCoords, objSize)
                if self.check_circle_overlap_rectangle(edgeCoordinates, rectangleCoordRanges):
                    return obj

        # Coordinates are fine to move to

        return True

    def check_circle_touch(self, person1, person2):
        """Checks to see if two circles have either coordinates overlap
        Reference: https://www.geeksforgeeks.org/check-two-given-circles-touch-intersect/
        Author: Smitha Dinesh Semwal
        :returns 1 if touching, -1 if not touching and 0 if there is an overlap
        """

        distSq = (person1["xCoord"] - person2["xCoord"]) * (person1["xCoord"] - person2["xCoord"]) + (
                    person1["yCoord"] - person2["yCoord"]) * (person1["yCoord"] - person2["yCoord"]);
        radSumSq = (person1["radius"] + person2["radius"]) * (person1["radius"] + person2["radius"]);
        if (distSq == radSumSq):
            # Circles are touching
            return 1
        elif (distSq > radSumSq):
            # Circles are not touching
            return -1
        else:
            # Circles overlap
            return 0

    def check_circle_overlap_rectangle(self, circleEdge, rectangle):
        """
        Checks to see if a circle and rectangle intersect
        :param circle: properties
        :param rectangle: rectangle properties to be given as [[X][lowX][highX], [Y][lowY][highY]]
        :return: True if overlap
        """
        # print(str(circleEdge))
        # print(str(rectangle))
        # quit()

        lowX = rectangle["X"][0]
        highX = rectangle["X"][1]
        if rectangle["X"][1] < rectangle["X"][0]:
            lowX = rectangle["X"][1]
            highX = rectangle["X"][0]

        lowY = rectangle["Y"][0]
        highY = rectangle["Y"][1]
        if rectangle["Y"][1] < rectangle["Y"][0]:
            lowY = rectangle["Y"][1]
            highY = rectangle["Y"][0]

        # Adjusting for diagonal movement
        lowX -= 2
        highX += 2
        lowY -= 2
        highY += 2

        for edge in circleEdge:
            if rectangle["X"][0] < edge[0] and edge[0] < rectangle["X"][1] and rectangle["Y"][0] < edge[1] and edge[1] < rectangle["Y"][1]:
                return True

        return False

    def check_person_touching_object(self, circleEdge, rectangle):
        """
        Checks to see if a person is intersecting or next too an object
        :param circleEdge: Circle edge array
        :param rectangleCoordsRange: Rectangles coordinates to be given as [[X][lowX][highX], [Y][lowY][highY]]
        :return: True on yes
        """

        if self.check_circle_overlap_rectangle(circleEdge, rectangle) is True:
            return True

        for edge in circleEdge:
            if (edge[0] == rectangle["X"][0] or edge[0] == (rectangle["X"][0] - 1) or edge[0] == rectangle["X"][1] or edge[0] == (rectangle["X"][1] + 1)) and (edge[1] == rectangle["Y"][0] or edge[1] == (rectangle["Y"][0] - 1) or edge[1] == rectangle["Y"][1] or edge[1] == (rectangle["Y"][0] + 1)):
                return True

        return False

    def add_bar_to_map(self, barCount):
        """Adds a number of bars to the map"""
        x = 0
        while x < barCount:
            coords = [100 * (x + 1), 100 * (x + 1)]
            newBar = bar.Bar(coords, "bar " + str(len(self.mapData)), 100, 20)

            self.mapData.append(newBar)

            x += 1

    def get_coordinates_range(self, coordinates, object_size):
        """ Function gets the range of spaces used by a set of coordinates
        :param coordinates is the set its checking to see if anything occupies it
        :param object_size is the obj that is the size of the obj currently checking coords, if it has a width and height give it as a list
        """
        xCoord = coordinates[0]
        yCoord = coordinates[1]
        # print("object size = " +str(object_size))
        # print("coordinates = " + str(coordinates))
        if isinstance(object_size, list):
            # If there is a width and height give it as a list
            xSize = object_size[0]
            ySize = object_size[1]

        else:
            # For when you just give the width, most likely gonna be for a person
            xSize = object_size
            ySize = object_size

        # X Coordinate ranges
        lowX = 0
        highX = 0
        lowY = 0
        highY = 0
        if xSize >= 0:
            lowX = xCoord
            highX = xCoord + xSize
        else:
            lowX = xCoord - abs(xSize)
            highX = xCoord

        if ySize >= 0:
            lowY = yCoord
            highY =  yCoord + ySize
        else:
            lowY = yCoord - abs(ySize)
            highY = yCoord

        xRanges = [lowX, highX]
        yRanges = [lowY, highY]
        returnValue = {
            "X" : xRanges,
            "Y" : yRanges
        }
        # print("get coords range " + str(returnValue))
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


    def what_object(self, coords):
        """This function checks to see if a cordiante is within another person and returns a reference to the object"""
        for obj in self.mapData:
            objCoords = obj.get_coordinates()

            if obj.get_shape() == "circle":
                x = objCoords[0]
                y = objCoords[1]
                radias = obj.get_width() / 2
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
                # coordsRange = self.get_coordinates_range(coords, [width, height])
                coordsRange = self.get_coordinates_range(objCoords, [width, height])
                if self.point_in_coordinates_range(coords, coordsRange):
                    return obj


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
            # print(obj)
            if isinstance(obj,Person):
                # print("ran")
                obj_type = 'Person'
                coords = obj.get_coordinates()
                angle = obj.get_angle()
                width = obj.get_width()
                data = [obj_type,coords,width,angle]
            if isinstance(obj, Wall):
                obj_type = 'Wall'
                coords = obj.get_coordinates()
                width = obj.get_width()
                height = obj.get_height()
                data = [obj_type,coords,width,height]
            str1 = '/'.join(str(e) for e in data)
            # print(str1)
            file.write(str1 + "\n")
        file.close()


    def import_from_file(self,file,save_name):
        file = open(file,'r')
        # print(file.read())
        # print(save_name)
        x = 1
        running_string = ""
        found_load = []
        new_save_array = []
        save_name = save_name.lower()
        for line in file:
            running_string = running_string + str(line)
        save_array = running_string.split("######")
        # print(save_array)
        for save in save_array:
            single_save_array =[x.strip() for x in save.split("\n")]
            new_save_array.append(single_save_array)
        for save in new_save_array:
            if save[1] == save_name:
                found_load = save

        if not found_load == []:
            found_load.pop(0)
            found_load.pop(0)
            for line in found_load:
                result = [x.strip() for x in line.split('/')]
                if not result == [""]:
                    coords = [x.strip() for x in result[1].split(",")]
                    coordX = coords[0].translate({ord("'"): None})
                    coordY = coords[1].translate({ord("'"): None})
                    coordX = coordX.translate({ord("["): None})
                    coordY = coordY.translate({ord("]"): None})
                    coords = [int(float(coordX)), int(float(coordY))]
                    if result[0] == 'Person':
                        newPerson = person.Person("person " + str(len(self.mapData)), coords, int(result[2]), int(result[3]))
                        self.mapData.append(newPerson)
                    elif result[0] == 'Wall':
                        newWall = Wall(coords,int(result[2]),int(result[3]))
                        self.mapData.append(newWall)
        else:
            print("ERROR FILE NOT FOUND")
        file.close()

    def get_map(self):
        return self.mapData

    def clear_map(self):
        self.get_map() == []

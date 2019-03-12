"""
Main Map class that should handle the init and management of the map
Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import random as rand
import math
from People import *
from Objects import *
from Nodes import node
from Algorithm import a_starv2
import numpy

# Seems to need these for allowing isinstance(example, Person), doesnt work with the above import
from People.person import Person
from Objects.wall import Wall
from Objects import fireExit
from People.flockingPerson import FlockingPerson

from Objects.bar import Bar
from Objects.danceFloor import DanceFloor
from Objects.toilet import Toilet

constant = 0
class map_data:
    """TO DO"""
    path = []
    """TO DO"""
    nodeList = []
    """Wall values to iterate over"""
    values_to_append = []
    mapData = []
    gui = None
    tick_rate = 0
    sim_screen_width = None
    sim_screen_height = None

    def __init__(self, gui, tick_rate):
        self.gui = gui
        self.tick_rate = tick_rate

    def map_default(self):
        """Getting default map data"""
        self.add_people_to_map(15)
        self.add_bar_to_map(1)
        self.add_toilet_to_map(1)
        # self.add_wall_to_map()
        global constant
        if constant == 0:
            # self.generate_nodes()
            constant += 1
        return self.mapData

    def add_people_to_map(self, coords, size, angle):
        """Adding people to map"""
        """CHANGED THE SIZE TO 10"""
        # newPerson = person.Person("person " + str(len(self.mapData)), coords, 10, angle, self.tick_rate)
        newPerson = person.Person("person " + str(len(self.mapData)), coords, 15, angle, self.tick_rate)
        newPerson.add_map(self, coords)
        self.mapData.append(newPerson)


    def add_bar_to_map(self, coords, width, height):
        """Adds a bar to the map when it is called buy the builder"""
        newBar = bar.Bar(coords, "bar " + str(len(self.mapData)),width, height)
        self.set_nodes_values(newBar)
        self.mapData.append(newBar)

    def add_wall_to_map(self, cords, width, height):
        newWall = wall.Wall(cords,width,height)
        self.set_nodes_values(newWall)
        self.get_map().append(newWall)

    def add_dancefloor_to_map(self, coords, width, height):
        newDancefloor = danceFloor.DanceFloor(coords, "dancefloor " + str(len(self.mapData)), width, height)
        self.mapData.append(newDancefloor)

    def add_toilet_to_map(self, coords, width, height):
        """
        This function adds a toliet to the data structure based off the map builder imput
        :param coords: The X and Y or the base corner
        :param hight: The height of the object
        :param width: The width of the toilet
        :return: None
        """

        newToilet = toilet.Toilet(coords, "toilet " + str(len(self.mapData)), width, height)
        self.set_nodes_values(newToilet)
        self.mapData.append(newToilet)

    def get_object_colour_code(self, objectType):
        """
        Gets an object colour code
        :param objectType: The object type you are looking for
        :return: Returns an RGB array, false if no such object type exists
        """

        for obj in self.mapData:
            # print("objType: " + str(type(obj)))
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

    def angleMath(self, angle, xcord, ycord, vision):
        """This is the maths that returns the amount the x and y cordianes need to change to produce the cordinates
        of the new location """
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

        if self.check_coordinates_in_bounds(check_coords, radius) is False:
            return False

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
                    "radius": obj.get_width() / 2,
                    "xCoord": obj.get_coordinates()[0],
                    "yCoord": obj.get_coordinates()[1]
                }

                if self.check_circle_touch(person1, person2) == 0:
                    # Circles overlap
                    return obj

            else:
                # Object is instance of baseObject, i.e. Bar
                objSize = [obj.get_width(), obj.get_height()]
                objCoords = obj.get_coordinates()
                rectangleCoordRanges = self.get_coordinates_range(objCoords, objSize)
                if self.check_circle_overlap_rectangle(edgeCoordinates, rectangleCoordRanges):
                    if obj.get_clip_through() == False: #
                        return obj

        # Coordinates are fine to move to
        return True

    def check_coordinates_in_bounds(self, coordinates, radius):
        """
        Checks to see is a set of coordinates is out of the map bounds for the person
        :param coordinates: the coordinates to move too
        :param radius: the persons radius
        :return: True if coordinates are fine
        """
        if coordinates[0] <= 0 or coordinates[1] <= 0:
            return False

        lowX = coordinates[0] - radius
        lowY = coordinates[1] - radius
        highX = coordinates[0] + radius
        highY = coordinates[1] + radius

        if lowX < 0 or lowY < 0:
            return False

        if highX > self.gui.get_screen_width() or highY > self.gui.get_screen_height():
            return False

        return True

    def check_circle_touch(self, person1, person2):
        """Checks to see if two circles have either coordinates overlap
        Reference: https://www.geeksforgeeks.org/check-two-given-circles-touch-intersect/
        Author: Smitha Dinesh Semwal
        :returns 1 if touching, -1 if not touching and 0 if there is an overlap
        """

        distSq = (person1["xCoord"] - person2["xCoord"]) * (person1["xCoord"] - person2["xCoord"]) + (
                    person1["yCoord"] - person2["yCoord"]) * (person1["yCoord"] - person2["yCoord"])
        radSumSq = (person1["radius"] + person2["radius"]) * (person1["radius"] + person2["radius"])
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



    def export(self,file_name,save_name):
        """
        Exports the current map data into a format that can be recreated by the import onto the maps_saves.txt
        :param file_name: The name of the target file
        :param save_name: The name of the map you are saving
        :return: True if it was saved sucesfully and False if it fails
        """
        check_name = self.check_save_name(file_name,save_name)
        if check_name:
            map = self.get_map()
            data = []
            file = open(file_name, 'r')
            saved_data = []
            for line in file:
                saved_data.append(line)
            file.close()
            file = open(file_name,'w+')
            for line in saved_data:
                file.write(line)
            file.write("######" + "\n")
            file.write(save_name.lower() + "\n")
            for obj in map:
                # print(obj)
                coords = obj.get_coordinates()
                width = obj.get_width()
                height = obj.get_height()
                if isinstance(obj, Wall):
                    obj_type = 'Wall'

                if isinstance(obj, Bar):
                    obj_type = "Bar"
                if isinstance(obj, Toilet):
                    obj_type = "Toilet"

                if isinstance(obj, DanceFloor):
                    obj_type = "DanceFloor"

                data = [obj_type, coords, width, height]
                # Different data needed to record person objects

                if isinstance(obj,Person):
                    # print("ran")
                    obj_type = 'Person'
                    coords = obj.get_coordinates()
                    angle = obj.get_angle()
                    width = obj.get_width()
                    data = [obj_type,coords,width,angle]

                str1 = '/'.join(str(e) for e in data)
                file.write(str1 + "\n")
            file.close()
            return True
        else:
            return False

    def check_save_name(self,file_name,save_name):
        """
        Sees if the name of the map is already taken
        :param file_name: maps_saves.txt
        :param save_name: the name you are testing to see if it is taken
        :return: True for the file name is free, False for if the name is taken
        """
        file = open(file_name, 'r')
        running_string = ''
        for line in file:
            running_string = running_string + str(line)
        search_array = running_string.split("######")
        for save in search_array:
            save_array = save.split("\n")
            if len(save_array) == 1:
                continue
            if str(save_array[1]) == save_name.lower():
                return False
        file.close()
        return True


    def import_from_file(self, file, save_name):
        """
        This takes the maps_saves.txt and a name of a map and imports it into the system
        :param file: maps_saves.txt
        :param save_name: the name of the map you want to load
        :return: True if loaded succesfully, False if not
        """
        file = open(file,'r')
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
            if len(save) == 1:
                continue
            if save[1] == save_name:
                found_load = save

        if not found_load == []:
            found_load.pop(0)
            found_load.pop(0)
            for line in found_load:
                result = [x.strip() for x in line.split('/')]
                if not result == [""]:
                    result[0] = result[0].lower()
                    coords = [x.strip() for x in result[1].split(",")]
                    coordX = coords[0].translate({ord("'"): None})
                    coordY = coords[1].translate({ord("'"): None})
                    coordX = coordX.translate({ord("["): None})
                    coordY = coordY.translate({ord("]"): None})
                    coords = [int(float(coordX)), int(float(coordY))]
                    if result[0] == 'person':
                        self.add_people_to_map(coords, int(result[2]), int(result[3]))
                        # newPerson = person.Person("person " + str(len(self.mapData)), coords, int(result[2]), int(result[3]),self.tick_rate)
                        # self.mapData.append(newPerson)
                    elif result[0] == 'wall':
                        self.add_wall_to_map(coords, int(result[2]), int(result[3]))
                        # newWall = Wall(coords,int(result[2]),int(result[3]))
                        # self.mapData.append(newWall)
                    elif result[0] == "toilet":
                        self.add_toilet_to_map(coords, int(result[2]), int(result[3]))
                        # new_toilet = Toilet(coords,"toilet" + str(len(self.mapData)),int(result[2]),int(result[3]))
                        # self.mapData.append(new_toilet)
                    elif result[0] == "bar":
                        self.add_bar_to_map(coords, int(result[2]), int(result[3]))
                        # newBar = bar.Bar(coords,str(len(self.get_map())),int(result[2]),int(result[3]))
                        # self.mapData.append(newBar)
                    elif result[0] == "dancefloor":
                        self.add_dancefloor_to_map(coords, int(result[2]), int(result[3]))
                        print("Dancefloor")
            # self.generate_nodes()
            return True
        else:
            print("ERROR FILE NOT FOUND")
        file.close()
        return False

    def add_to_map(self,object_type,x_cord,y_cord,width,height):
        """
        Takes the name of the object then creates the apropriate object to the array only works for cubes/ rectangles
        :param object_type:
        :param x_cord: x coordinate
        :param y_cord: y coordinate
        :param width: width of the object
        :param height: height of the object
        :return: Null
        """
        cords = [x_cord,y_cord]
        objectType = object_type.lower()
        if objectType == 'wall':
            self.add_wall_to_map(cords, width, height)
        if objectType == 'bar':
            self.add_bar_to_map(cords, width, height)
        if objectType == "toilet":
            self.add_toilet_to_map(cords, width, height)
        if objectType == "d floor":
            print("Dancefloor")
            self.add_dancefloor_to_map(cords, width, height)
        """Used to create the nodes"""
        # self.generate_nodes()

    def delete_object(self,coords):
        """
        Function that removes rectangles by their coordinates, takes it out of the map_data
        :param coords: the x and y cordinate of the object on the display
        :return: Null
        """
        map_data = self.get_map()
        x_coord = coords[0]
        y_coord = coords[1]
        index = 0
        for obj in map_data:
            if obj.get_shape != "circle":
                cords = obj.get_coordinates()
                x1 = cords[0]
                y1 = cords[1]
                x2 = x1 + obj.get_width()
                y2 = y1 + obj.get_height()
                if obj.get_width() < 0:
                    x2 = x1
                    x1 = x2 + obj.get_width()
                if obj.get_height() < 0:
                    y2 = y1
                    y1 = y2 + obj.get_height()
                if x1 < x_coord and x2 > x_coord and y1 < y_coord and y2 > y_coord:
                    map_data.pop(index)
            index = index + 1


    def get_map(self):
        """Gets the map of objects"""
        return self.mapData

    def clear_map(self):
        """Clears the map of objects"""
        self.mapData = []

    def get_people_within_range(self, coordinates, diameter, ignorePerson):
        """
        Gets an array of people within a distance of coordiantes
        :param coordinates: Coordinates to search around
        :param diameter: Diameter to check around
        :return: An array
        """

        returnArray = []

        checkCircle = {
            "xCoord": coordinates[0],
            "yCoord": coordinates[1],
            "radius": (diameter / 2)
        }

        for obj in self.mapData:
            if isinstance(obj, Person) is False or obj == ignorePerson:
                continue

            objCoordinates = obj.get_coordinates()
            objWidth = obj.get_width()
            personParameters = {
                "xCoord": objCoordinates[0],
                "yCoord": objCoordinates[1],
                "radius": (objWidth / 2)
            }
            if self.check_circle_touch(checkCircle, personParameters) == 0:
                returnArray.append(obj)

        if returnArray == []:
            return False

        return returnArray

    def get_objects_within_range(self, coordinates, radius, edgeCoordinates, ignorePerson):
        """
        Returns an array of all objects within a range
        :param coordinates: The target coordinates
        :param radius: The area to search
        :return: Array of objectss
        """

        objArray = self.get_people_within_range(coordinates, radius * 2, ignorePerson)
        if objArray is False:
            objArray = []

        for obj in self.mapData:
            if isinstance(obj, Person):
                continue

            object_size = [obj.get_width(), obj.get_height()]
            rectangleProperties = self.get_coordinates_range(obj.get_coordinates(), object_size)
            if self.check_circle_overlap_rectangle(edgeCoordinates, rectangleProperties):
                if not obj.get_clip_through():
                    objArray.append(obj)

        return objArray

    def add_fireEscape_to_map(self):
        x = 0
        fireEscapes = []
        while x <= 1:
            coords = [480, 200]
            newFireEscape = fireExit.FireExit(coords, "fireEscape " + str(self.mapData), 20, 30)
            self.mapData.append(newFireEscape)
            x += 1

    def calculate_starting_nodes(self):
        screen_width = 800
        screen_height = 600
        node_distance = 20  # Pixel distance between each node. The higher the number, the greater granularity we get.
        """
        Calculates how many nodes will be generated on the starting init.
        :return: 
        """
        total_pixels = (screen_height * screen_width)
        total_nodes = total_pixels / (node_distance * node_distance)
        return int(total_nodes)

    def set_nodes_values(self, wall):
        """
        This function sets the wall nodes value to 1.
        In doing so, it will make the node unavailable to travel to & through.
        :param walls: the walls to set nodes to.
        :return:
        """
        screen_width = 800
        screen_height = 600
        node_distance = 20 # Spacing between each node.
        xBoundaries = int(screen_width/node_distance)
        yBoundaries = int(screen_height/node_distance)
        cordX = (int(wall.get_coordinates()[0] / node_distance))
        cordY = (int(wall.get_coordinates()[1] / node_distance))
        width = (math.ceil(wall.get_width() / node_distance))
        height = (math.ceil(wall.get_height() / node_distance))
        x2 = cordX + width
        y2 = cordY + height

        # print("widths")
        # print((wall.get_width() / node_distance))
        # print(int(width))
        # print("heights")
        # print((wall.get_height() / node_distance))
        # print(int(height))

        # If the coord starts from bottom right
        if int(width) < 0 and int(height) < 0:
            # print("in bottom right")
            width2 = int(abs(width)) + 1 # Rounding up on a negative number will drop by one
            height2 = int(abs(height)) + 1
            if width2 < height2:
                width2 += 1
            else:
                height2 += 1
            # print(width2, height2)
            for x in range(width2):
                # self.values_to_append.append([cordX - x, cordY])
                # self.values_to_append.append([cordX - x, y2])
                for y in range(height2):
                    self.values_to_append.append([cordX - x, cordY - y])
            # for y in range(height2):
            #     self.values_to_append.append([cordX, cordY - y])
            #     self.values_to_append.append([x2, cordY - y])
        # If the coord starts from top Left
        if int(width) > 0 and int(height) > 0:
            # print("in top left")
            # print(width, height)
            # self.values_to_append.append([cordX + width + 1, cordY + height + 1])
            # self.values_to_append.append([cordX - 1, cordY + height + 1])
            # self.values_to_append.append([cordX + width + 1, cordY - 1])
            # self.values_to_append.append([cordX - 1, cordY - 1])
            for x in range(width):
                self.values_to_append.append([cordX + x, cordY])  # The top line in a rect
                self.values_to_append.append([cordX + x, y2])  # Bottom line in a rect
                for y in range(height):
                    self.values_to_append.append([cordX + x, cordY + y])
            for y in range(height):
                self.values_to_append.append([cordX, cordY + y])  # Left like in a rect
                self.values_to_append.append([x2, cordY + y])  # Right line in a rect
                # self.values_to_append.append([cordX + width, cordY + y])
        # If the coord starts from Bottom Left
        if int(width) > 0 and int(height) < 0:
            # print("in bottom left")
            height3 = int(abs(height)) + 1
            if height3 < width:
                height3 += 1
            for x in range(width):
                self.values_to_append.append([cordX + x, cordY])  # The top line in a rect
                self.values_to_append.append([cordX + x, y2])
                for y in range(height3):
                    self.values_to_append.append([cordX + x, cordY - y])
            for y in range(height3):
                self.values_to_append.append([cordX, cordY - y])
                self.values_to_append.append([x2, cordY - y])
        # If the coord starts from Top Right
        if int(width) < 0 and int(height) > 0:
            # print("in top right")
            width3 = int(abs(width)) + 1
            # print(width3)
            # print(height)
            if height > width3:
                width3 += 1
            for x in range(width3):
                self.values_to_append.append([cordX - x, cordY])
                self.values_to_append.append([cordX - x, y2])
                for y in range(height):
                    self.values_to_append.append([cordX - x, cordY + y])
            for y in range(height):
                self.values_to_append.append([cordX, cordY + y])  # Left like in a rect
                self.values_to_append.append([x2, cordY + y])

        # self.values_to_append.append([cordX + width + 1, cordY + height])
        self.values_to_append.append([x2, y2])  # Append the corner opposite
        # self.values_to_append.append([x2 + 1, y2])


        """Check values are in the grid"""
        # for v in self.values_to_append:
        #     if v[0] > yBoundaries and v[1] > xBoundaries:
        #         self.values_to_append.remove(v)

    """Generate the node objects that appear on the map"""


    def generate_nodes(self):
        """
        Generate all nodes, adding values to each node and applying this to a*
        :return:
        """
        screen_width = 800
        screen_height = 600
        node_distance = 20
        total_nodes = self.calculate_starting_nodes() # All nodes to being with.
        square_root = int(math.sqrt(total_nodes)) # The total length of the node map.
        maxX = int(screen_width/node_distance)
        maxY = int(screen_height/node_distance)

        listofID = []  # IDs for the nodes
        # print(self.calculate_starting_nodes())
        """Basic 10x10 grid"""
        simpleCords = []
        for number in range(0, total_nodes):
            listofID.append(number)
        """Create cords for the grid"""
        for x in range(maxX):
            for y in range(maxY):
                simpleCords.append([x, y])
        """Create 100 nodes, apply the coords"""
        for n in range(total_nodes):
            self.nodeList.append(node.Node(simpleCords[n], 0))
        """Obtaining last coord in the simple grid to create the range of maze"""
        """Create the empty node graph, adding 0's"""
        graph = numpy.zeros((maxX, maxY), int)
        """For the values in append, apply the value of 1 to the node object"""
        """1 Represents a wall"""
        for v in self.values_to_append:
            for n in self.nodeList:
                if v == n.get_idCoords():
                    n.set_value(1)
        openNodes = []
        for cords in self.nodeList:
            """if it is an environment object, show this in our graph"""
            if cords.get_value() == 1:
                graph[cords.get_idCoords()[0]][cords.get_idCoords()[1]] = cords.get_value()
            elif cords.get_value() == 0:  # Cord should be added to list of open nodes
                openNodes.append(cords.get_idCoords())
        # print(graph)
        """Stores all free nodes in a_star class"""
        a_starv2.set_open_nodes(openNodes)
        """Store all the nodes in the a_star class"""
        a_starv2.store_all_nodes(graph)

    def get_person_cord_info(self):
        personCoords = []
        personState = []
        personName = []
        personNeeds = []
        current_map = self.mapData
        for p in current_map:
            if "person" in p.get_name():
                # print(p.get_name())
                personCoords.append(p.get_coordinates())
                personName.append(p.get_name())
                personState.append(p.get_state_action())
                personNeeds.append(p.get_person_needs())

    def set_size_screen(self, width, height):
        self.sim_screen_width = width
        self.sim_screen_height = height
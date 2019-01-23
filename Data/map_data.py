"""
Main Map class that should handle the init and management of the map
Created by Chris Clark cc604
"""
import random as rand
import math
import string
from People import *
from Objects import *
from Algorithm import a_starv2
from Nodes import node
import numpy

astar = a_starv2

class map_data:
    counter = 0
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]

    personCords = []
    envCords = []

    mapDefult = [['person','id:1',[150,350],30,10],['person','id:2',[200,300],30,10],['wall',[10,10],[100,10]]]
    nodes = []

    mapData = []
    """Stores the grid replica of the surface"""
    grid = []
    """Path for a person to follow"""
    path = []

    nodeList = []
    """Wall values to iterate over"""
    values_to_append = []

    def __init__(self):
        print("Map_data Object Created")
        # self.generate_nodes()
        # self.generate_nodes()
        # self.get_node_coords()
        # print(self.get_node_coords())
        # self.generate_grid()


    """functions to append/obtain the person/env cords"""
    def set_p_coords(self, obj):
        self.personCords.append(obj)

    def set_e_coords(self, obj):
        self.envCords.append(obj)

    def get_p_coords(self):
        return self.personCords

    def get_e_coords(self):
        return self.envCords

    def map_default(self):
        """Getting default map data"""
        self.add_people_to_map(2)
        self.add_env_obj_to_map()
        self.add_wall_to_map()
        self.generate_nodes()
        return self.mapData



    def add_people_to_map(self, peopleCount):
        """Adding people to map"""
        x = 0
        while x < peopleCount:
            if x == 0:
                coords = [200, 300]
            else:
                coords = [20, 20]
            # print(coords)

            newPerson = person.Person("person " + str(len(self.mapData)), coords, None)
            """Update the p cooords"""
            self.mapData.append(newPerson)

            x += 1

    def add_env_obj_to_map(self):
        newEnvObject = bar.Bar()
        """Update the env cooords"""
        self.set_e_coords(newEnvObject.get_coordinates())
        self.mapData.append(newEnvObject)
    """Adds a wall to the map a"""
    def add_wall_to_map(self):
        newWall = []
        newWall.append(wall.Wall(4, "wall1", [0, 100], 0, 400, "wall"))
        newWall.append(wall.Wall(4, "wall2", [50, 200], 30, 500, "wall"))
        newWall.append(wall.Wall(4, "wall3", [0, 400], 30, 400, "wall"))
        for walls in newWall:
            self.mapData.append(walls)
        self.set_walls(newWall)


    def personVision(self,id):
        vision = 100
        angleOfVison = 30
        found = False
        for person in self.mapDefult:
            if person[0] == 'person':
                if person[1] == id:
                    xCord = person[2][0]
                    yCord = person[2][1]
                    angle1 = person[3] - (angleOfVison/2)
                    angle2 = person[3] + (angleOfVison/2)
                    if angle1 <= 0:
                        angle1 = angle1 + 360
                    if angle1 > 360:
                        angle1 = angle1 - 360
                    found = True
                    break
        if found == False:
            print("Error finding %s" % id)
            return 0
        # result = self.angleMath(angle1,xCord,yCord,vision)
        # # print('reslut1 = %s' %result)
        # cordA = [xCord, yCord]
        # cordB = [xCord + result[0],yCord + result[1]]
        # result2 = self.angleMath(angle2,xCord,yCord,vision)
        # cordC = [xCord + result2[0],yCord + result2[1]]
        # adding all the cordiantes along one line of vision
        x = 12
        resultArray = []
        rays = 10
        i = 0
        originalAngle = angle1
        while i <= rays:
            angle1 = originalAngle + (i * 5)
            if angle1 <= 0:
                angle1 = angle1 + 360
            if angle1 > 360:
                angle1 = angle1 - 360
            while vision >= x:
                value = self.angleMath(angle1,xCord,yCord,x)
                value = [xCord + value[0],yCord + value[1]]
                resultArray.append(value)
                x = x + 1
            i = i + 1
            x = 12
        return resultArray

    def angleMath(self, angle, xcord, ycord,vision):
        veritcal = 0
        horizontal = 0
        # print(angle)
        angle1 = math.radians(angle)
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

    def getMap(self):
        # Returns the map
        return self.mapDefult

    def addPerson(self,name,cordinateX,cordinateY,angle,width):
        array = self.mapDefult
        array.append('person',name,[cordinateX,cordinateY],angle,width)

    def whichPerson(self,cords):
        map = self.getMap()
        for people in map:
            if people[0] == "person":
                x = people[2][0]
                y = people[2][1]
                radias = people[4]
                x1 = cords[0]
                y1 = cords[1]
                distance = math.pow(x1 - x,2) + math.pow(y1 - y,2)
                distanceRoot = math.sqrt(distance)
                if distanceRoot <= radias:
                    return people[1]

    def rotatePerson(self,newAngle):
        map = self.getMap()
        map[0][3] = newAngle
        # print(map[0][3])

    """This will set wall on the nodes, so the person cannot pass through"""
    """Converts the coords to the required node id"""
    """Stores in values to append"""
    def set_walls(self, walls):
        for wall in walls:
            cordX = (int(wall.get_coordinates()[0] / 50))
            cordY = (int(wall.get_coordinates()[1] / 50))
            width = (int(wall.get_width() / 50))
            height = (int(wall.get_height() / 50))
            for x in range(width):
                self.values_to_append.append([cordX + x, cordY])
        """Check that coords are within the 10x10 grid"""
        for v in self.values_to_append:
            if v[0] > 9 and v[1] > 9:
                self.values_to_append.remove(v)
    """Generate the node objects that appear on the map"""
    def generate_nodes(self):
        """IDs for the nodes"""
        listofID = []
        """Basic 10x10 grid"""
        simpleCords = []
        """Actual Grid used by the map"""
        complexCords = []
        for number in range(0, 100):
            listofID.append(number)
        """Create cords for the 10x10 grid"""
        for x in range(100):
            simpleCords.append([math.floor(x/10), (x % 10)])
            """Create cords for the 500x500 grid"""
            complexCords.append([(math.floor(x / 10) * 50), (x % 10) * 50])
        """Create 100 nodes, apply the coords"""
        for n in range(100):
            self.nodeList.append(node.Node(simpleCords[n], 0, complexCords[n]))
        """Obtaining last coord in the simple grid to create the range of maze"""
        """Create the empty node graph"""
        graph = numpy.zeros((10, 10), int)
        """For the values in append, apply the value of 1 to the node object"""
        """1 Represents a wall"""
        for v in self.values_to_append:
            for n in self.nodeList:
                if v == n.get_idCoords():
                    n.set_value(1)
        for cords in self.nodeList:
            """if it is an environment object, show this in our graph"""
            if cords.get_value() == 1:
                graph[cords.get_idCoords()[0]][cords.get_idCoords()[1]] = cords.get_value()
        """Store all the nodes in the a_star class"""
        a_starv2.store_all_nodes(graph)
        """Placeholder locations - Need to run the algo from the person class"""
        # start = (self.nodeList[0].get_idCoords()[0]), (self.nodeList[0].get_idCoords()[1])
        # dest = (self.nodeList[99].get_idCoords()[0]), (self.nodeList[99].get_idCoords()[1])

"""
Main Map class that should handle the init and management of the map
Created by Chris Clark cc604
"""
import random as rand
import math
class map_data:
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]
    mapDefult = [['person','id:1',[150,350],30,10],['person','id:2',[200,300],30,10],['wall',[10,10],[100,10]]]

    def __init__(self):
        print("Map_data Object Created")

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
test = map_data()
test.whichPerson([205,305])

# Main Map class that should handle the init and management of the map
# Created by Chris Clark 11/12/2018
import random as rand
import math
class map_data:
    # The GUI currently operates at 30 FPS meaning that each second the array is cycled though 30 times
    # [personType,uniqueName, [cordinateX,cordinateY],directionLooking,width]
    # [wall,[cordinateX,cordinateY],[width,height]]
    mapDefult = [['person','id:1',[100,500],90,10],['person','id:2',[200,300],89,10],['wall',[10,10],[100,10]]]

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
                        print(angle1)
                    found = True
                    break
        if found == False:
            print("Error finding %s" % id)
            return 0
        result = self.angleMath(angle1,xCord,yCord,vision)
        # print('reslut1 = %s' %result)
        cordA = [xCord, yCord]
        cordB = [xCord + result[0],yCord + result[1]]
        result2 = self.angleMath(angle2,xCord,yCord,vision)
        cordC = [xCord + result2[0],yCord + result2[1]]
        # adding all the cordiantes along one line of vision
        x = 0
        resultArray = []
        while vision >= x:
            value = self.angleMath(angle1,xCord,yCord,x)
            value = [xCord + value[0],yCord + value[1]]
            resultArray.append(value)
            x = x + 1
        # print('result2 = %s' %result2)
        # print("coridanates")
        # print(cordA)
        # print(cordB)
        # print(cordC)
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

test = map_data()
test.personVision('id:2')

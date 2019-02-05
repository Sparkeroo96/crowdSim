# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018
# Modified by Chris
# from random import seed
from random import randint, seed
# import random
from People.stateMachine import StateMachine
from Objects.bar import Bar
from Objects.toilet import Toilet
from Objects.danceFloor import DanceFloor
import math


class Person:

    tick_rate = 0
    actionCount = None
    currentActionCount = None

    coordinates = [0,1]
    #Was size but chris has angle and width so using that instead
    angle = 0
    width = 10
    name = ""

    # map is Noneisinstance
    map = 0
    sight = 100

    vision = []

    #Persons colour for display on map
    colour = [255, 0, 0]
    shape = "circle"

    rememberedObj = ""
    rememberedObjType = ""
    rememberedColour = ""
    rememberedCoords = []

    rotate = 0

    headAngle = 0

    memory = {
        "Bar" : [],
        "DanceFloor" : [],
        "Toilet" : []
    }

    orderedDrink = 0
    hasDrink = 0

    # Persons "needs" first value is importance second is how much they want to do it
    #Not in use currently might remove them
    needs = [["toilet", 1, 0],
             ["thirst", 2, 0],
             ["entertainment", 3, 0],
             ["freshAir", 3, 0]
            ]

    defaultState = "greatestNeed"
    currentState = "greatestNeed"
    stateMachine = ""

    states = {
        "greatestNeed": [["usedToilet", "drinkDrink", "danced"], ["wantDrink", "wantToilet", "wantDance"]],

        "wantDrink": [["isGreatestNeed"], ["findBar", "orderDrink"]],
        "findBar": [["notAtBar"], ["moveToBar"]],
        "moveToBar": [["found", "notFound"], ["orderDrink", "moveToBar"]],
        "orderDrink": [["atBar"], ["drink"]],
        "drink": [["getDrink"], ["greatestNeed"]],

        "wantDance": [["isGreatestNeed"], ["dance", "findDanceFloor"]],
        "findDanceFloor": [["notAtDanceFloor", "notFound"], ["moveToDanceFloor"]],
        "moveToDanceFloor": [["notAtDanceFloor", "found"], ["dance", "moveToDanceFloor"]],
        "dance": [["atDanceFloor"], ["greatestNeed"]],

        "wantToilet": [["isGreatestNeed"], ["findToilet", "useToilet"]],
        "findToilet": [["notAtToilet"], ["moveToToilet"]],
        "moveToToilet": [["foundToilet", "notFoundToilet"], ["moveToilet", "useToilet"]],
        "useToilet": [["atToilet"], ["greatestNeed"]],
    }
    # gender = "" Use this one to determine which bathroom, later

    def __init__(self, name, coords, width, angle, tick_rate):
        # random.seed()
        self.name = name

        if coords:
            self.coordinates = coords
        if angle:
            self.angle = angle
        if width:
            self.width = width

        self.stateMachine = StateMachine("person")
        self.add_states_to_machine()

        self.currentState = self.defaultState
        self.stateMachine.set_current_state(self.currentState)

        self.tick_rate = tick_rate

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]

    def action(self):
        """What the person is going to do"""
        self.currentState = self.stateMachine.get_current_state()

        if self.wait_on_action_count():
            return "Waiting"

        stateAction = self.get_state_action()
        # print("currentState: " + self.currentState + " / stateAction " + stateAction)

        if stateAction == "navigateToRememberedObj":
             self.navigate_to_remembered_object()

        elif stateAction == "rotate":
             #print("no action")
             self.person_rotate()

        elif stateAction == "wait":
            # The person sits there and waits
            # print(self.name + " waiting")
            nothing = None
        else:
            self.random_move()
        # return self.random_move()

    def navigate_to_remembered_object(self):
        """
        Starts to move to the rememberd Object
        :return: True on success
        """

        nextMove = []
        x = self.coordinates[0]
        y = self.coordinates[1]
        targetCoordinates = self.rememberedObj.get_coordinates()

        #First move
        if targetCoordinates[0] > x:
            x += 1
        elif targetCoordinates[0] < x:
            x -=1

        if targetCoordinates[1] > y:
            y += 1

        elif targetCoordinates[1] < y:
            y -= 1

        nextMove = [x, y]

        # PHILS A* STUFF

        moveReturn = self.move(nextMove)
        if moveReturn != True:
            # There is a colliding object
            newCoords = self.get_coordinates_for_move_avoiding_collision_object(targetCoordinates, moveReturn, nextMove)

        # self.move(nextMove)


    def get_coordinates_for_move_avoiding_collision_object(self, targetCoordinates,  collisionObject, attemptedMove):
        """
        Try to move to an object avoiding an object
        :param targetCoordinates: The coordinates to move too
        :param collisionObject: The object to avoid
        :return: The coordinates to move to
        """

        newMove = attemptedMove

        collisionCoordinates = collisionObject.get_coordinates()
        if collisionObject[0] != self.coordinates[0]:
            if collisionObject[0] >= self.coordinates[0]:
                newMove[0] = newMove[0] - 1
            else :
                newMove[0] = newMove[0] + 1

        if collisionObject[1] != self.coordinates[1]:
            if collisionObject[1] >= self.coordinates[1]:
                newMove[1] = newMove[1] - 1
            else:
                newMove[1] = newMove[1] + 1

        return newMove

    def move(self, coordinates):
        """
        Moves to a given set of coordinates
        :param coordinates:
        :return: True on successful move, returns the collision object on false
        """

        collisionObject = self.map.check_coordinates_for_person(coordinates, self.width, self.name, self.get_edge_coordinates_array())

        # if self.map.check_coordinates_for_person(coordinates, self.width, self.name, self.get_edge_coordinates_array()):
        if collisionObject:
            self.coordinates = coordinates
            return True

        return collisionObject

    def person_rotate(self, clockwise = True):
        """
        Rotates the person so there vision goes full circle, going to do by 30 degrees
        :param clockwise: says whether or not to go clockwise or counter clockwise
        :return: Returns the new angle
        """
        # print(self.name + "  " + str(self.rotate))
        if clockwise:

            angleResult =  self.angle + 30
        else:
            angleResult = self.angle - 30

        if angleResult > 360:
            angleResult = angleResult - 360

        elif angleResult < 0:
            angleResult = 360 - angleResult

        self.angle = angleResult
        self.rotate += 1


        return angleResult



    def random_move(self):
        """Person moving randomly around the map"""
        randomNumber = randint(0, 8)
        # #print(self.name + " should move " + str(randomNumber))
        newCoordinates = 0
        # #print(self.name + " random number " + str(randomNumber) + " -- initial coords " + str(self.coordinates))
        if randomNumber <= 2: #person move up
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]

        elif randomNumber <= 4: #Person move down
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]

        elif randomNumber <= 6: #person move right
            newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]

        elif randomNumber <= 8: #Person move left
            newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]
        self.coordinates = newCoordinates
        # print(self.get_coordinates())

        # PERSON NEEDS TO SEE IF THERE IS SOMETHING OCCUPING THIS SPACE
        # ADD THAT IN
        # if isinstance(newCoordinates, list):
        #     edgeCoordinates = self.get_edge_coordinates_array()

            # if self.map.check_coordinates_for_person(newCoordinates, self.width, self.name, edgeCoordinates):

    def store_coordinates(self, coordinates):
        """Storing a set of coordinates"""
        self.coordinates = coordinates

    def get_coordinates(self):
        """Getting stored coordinates"""
        return self.coordinates

    def get_name(self):
        """Returns the name of the person"""
        return self.name

    def get_angle(self):
        """Returns the objects angle"""
        return self.angle

    def get_width(self):
        """Returns the objects size"""
        return self.width

    def get_size(self):
        """returns persons size"""
        return self.size

    def get_height(self):
        """Returns the objects height"""
        return self.height

    def get_shape(self):
        """Returns the shape of the object to draw"""
        return self.shape

    def get_colour(self):
        """Returns the persons colour"""
        return self.colour

    def get_sight(self):
        """Returns the persons sight range"""
        return self.sight

    def get_state_action(self):
        """Causes the person to act based on their current state"""
        # #print("get state action " + str(self.currentState))

        action = "moveRandom"

        if self.currentState == self.defaultState:
            # #print(self.name + " in greatest need")
            self.currentState = self.stateMachine.get_next_state()
        else:
            #print("not greatest need")
            x = 0

        if "want" in str(self.currentState):
            # #print("here")
            # Person has a want desire
            if self.want_action(self.currentState):
                action = "navigateToRememberedObj"
                self.rotate = 0
                self.advance_state_machine()

            else:
                action = "rotate"

        elif "find" in str(self.currentState):
            # Person trying to find an object
            #print(self.name + " finding object")
            # print("remembered obj type " + self.rememberedObjType)
            if self.find_object(self.rememberedObjType):
                action = "navigateToRememberedObj"
                self.rotate = 0
                # print("here")
                self.advance_state_machine()
            else:
                # Cant find object do a circle to see it
                if self.rotate < 12:
                    action = "rotate"

                else:
                    #Done a circle move or rotate, dont want it to
                    random = randint(0, 100)
                    if random == 1:
                        action = "rotate"
                        self.rotate = 0
                    else:
                        action = "moveRandom"
                #Move random or rotate?

        elif "move" in str(self.currentState):
            # Person moving to object
            # print(self.name + " Person moving to object")
            action = "navigateToRememberedObj"

            #If the person is next to the thing they are supposed to be on like a bar, advance the state again
            objectSize = [self.rememberedObj.get_width(), self.rememberedObj.get_height()]
            rememberedObjectCoords = self.rememberedObj.get_coordinates()
            # print("rememberedObj " + str(self.rememberedObj))
            # print("rememberedObjectCoords " + str(rememberedObjectCoords))
            rectangleCoordRanges = self.map.get_coordinates_range(rememberedObjectCoords, objectSize)
            selfEdge = self.get_edge_coordinates_array()

            if self.map.check_circle_overlap_rectangle(selfEdge, rectangleCoordRanges):
                # print("at target")
                self.advance_state_machine()
            else:
                # print("not at target")
                nothing = None

        elif self.currentState == "orderDrink":
            # Person is ordering their drink
            #print(self.name + " Ordering a drink")
            action = "wait"
            # self.clear_remembered_object()
            if self.has_ordered_drink() == 0 and self.has_drink() is False:
                self.order_drink()
                self.clear_remembered_object()

            elif self.has_drink():
                self.advance_state_machine()


        elif self.currentState == "drink":
            # Person drinks their drink
            self.drink_drink()
            self.advance_state_machine()
            # ACTION MIGHT CHANGE, LEAVE AT MOVE RANDOM FOR TIME

        elif self.currentState == "dance":
            # Person will dance
            #print(self.name + " is dancing")
            # self.stateMachine.get_next_state()
            self.advance_state_machine()

        elif self.currentState == "useToilet":

            action = "wait"
            self.use_toilet()
                # Toilet is free and now you are using it
            # self.clear_remembered_object()

        return action

    def want_action(self, wantState):
        """The people want to do something"""
        if wantState == "wantDrink":
            #print("wantDrink")
            searchObject = "Bar"

        elif wantState == "wantDance":
            #print("want dance")-
            searchObject = "DanceFloor"

        else:
            #print("want Toilet")
            searchObject = "Toilet"

        #print("Search object " + searchObject)
        self.rememberedObjType = searchObject

        self.advance_state_machine()
        # self.currentState = self.stateMachine.choose_next_state("find" + searchObject)

        return self.find_object(searchObject)

    def find_object(self, searchObject):
        """This function does the find function of a person
        :param searchObject: The object you want to look for
        :return Returns True if there are objects, false if it cant find one
        """

        closestObj = self.get_closest_object_from_memory(searchObject)

        if closestObj is False or closestObj is None:
            return False
        else:
            self.rememberedObjType = searchObject
            self.rememberedObj = closestObj
            self.rememberedCoords = closestObj.get_coordinates()
            self.rememberedColour = closestObj.get_colour()
            return True

    def clear_remembered_object(self):
        """
        Clears the remembered object
        """
        self.rememberedObj = ""
        self.rememberedObjType = ""
        self.rememberedColour = ""
        self.rememberedCoords = []

    def work_out_closest_object(self, objects):
        """ Works out which of the seen objects are closest"""

        smallestDifference = None
        newCoords = []
        returnedObject = None

        for obj in objects:
            # objCoords = obj["coordinates"]
            objCoords = obj.get_coordinates()
            xDiff = abs(self.coordinates[0] - objCoords[0])
            yDiff = abs(self.coordinates[1] - objCoords[1])
            totalDifference = xDiff + yDiff

            if smallestDifference is None or totalDifference < smallestDifference:
                smallestDifference = totalDifference
                newCoords = objCoords
                returnedObject = obj

        return returnedObject
        self.rememberedCoords = newCoords

    def get_edge_coordinates_array(self):
        """Gets the edge coordinates of the circle"""
        edge_coordinates = []
        x = 0
        xCoord = self.coordinates[0]
        yCoord = self.coordinates[1]
        # print(str(self.coordinates))
        while x < 360:
            change = self.angleMath(x, xCoord, yCoord, round(self.width / 2) )
            temp = []
            temp = [xCoord + change[0], yCoord + change[1]]
            edge_coordinates.append(temp)

            x += 1

        return edge_coordinates

    def add_states_to_machine(self):
        """This is where the object will add states to its statemachine"""
        # #print("Adding states to machine")
        for key, value in self.states.items():
            # #print("\ncurrentState " + key)
            # #print("currentValue " + str(value))
            self.stateMachine.add_state(key, value[1], value[0])

    def advance_state_machine(self):
        """
        Advances the statemachine to the next logical step instead of a random one
        :return:
        """

        current_state = self.stateMachine.get_current_state()
        nextState = ""

        if "want" in current_state or "find" in current_state:
            keyword = ""
            if "Drink" in current_state or "Bar" in current_state:
                keyword = "Bar"
            elif "Dance" in current_state:
                keyword = "DanceFloor"
            elif "Toilet" in current_state:
                keyword = "Toilet"

            if "want" in current_state:
                nextState = "find"
            else:
                nextState = "moveTo"

            nextState += keyword
        elif "move" in current_state:
            if "Bar" in current_state:
                nextState = "orderDrink"

            elif "DanceFloor" in current_state:
                nextState = "dance"

            elif "Toilet" in current_state:
                nextState = "useToilet"

        else:
            return self.stateMachine.get_next_state()

        return self.stateMachine.choose_next_state(nextState)



    def clear_vision(self):
        """This method wipes the vison"""
        self.vision = []

    def add_to_vision(self,id):
        """Adds to the vision array if it isn't aready in there"""
        # vision = self.vision
        #variable to see if the id is already in the vision
        already_there = False
        for people in self.vision:
            #Cheacks to see if the person is already in the vision
            if id == people:
                already_there = True
        # if it isnt then it adds it to the array
        if already_there == False:
            self.vision.append(id)


    def add_to_memory(self, obj):
        """Adds an object to the persons memory so they can find it again easier
        :param obj: The obj to add
        """
        key = ""
        if isinstance(obj, Bar):
            key = "Bar"

        elif isinstance(obj, DanceFloor):
            key = "DanceFloor"

        elif isinstance(obj, Toilet):
            key = "Toilet"

        if key == "":
            return False

        if not self.memory[key]:
            self.memory[key].append(obj)
            return True

        if self.check_obj_already_known(obj, key) is None:
            self.memory[key].append(obj)

    def check_obj_already_known(self, obj, key):
        """
        Checks to see if an obj is already remembered
        :param obj: The object to check
        :param key: The object type
        :return: True if it is remembered
        """

        for rememberedObj in self.memory[key]:
            if rememberedObj.get_name() == obj.get_name():
                return True

        return False

    def get_closest_object_from_memory(self, objType):
        """
        Searches the persons memory for the object that they are looking for
        :param objType: The object type they are looking for
        :return: The object or false if none
        """

        if self.memory[objType] is None:
            return False

        return self.work_out_closest_object(self.memory[objType])

    def coords_between_two_points(self, cord1, cord2):
        """This is a funciton the takes 2 coordinates and returns all the cordinates that are between them
        :pram cord1 is the first cordinate
        :pram cord2 is the second
        :retrun is the array of cordinates between the two points
        """
        # Gets the angle of the line
        angleRad =  math.atan2(cord2[1]-cord1[1], cord2[0]-cord1[0])
        # Converts it to degrees
        angleDeg = math.degrees(angleRad)
        # works out the distance between the two cordinates
        distance = math.pow(cord1[0] - cord2[0],2) + math.pow(cord2[1] - cord2[1],2)
        distanceRoot = math.sqrt(distance)
        result = []
        x = 1
        #Goes though each itoration and works out what the cordiante is and adds it to the array
        while x <= distanceRoot:
            lineCoords = self.angleMath(angleDeg,cord1[0],cord1[1],x)
            result.append(lineCoords)
            x = x + 1
        return result

    def personVision(self, x1, y1, angle, vision):
        """This function gets an person and returns an array of the cordinates of their vision
        :pram x1 is the cordinate of the person x cord
        :pram y1 is the cordiate of the person y cord
        :retrun an array of all the cordinates in their vision
        """
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
            # #print(resultArray)
            # #print( )
        return resultArray

    def angleMath(self, angle, xcord, ycord,vision):
        """This is the maths that returns the amount the x and y cordianes need to change to produce the cordinates
        of the new loaction
        :pram angle they are are looking at
        :pram xcord of the person who is direction looking
        :pram ycord of the person who is looking
        :pram vision is the lengh that they can see
        :retrun the amount the orignial coordinate would need to change to create the new one
         """
        # These variables will be chnaged into number to change
        veritcal = 0
        horizontal = 0
        # The math.sin and cos works in radians so this converts the number to radians
        angle1 = math.radians(angle)
        #These 4 if statements do the maths that takes the lengh of their vision, and the angle that they are directionLooking
        # then returns the value that the point would have to change

        if 1 <= angle and angle <= 90:
            veritcal = round(vision * math.sin(math.radians(90) - angle1))
            veritcal = veritcal * -1
            horizontal = round(vision * math.cos(math.radians(90) - angle1))
        if 90 < angle and angle <= 180:
            veritcal = round(vision * math.sin(angle1 - math.radians(90)))
            horizontal = round(vision * math.cos(angle1 - math.radians(90)))
        if 180 < angle and angle <= 270:
            veritcal = round(vision * math.sin(math.radians(270) - angle1))
            horizontal = round(vision * math.cos(math.radians(270) - angle1))
            horizontal = horizontal *-1
        if 270 < angle and angle <=360:
            veritcal = round(vision * math.cos(math.radians(360)- angle1))
            veritcal = veritcal * -1
            horizontal = round(vision * math.sin(math.radians(360) - angle1))
            horizontal = horizontal * -1
        return [veritcal, horizontal]

    def person_eyes(self, cords, angle, radias):
        """Function that returns the cordinates of where the eyes are located
        :pram cords the cordinates of the centre of the persons
        :pram angle the angle that the person is facing
        :pram radias the size of the circle
        :return The cordinates of the eyes
        """

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


    def order_drink(self):
        """Function orders a drink from the remembered object
        :return True on success"""

        if self.rememberedObj.orderDrink(self):
            self.orderedDrink = 1
            return True

        return False

    def has_ordered_drink(self):
        """
        Checks to see if the person has ordered a drink
        :return:
        """
        return self.orderedDrink

    def served_drink(self):
        """
        Bar servers person drink
        :return:
        """
        self.hasDrink = 1
        self.orderedDrink = 0

        self.advance_state_machine()

        return self.set_action_count(5,10)

    def has_drink(self):
        """
        Checks to see if person has a drink
        :return:
        """
        if self.hasDrink:
            return True

        return False

    def drink_drink(self):
        """
        Drinks the drink the person currently has
        :return:
        """

        if self.has_drink():
            self.hasDrink = 0
            return True

        return False

    def use_toilet(self):
        """
        Uses the toilet, maybe adjust the persons needs,
        tells the toilet it is in use
        :return: the action count of how long they are going to be waiting for
        """

        if self.rememberedObj.get_person_using_toilet() == self:
            self.rememberedObj.person_stop_using_toilet(self)
            self.advance_state_machine()

        elif self.rememberedObj.person_use_toilet(self):
            # print("using toilet")
            self.set_action_count(8, 10)



    def set_action_count(self, minRange, maxRange):
        """
        Sets action count to be a random int multipled by the tickRate to mean a number of seconds
        :param minRange: Random number minimum
        :param maxRange: Random number maximum
        :return: No. ticks
        """

        multiplier = randint(minRange, maxRange)

        self.actionCount = multiplier * self.tick_rate
        self.currentActionCount = 0

        # print(self.name + " is waiting for " + str(self.actionCount) + " ticks")
        return self.actionCount

    def clear_action_count(self):
        """Clears the set action count"""
        self.actionCount = None
        self.currentActionCount = None

    def wait_on_action_count(self):
        """Causes the person to wait until the currentActionCount reaches the set actionCount
        Also incremeents the currentActionCount or clear if needs be
        :return: True on waiting"""

        if self.actionCount is None and self.currentActionCount is None:
            return False

        if self.currentActionCount < self.actionCount:
            self.currentActionCount += 1
            return True

        self.clear_action_count()
        return False


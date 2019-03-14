# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018
# Modified by Chris
# from random import seed
from random import randint, seed
# import random
from People.stateMachine import StateMachine
from Objects.baseObject import BaseObject
from Objects.bar import Bar
from Objects.toilet import Toilet
from Objects.danceFloor import DanceFloor
from Algorithm import a_starv2
import math


class Person:
    """Placeholder testing"""
    placeholder = 0
    tick_rate = 0

    flockingDistance = 40

    #Was size but chris has angle and width so using that instead
    angle = 0
    #This is the diameter
    width = 10
    name = ""

    # map is Noneisinstance
    map = 0
    sight = 100
    maxSpeed = 4

    shape = "circle"

    defaultState = "greatestNeed"
    idleState = "greatestNeed"
    # The initial key is the state
    # the first array is the properties from the previous state that they have to be in, not currently used
    # THe second array is the next states, must match another state or its going to break
    states = {
        "greatestNeed": [["usedToilet", "drinkDrink", "danced"], ["wantDrink", "wantToilet", "wantDance"]],

        # "wantSearch": [[], ["search"]],
        # "search": [[], ["greatestNeed"]],


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
            self.flockingDistance = 100 + width
        else:
            self.flockingDistance = 100

        self.stateMachine = StateMachine("person")
        self.add_states_to_machine()

        self.currentState = self.idleState
        self.stateMachine.set_current_state(self.currentState)

        self.starting_value = None
        self.doing_task = False

        self.tick_rate = tick_rate

        # variable declaration
        self.actionCount = None
        self.currentActionCount = None
        # Current coordinates
        # self.coordinates = [0, 1]
        # Last Coordinates, used for flocking
        self.lastCoordinates = []
        #Tracks how many times the person gets stuck to try and get them to go somewhere else
        self.coordinatesFailed = 0
        self.objectFailed = 0
        self.objectFailedCount = 0

        # A flocking parameter, dont want to be within 10 pixels of a nearby object, will attempt to move out of them
        self.rejectionArea = 10
        self.rejectionStrength = 1

        self.vision = []

        # Persons colour for display on map
        self.colour = [255, 0, 0]

        self.rememberedObj = ""
        self.rememberedObjType = ""
        self.rememberedColour = ""
        self.rememberedCoords = []
        self.exploreNode = []

        #To stop something moving more than 4 a go
        self.usedSpeed = 0

        self.astarCoords = []

        self.rotate = 0

        self.headAngle = 0

        self.memory = {
            "Bar": [],
            "DanceFloor": [],
            "Toilet": []
        }

        self.orderedDrink = 0
        self.hasDrink = 0
        # Persons "needs" first value is importance second is how much they want to do it
        self.brain = [["Toilet", randint(0,100)],["Drink", randint(0,100)],["Dance", randint(0,100)]]

        self.random_node = None

        self.inside_dance_floor = False
        self.random_dance_area = None

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]

    def action(self):
        """What the person is going to do"""
        self.currentState = self.stateMachine.get_current_state()
        self.usedSpeed = 0


        if self.wait_on_action_count():
            return "Waiting"
        # print(" My current state " + self.currentState)
        stateAction = self.get_state_action()
        if stateAction == "navigateToRememberedObj":
            self.navigate_to_remembered_object()

        elif stateAction == "rotate":
             self.person_rotate()

        elif stateAction == "wait":
            # The person sits there and waits
            nothing = None

        elif stateAction == "explore":
            # Person will pick a random node and navigate to it
            self.setup_explore()

            self.navigate_to_remembered_object()

        # elif stateAction == "dance":
        #     if self.inside_dance_floor:
        #         self.advance_state_machine()
        #     self.astarCoords.clear()

        else:
            # self.random_move()
            self.flock()
        # return self.random_move()

    def navigate_to_remembered_object(self):
        """
        Starts to move to the remembered Object
        :return: True on success
        """

        print("my state is" + str(self.currentState))
        # Hopefully this will allow someone to flock around objects in front of them, whilst navigiating to the remembered object
        objectsWithinRejection = self.map.get_objects_within_range(self.coordinates, self.get_rejection_area(), self.get_edge_coordinates_array(self.coordinates, self.get_rejection_area()), self)

        if objectsWithinRejection and self.rememberedObj not in objectsWithinRejection:
            # Sam - Keeping the flocking in but not allowing it to move two blocks to its destination
            self.flock_away_from_objects(objectsWithinRejection)
            # return self.flock_away_from_objects(objectsWithinRejection)

        targetCoordinates = None
        if self.rememberedObj:
            targetCoordinates = self.work_out_objects_closest_point(self.rememberedObj)
        else:
            targetCoordinates = self.exploreNode

        targetDistance = self.map.calculate_distance_between_two_points(self.coordinates, targetCoordinates)
        x = self.coordinates[0]
        y = self.coordinates[1]
        nextMove = [x, y]

        # if not self.astarCoords:
        if self.astarCoords == []  or not self.astarCoords:
            self.set_cords_from_algo()

        if self.astarCoords and (targetDistance > (self.get_rejection_area() / 2) or self.object_in_vision(self.rememberedObj) is True and self.count_objects_in_vision(False) > 1):
            print("THIS IS TRUE AND IM NAVIGATING HERE")
            print(str(self.astarCoords))
            self.navigate_via_astar(nextMove)
        else:
            if targetCoordinates != nextMove:
                # while targetCoordinates != nextMove:
                x = self.coordinates[0]
                y = self.coordinates[1]

                if targetCoordinates[0] > x:
                    if targetCoordinates[0] > x + 2 and self.usedSpeed == 0:
                        x += 2
                    else:
                        x += 1

                elif targetCoordinates[0] < x:
                    if targetCoordinates[0] < x - 2 and self.usedSpeed == 0:
                        x -= 2
                    else:
                        x -= 1

                if targetCoordinates[1] > y:
                    if targetCoordinates[1] > y + 2 and self.usedSpeed == 0:
                        y += 2
                    else:
                        y += 1
                elif targetCoordinates[1] < y:
                    if targetCoordinates[1] < y - 2 and self.usedSpeed == 0:
                        y -= 2
                    else:
                        y -= 1

                nextMove = [x, y]
                moveReturn = self.move(nextMove)
                # if moveReturn is not True:
                #     newCoords = self.get_coordinates_for_move_avoiding_collision_object(targetCoordinates, moveReturn, nextMove)

    def navigate_via_astar(self, nextMove):
        """
        :return: True on success
        """
        targetCoordinates = [self.astarCoords[0][0], self.astarCoords[0][1]]
        # First move
        # Sam - Think this being in while was partially responsible for the big jumps changed to if
        # if targetCoordinates != nextMove:
        if True:
            # while targetCoordinates != nextMove:
            x = self.coordinates[0]
            y = self.coordinates[1]

            if targetCoordinates[0] > x:
                if targetCoordinates[0] > x + 1 and self.usedSpeed == 0:
                    x += 2
                else:
                    x += 1

            elif targetCoordinates[0] < x:
                if targetCoordinates[0] < x - 1 and self.usedSpeed == 0:
                    x -= 2
                else:
                    x -= 1

            if targetCoordinates[1] > y:
                if targetCoordinates[1] > y + 1 and self.usedSpeed == 0:
                    y += 2
                else:
                    y += 1
            elif targetCoordinates[1] < y:
                if targetCoordinates[1] < y - 1 and self.usedSpeed == 0:
                    y -= 2
                else:
                    y -= 1

            nextMove = [x, y]
            moveReturn = self.move(nextMove)
            if moveReturn is not True and moveReturn != self.rememberedObj and moveReturn != False:
                newCoords = self.get_coordinates_for_move_avoiding_collision_object(targetCoordinates, moveReturn, nextMove)
                self.move(newCoords)
                # return self.move(nextMove)
        x1, y1 = self.coordinates
        x2, y2 = self.astarCoords[0]
        x_distance = abs(x2 - x1)
        y_distance = abs(y2 - y1)
        distance = (x_distance * x_distance) + (y_distance * y_distance)
        distance = math.sqrt(distance)
        if distance < self.width + self.width * 0.3:
            self.astarCoords.pop(0)
            if len(self.astarCoords) == 0:
                self.clear_explore_node()

    def setup_explore(self):
        """
        Sets Explore node if exists
        Changes Explore Node if it has multiple collisions with the same object
        Needs to be used in conjunction with navigate_to_remembered_object
        :return:
        """
        # Failed to explore a certain way a number of times moving back
        if self.coordinatesFailed == 5 or self.objectFailedCount == 5:
            # Could have gone off the map or something is going wrong, try to go somewhere else instead
            self.coordinatesFailed = 0
            self.objectFailed = 0
            self.objectFailedCount = 0
            self.clear_explore_node()

        if len(self.exploreNode) == 2:
            if self.exploreNode[0] == self.coordinates[0] and self.exploreNode[1] == self.coordinates[1]:
                self.clear_explore_node()

        # if self.rememberedObjType != "" and (not self.exploreNode or self.exploreNode is None):
        if not self.exploreNode or self.exploreNode is None:
            # if self.rememberedObjType != "" and self.exploreNode == []:
            self.exploreNode = a_starv2.get_random_waypoint()
            self.astarCoords = a_starv2.run_astar(self.find_nearest_waypoint(), self.exploreNode)

    def get_coordinates_for_move_avoiding_collision_object(self, targetCoordinates,  collisionObject, attemptedMove):
        """
        Try to move to an object avoiding an object
        :param targetCoordinates: The coordinates to move too
        :param collisionObject: The object to avoid
        :return: The coordinates to move to
        """
        newMove = [0, 0]
        newMove[0] = attemptedMove[0]
        newMove[1] = attemptedMove[1]
        collisionCoordinates = collisionObject.get_coordinates()

        if collisionCoordinates[0] != self.coordinates[0]:
            if collisionCoordinates[0] >= self.coordinates[0]:
                newMove[0] = newMove[0] - 1
            else:
                newMove[0] = newMove[0] + 1

            moveResult = self.move(newMove)

            if moveResult != True:
                newMove[0] = attemptedMove[0]

        if collisionCoordinates[1] != self.coordinates[1]:
            if collisionCoordinates[1] >= self.coordinates[1]:
                newMove[1] = newMove[1] - 1
            else:
                newMove[1] = newMove[1] + 1
            self.move(newMove)

        return newMove

    def move(self, coordinates):
        """
        Moves to a given set of coordinates, also makes sure the move isnt too far
        :param coordinates:
        :return: True on successful move, returns the collision object on false
        """
        collisionObject = self.map.check_coordinates_for_person(coordinates, self.width / 2, self.name, self.get_edge_coordinates_array(coordinates, round(self.width / 2) ))
        # if abs(self.coordinates[0] - coordinates[0]) > self.maxSpeed or abs(self.coordinates[1] - coordinates[1]) > self.maxSpeed:
        if abs(self.coordinates[0] - coordinates[0]) > 2 or abs(self.coordinates[1] - coordinates[1]) > 2:
            self.coordinatesFailed += 1
            return False

        # if self.map.check_coordinates_for_person(coordinates, self.width, self.name, self.get_edge_coordinates_array()):
        if collisionObject is True:

            self.change_angle_to_move_direction(self.coordinates, coordinates)
            self.lastCoordinates = self.coordinates
            self.coordinates = coordinates
            self.coordinatesFailed = 0

            return True

        print("person not moving because of " + str(collisionObject))

        if self.rememberedObj != "":
            self.check_person_collided_with_target(collisionObject)

        self.coordinatesFailed += 1
        if self.objectFailed == collisionObject:
            self.objectFailedCount += 1
            print("THIS IS OCCURING")
            # Phil - Put this here as a test of b-line. Ignore if not neccesary in future commits
            print("Navigate still")
            # self.navigate_to_remembered_object()
        else:
            self.objectFailed = collisionObject
            self.objectFailedCount = 1

        return collisionObject


    def person_rotate(self, clockwise = True):
        """
        Rotates the person so there vision goes full circle, going to do by 30 degrees
        :param clockwise: says whether or not to go clockwise or counter clockwise
        :return: Returns the new angle
        """
        if clockwise:
            angleResult = self.angle + 30
        else:
            angleResult = self.angle - 30

        if angleResult > 360:
            angleResult = angleResult - 360

        elif angleResult < 0:
            angleResult = 360 - angleResult

        self.angle = angleResult
        self.rotate += 1


        return angleResult

    def change_angle_to_move_direction(self, oldCoords, newCoords):
        """
        Changes the persons angle so they move in the direction they're looking
        Based on this: https://math.stackexchange.com/questions/707673/find-angle-in-degrees-from-one-point-to-another-in-2d-space
        :param oldCoords: The old/current coordinates
        :param newCoords: The new ones youre moving to that you want to set the angle to face
        :return: The new angle
        """

        newAngle = self.get_angle_between_coords(oldCoords, newCoords)
        if newAngle is not False:
            self.angle = newAngle
        return self.angle

    def get_angle_between_coords(self, oldCoords, newCoords):
        """Gets the angle between a pair of coordinatse
        0 degrees is up
        :param oldCoords: The old/current coordinates
        :param newCoords: The new ones youre moving to that you want to set the angle to face
        """
        if oldCoords[0] == newCoords[0] and oldCoords[1] == newCoords[1]:
            return False

        degrees = 0
        # yDiff = 0
        yDiff = (0 - newCoords[1]) - (0 - oldCoords[1] )
        xDiff = newCoords[0] - oldCoords[0]


        # yDiff =  oldCoords[1] - newCoords[1]
        # xDiff = oldCoords[1] - newCoords[0]
        if xDiff != 0 and yDiff != 0:
            # slopeOfLine = (newCoords[1] - oldCoords[1]) / (newCoords[0] - oldCoords[0])
            slopeOfLine = yDiff / xDiff
            # radians = math.atan(slopeOfLine)
            radians = math.atan2(yDiff, xDiff)
            degrees = math.degrees(radians)

            degrees += 180

            if degrees < 0:
                degrees += 360

            elif degrees > 360:
                degrees = degrees - 360
                # degrees = 360 - degrees

        else:
            if xDiff != 0:
                if newCoords[0] > oldCoords[0]:
                    degrees = 180

                else:
                    degrees = 0

            else:
                if newCoords[1] > oldCoords[1]:
                    degrees = 90

                else:
                    degrees = 270
        return degrees


    def random_move(self):
        """Person moving randomly around the map"""
        randomNumber = randint(0, 8)
        newCoordinates = []
        if randomNumber <= 2:  # person move up
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]

        elif randomNumber <= 4:  # Person move down
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]

        elif randomNumber <= 6:  # person move right
            newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]

        elif randomNumber <= 8:  # Person move left
            newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]


        self.move(newCoordinates)

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

    def get_rejection_area(self):
        """Returns the area that a person doesnt want other objects in"""
        radius = self.width / 2
        return radius + self.rejectionArea

    def get_rejection_strength(self):
        """Reutrns the rejectionStrength"""
        return self.rejectionStrength

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
        action = "moveRandom"

        """NEED TO CHECK HERE FOR NEEDS"""
        """IF STATE IS GREATEST NEED"""
        print("CURRENT STATE IS: ")
        print(self.currentState)
        if self.currentState == self.idleState:
            """While there are no current needs, the person will relax."""
            """relax will reduce the needs of the person"""
            self.clear_remembered_object()
            if self.check_needs() == False:
                self.relax()
                """RETURN THE ACTION OF DOING NOTHING, THERE IS NO NEED"""
                print("WHEN AM I HERE?")
                print(action)
                return action
            """Setting the current state to the persons needs."""
            print("Currently here within the get_state_action")
            self.currentState = self.stateMachine.get_need_state(self.check_needs())
            print(self.currentState)

        if "want" in str(self.currentState):
            # Person has a want desire
            if self.want_action(self.currentState):
                action = "navigateToRememberedObj"
                self.rotate = 0
                self.advance_state_machine()

            else:
                action = "rotate"

        elif "find" in str(self.currentState):
            # Person trying to find an object
            action = self.find_action()

        elif "move" in str(self.currentState):
            # Person moving to object
            action = "navigateToRememberedObj"
            rememberedObjectCoords = 0
            objectClosestPoint = -1
            if self.object_in_vision(self.rememberedObj):
                objectClosestPoint = self.work_out_objects_closest_point(self.rememberedObj)

            rememberedObjectCoords = self.rememberedObj.get_coordinates()

            objectSize = [self.rememberedObj.get_width(), self.rememberedObj.get_height()]
            rectangleCoordRanges = self.map.get_coordinates_range(rememberedObjectCoords, objectSize)
            selfEdge = self.get_edge_coordinates_array(self.coordinates, round(self.width / 2))

            # if self.map.check_circle_overlap_rectangle(selfEdge, rectangleCoordRanges):
            if self.map.check_person_touching_object(selfEdge, rectangleCoordRanges):
                self.astarCoords = []
                self.advance_state_machine()
                self.change_angle_to_move_direction(self.coordinates, self.rememberedObj.get_coordinates())

        elif self.currentState == "orderDrink":
            # Person is ordering their drink
            action = "wait"
            if self.has_ordered_drink() == 0 and self.has_drink() is False:
                self.order_drink()
                self.brain[1][1] = 100
                self.clear_remembered_object()

            elif self.has_drink():
                """PHIL - Adding this change in"""
                self.advance_state_machine()


        elif self.currentState == "drink":
            # Person drinks their drink
            self.drink_drink()
            self.advance_state_machine()

        elif self.currentState == "dance":
            # Person will dance
            # self.stateMachine.get_next_state()

            action = "dance"
            self.move_inside_dance_floor()
            if self.inside_dance_floor:
                self.dance()
                """PHIL STUFF HERE"""
                if self.check_needs() is not False:
                    self.advance_state_machine()

        elif self.currentState == "useToilet":

            action = "wait"
            self.use_toilet()
                # Toilet is free and now you are using it
            # self.clear_remembered_object()

        return action

    def find_action(self):
        """
        Does the find action for get_state_action
        :return: String of action
        """
        action = "moveRandom"
        if self.find_object(self.rememberedObjType):
            action = "navigateToRememberedObj"
            self.rotate = 0
            print("found object " + str(self.currentState))
            self.advance_state_machine()
            print("new state " + self.currentState)

            if self.astarCoords or self.exploreNode:
                self.clear_explore_node()
        else:
            # Cant find object do a circle to see it
            if self.rotate < 12:
                action = "rotate"
            else:
                action = "explore"
                # self.set_explore_node()
                #if at target dont do the rest

        return action


    def want_action(self, wantState):
        """The people want to do something"""
        if wantState == "wantDrink":
            searchObject = "Bar"

        elif wantState == "wantDance":
            searchObject = "DanceFloor"

        else:
            searchObject = "Toilet"

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


    def get_edge_coordinates_array(self, coordinates, width):
        """Gets the edge coordinates of the circle"""
        edge_coordinates = []
        x = 0
        # xCoord = self.coordinates[0]
        # yCoord = self.coordinates[1]
        xCoord = coordinates[0]
        yCoord = coordinates[1]
        while x < 360:
            change = self.angleMath(x, xCoord, yCoord, width)
            temp = []
            temp = [xCoord + change[0], yCoord + change[1]]
            edge_coordinates.append(temp)

            x += 1

        return edge_coordinates

    def add_states_to_machine(self):
        """This is where the object will add states to its statemachine"""
        for key, value in self.states.items():
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

        nextState = self.stateMachine.choose_next_state(nextState)

        if nextState is not False:
            self.currentState = nextState
            return nextState

        return False
        # return self.stateMachine.choose_next_state(nextState)



    def clear_vision(self):
        """This method wipes the vison"""
        self.vision = []

    def add_to_vision(self, obj):
        """Adds to the vision array if it isn't aready in there"""
        # vision = self.vision
        #variable to see if the id is already in the vision
        already_there = False

        if self.object_in_vision(obj) is False:
            self.vision.append(obj)

        # for people in self.vision:
        #     #Cheacks to see if the person is already in the vision
        #     if obj == people:
        #         already_there = True
        # # if it isnt then it adds it to the array
        # if already_there == False:
        #     self.vision.append(obj)

    def object_in_vision(self, searchObj):
        """
        Checks to see if an object can be seen by the person
        :param obj: The obj in question
        :return: True if it exists
        """

        for obj in self.vision:
            if searchObj == obj:
                return True

        return False

    def count_objects_in_vision(self, includePeople):
        """
        Counts objects in vision
        :param includePeople: will count people as well if true
        :return: Number of objects
        """
        if includePeople is True:
            return len(self.vision)

        objCount = 0

        for obj in self.vision:
            if isinstance(obj, BaseObject):
                objCount += 1

        return objCount


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
        rays = 9
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
            tempArray = []

            # increases the angles by 5 each intoration
            angle = originalAngle + (i * 5)
            # this is an if statement that stops the number being more than 360 and less than 0
            if angle > 360:
                angle = angle - 360
            # this then produces the cordiantes for each line and adds them to the array
            while vision >= x:
                value = self.angleMath(angle,x1,y1,x)
                value = [x1 + value[0], y1 + value[1]]
                # resultArray.append(value)
                tempArray.append(value)
                x = x + 3
            i = i + 1
            x = 12
            resultArray.append(tempArray)

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
        #Update drink meter
        self.incriment_need(1, 1)
        self.astarCoords.clear()

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

    def dance(self):
        """
        Agent has reached an area on the dancefloor and is now dancing.
        :return:
        """
        self.incriment_need(2,1)
        self.incriment_need(1,-1)
        self.incriment_need(0,-1)
        self.set_action_count(5, 10)
        # self.clear_remembered_object()

    def use_toilet(self):
        """
        Uses the toilet, maybe adjust the persons needs,
        tells the toilet it is in use
        :return: the action count of how long they are going to be waiting for
        """

        if self.rememberedObj.check_person_using_toilet(self) is True:
            self.get_person_needs()
            """Phil- Added this as a placeholder"""
            self.brain[0][1] = 100

            self.rememberedObj.person_stop_using_toilet(self)
            self.advance_state_machine()
            self.clear_remembered_object()

        elif self.rememberedObj.person_use_toilet(self):
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

        # self.actionCount = 1

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

    """gets the cord from the a* and returns the cords needed"""
    def set_cords_from_algo(self):

        """If the current cords are the nearest node"""
        startingLoc = self.coordinates
        if self.find_nearest_waypoint() != self.coordinates:
            startingLoc = self.find_nearest_waypoint()
        """NEED TO ADD THE DESTINATION OF REQUIRED OBJECT"""
        # Sam - Trying to change it to use startingLoc as its making a huge jump as it goes to the node
        locations = None

        if self.rememberedObj:
            print("THERE IS A REMEMBERED OBJECT AND THAT IS" + str(self.rememberedObj))
            targetCoordinates = self.work_out_objects_closest_point(self.rememberedObj)
            print("Target coords for the remembered object is: " + str(targetCoordinates))
            locations = a_starv2.run_astar(startingLoc, targetCoordinates)
        else:
            locations = a_starv2.run_astar(startingLoc, self.exploreNode)

        if not locations:
            print("No locations found")
            return False
        else:
            for location in locations:
                self.store_waypoints(location)

    def store_waypoints(self, cord):
        """Stores the waypoints in cords var"""
        try:
            self.astarCoords.append([cord[0], cord[1]])
        except:
            print("no astar coords")



    def find_nearest_waypoint(self):
        cords = []
        open = a_starv2.get_open_nodes()
        currentX = self.coordinates[0]
        currentY = self.coordinates[1]
        notFound = True
        currentX = int(20 * round(float(currentX / 20)))
        currentY = int(20 * round(float(currentY / 20)))
        cords.append(currentX)
        cords.append(currentY)
        return cords

    #FLOCKING STUFF FML

    def flock(self):
        """
        Person flocks with others
        Going to want an average angle of nearby people and average move direction
        :return:
        """
        nearbyPeople = self.map.get_people_within_range(self.coordinates, self.flockingDistance, self)

        objectsWithinRejection = self.map.get_objects_within_range(self.coordinates, self.get_rejection_area(), self.get_edge_coordinates_array(self.coordinates, self.get_rejection_area()), self)

        if objectsWithinRejection:
            return self.flock_away_from_objects(objectsWithinRejection)


        if nearbyPeople is False or len(nearbyPeople) == 1:
            # No nearby people random
            self.setup_explore()
            return self.navigate_to_remembered_object()
            # return self.random_move()

        angleTotal = 0
        # These are the directions people are moving on the axis
        xDirection = {
            "positive": 0,
            "negative": 0
        }
        yDirection = {
            "positive": 0,
            "negative": 0
        }


        for person in nearbyPeople:
            if person == self:
                # This is a reference to itself
                continue

            flockingParameters = person.get_flocking_parameters()

            angleTotal += flockingParameters["angle"]

            if flockingParameters["direction"] is not False:
                # Finding most common movement direction
                if flockingParameters["direction"][0] > 0:
                    xDirection["positive"] += 1

                elif flockingParameters["direction"][0] < 0:
                    xDirection["negative"] += 1

                if flockingParameters["direction"][1] > 0:
                    xDirection["positive"] += 1

                elif flockingParameters["direction"][1] < 0:
                    xDirection["negative"] += 1

        avgAngle = angleTotal / (len(nearbyPeople) - 1)
        self.flock_move(avgAngle, xDirection, yDirection)

    def flock_away_from_objects(self, objects):
        """
        Flocks away from the array of objects
        :param objects: Objects to avoid
        :return: true on success
        """
        coordsToAvoid = self.coordinates_to_avoid_of_nearby_objects(objects)

        priorityCoordiantes = self.priority_avoid_coordinates(objects, coordsToAvoid)

        # coordsToAvoid[100]
        nextMove = []
        nextMove.append(self.coordinates[0])
        nextMove.append(self.coordinates[1])
        moveX = 0
        moveY = 0


        for coord in priorityCoordiantes:
            if coord[0] > self.coordinates[0]:
                moveX -= 1
            elif coord[0] < self.coordinates[0]:
                moveX += 1

            if coord[1] > self.coordinates[1]:
                moveY -= 1
            elif coord[1] < self.coordinates[1]:
                moveY += 1

        randInc = randint(0, 8)
        if randInc == 0:
            moveX += 1
        elif randInc == 1:
            moveX -= 1
        elif randInc == 2:
            moveY += 1
        elif randInc == 3:
            moveY -= 1


        if moveX > 0:
            nextMove[0] += 1
        elif moveX < 0:
            nextMove[0] -= 1

        if moveY > 0:
            nextMove[1] += 1
        elif moveY < 0:
            nextMove[1] -= 1

        if self.move(nextMove) is True:
            # So that it can navigate away from objects that come to close but still attempt to move to its destination
            self.usedSpeed += 1
            return True

    def priority_avoid_coordinates(self, objects, coordinates):
        """
        The coordinates to avoid as a priority
        :param objects:
        :param coordinates:
        :return:
        """
        closest = []
        priorityDiff = 0
        rejectionScore = 0

        x = 0
        # for key, obj in enumerate(objects):
        for obj in objects:
            if obj == self:
                continue
            # Finding closest and moving away from that
            coords = coordinates[x]
            coordsDiff = (abs(coords[0] - self.coordinates[0]) + abs(coords[1] - self.coordinates[1]))
            if obj.get_rejection_strength() > rejectionScore:
                rejectionScore = obj.get_rejection_strength()
                closest = []
                closest.append(coordinates[x])
                priorityDiff = coordsDiff

            elif obj.get_rejection_strength() == rejectionScore and priorityDiff == coordinates:

                closest.append(coordinates[x])

            x += 1

        return closest


    def coordinates_to_avoid_of_nearby_objects(self, objects):
        """
        Works out the direction to move to to get away from nearby objects
        :param objects: The objects too close
        :return:
        """

        coordsToAvoid = []

        for obj in objects:
            if obj == self:
                continue

            if isinstance(obj, Person):
                coordsToAvoid.append(obj.get_coordinates())

            else:
                coordsToAvoid.append(self.work_out_objects_closest_point(obj))

        return coordsToAvoid

    def work_out_objects_closest_point(self, obj):
        """
        Work out the coordinate of an objects closest point
        :param obj: the object in question
        :return: a set of coordinates
        """
        ranges = self.map.get_coordinates_range(obj.get_coordinates(), [obj.get_width(), obj.get_height()])

        closestX = self.find_closest_coordinate(self.coordinates[0], ranges["X"][0], ranges["X"][1])
        closestY = self.find_closest_coordinate(self.coordinates[0], ranges["Y"][0], ranges["Y"][1])

        return [closestX, closestY]

    def find_closest_coordinate(self, myCoord, lowCoord, highCoord):
        """
        Roughly tries to find the closest coordinate
        :param myCoord: My coordinate an x or y value that you want to compare it to
        :param lowCoord: the low range of that x or y
        :param highCoord: the high range value of that x or y
        :return: an int
        """
        returnCoord = 0
        if myCoord <= lowCoord:
            returnCoord = lowCoord

        elif myCoord >= highCoord:
            returnCoord = highCoord

        else:
            returnCoord = myCoord

        return returnCoord

    def flock_move(self, avgAngle, xDirection, yDirection):
        """
        Move in a direction based on the x and y direciton
        :param avgAngle:
        :param xDirection:
        :param yDirection:
        :return:
        """

        newCoordinates = [self.coordinates[0], self.coordinates[1]]

        if xDirection["positive"] > xDirection["negative"]:
            newCoordinates[0] += 1
        elif xDirection["positive"] < xDirection["negative"]:
            newCoordinates[0] -= 1

        if yDirection["positive"] > yDirection["negative"]:
            newCoordinates[1] += 1
        elif yDirection["positive"] < yDirection["negative"]:
            newCoordinates[1] -= 1

        moveReturn = self.move(newCoordinates)
        if moveReturn is True:
            self.angle = avgAngle
        else:
            self.random_move()
        # Needs a way of handling a collision

    def get_flocking_parameters(self):
        """
        Gets the parameters for another object to flock with this one with
        Source: http://harry.me/blog/2011/02/17/neat-algorithms-flocking/
        Not using velocity yet as currently it only moves one space at a time
        :return: A list of angle and move direction
        """

        returnList  = {
            "angle" : self.angle,
            "direction" : self.calculate_move_direction_difference()
        }

        return returnList

    def calculate_move_direction_difference(self):
        """
        Works out the X,Y difference from the old coordiantes to the current ones
        :return:
        """

        try:
            xDiff = self.coordinates[0] - self.lastCoordinates[0]
            yDiff = self.coordinates[1] - self.lastCoordinates[1]
        except:
            return False
        return [xDiff, yDiff]

    def get_memory(self):
        return self.memory

    """Returns array of persons current needs, alone with value"""
    def get_person_needs(self):
        return self.brain

    """This will be in an idle state when a person has no desire of drinking, dancing or wanting the toilet"""
    def relax(self):
        for i in range(len(self.brain)):
            self.incriment_need(i,-1)

    def set_random_dance_area(self):
        if self.random_dance_area is None:
            self.random_dance_area = self.rememberedObj.get_random_dance_area()
        else:
            return

    def get_random_dance_area(self):
        return self.random_dance_area
    """
    This function checks the needs of the person.
    If the value goes below the limit, it'll return that need, otherwise False
    """

    def move_inside_dance_floor(self):
        """Person moves to a random location on the dancefloor
        Currently broken as it only moves one cord, not the full destination.
        """
        randomNumber = randint(0, 8)
        nextMove = self.coordinates
        self.set_random_dance_area()
        if self.random_dance_area != self.coordinates:
            # while targetCoordinates != nextMove:
            x = self.coordinates[0]
            y = self.coordinates[1]

            if self.random_dance_area[0] > x:
                if self.random_dance_area[0] > x + 1:
                    x += 2
                else:
                    x += 1

            elif self.random_dance_area[0] < x:
                if self.random_dance_area[0] < x - 1:
                    x -= 2
                else:
                    x -= 1

            if self.random_dance_area[1] > y:
                if self.random_dance_area[1] > y + 1:
                    y += 2
                else:
                    y += 1
            elif self.random_dance_area[1] < y:
                if self.random_dance_area[1] < y - 1:
                    y -= 2
                else:
                    y -= 1

            nextMove = [x, y]
            moveReturn = self.move(nextMove)
            if moveReturn is not True:
                newCoords = self.get_coordinates_for_move_avoiding_collision_object(self.random_dance_area, moveReturn, nextMove)
                self.move(newCoords)
                # return self.move(nextMove)

        if self.coordinates == self.random_dance_area:
            """DELAY here?"""
            self.random_dance_area = None
            self.inside_dance_floor = True

    def check_needs(self):
        """
        This function checks the needs of the person.
        If the value goes below the limit, it'll return that need, otherwise False
        """
        for b in self.brain:
            if b[1] <= 1:
                return b[0]
        return False

    def clear_explore_node(self):
        """
        Functions clears explore node, just so we have a clear view of where it happens
        :return:
        """

        self.exploreNode = []
        self.astarCoords = []


    def check_astar_cords_is_empty(self):
        if self.astarCoords is None:
            return True
        else:
            return False

    def set_needs_values(self, index, value):
        array = self.brain
        array[index][1] = value

    def check_person_collided_with_target(self, collisionObj):

        if collisionObj == self.rememberedObj or type(collisionObj) is type(self.rememberedObj) is True:
            # Found your way there goon, do your thing
            self.advance_state_machine()
            return True

        return False

    def incriment_need(self, index, value_of_incriment):
        needs = self.brain
        current_value = needs[index][1]
        current_value = (current_value + value_of_incriment)
        if current_value > 100:
            current_value = 100
        if current_value < 0:
            current_value = 0
        needs[index][1] = current_value

    def probility_choice_need(self):
        """
        This function takes all the needs and selects one based on the probibility of it being needed
        :return:
        """
        needs = self.brain
        toilet = 100 - needs[0][1]
        if toilet == 0:
            toilet = 1
        drink = 100 - needs[1][1]
        if drink == 0:
            drink = 1
        dance = 100 - needs[2][1]
        if dance == 0:
            dance = 1
        sum_of_needs = toilet + drink + dance
        prob_toilet = (toilet / sum_of_needs) * 100
        prob_drink = (drink / sum_of_needs) * 100
        prob_dance = (dance / sum_of_needs) * 100
        rand_num = randint(0,100)
        if prob_toilet > rand_num:
            return needs[0]
        elif prob_toilet + prob_drink > rand_num:
            return needs[1]
        elif prob_drink + prob_toilet + prob_dance > rand_num:
            return needs[2]
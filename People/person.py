# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018
from random import randint
from People.stateMachine import StateMachine
from Objects.bar import Bar
from Objects.toilet import Toilet
from Objects.danceFloor import DanceFloor

class Person:
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
    rememberedColour = ""
    rememberedCoords = []

    headAngle = 0

    memory = {
        "Bar" : [],
        "DanceFloor" : [],
        "Toilet" : []
    }

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
        "findToilet": [["notAtToilet"], ["moveToilet"]],
        "moveToilet": [["foundToilet", "notFoundToilet"], ["moveToilet", "useToilet"]],
        "useToilet": [["atToilet"], ["greatestNeed"]],
    }
    # gender = "" Use this one to determine which bathroom, later

    def __init__(self, name, coords, width, angle):
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
        # print(self.stateMachine.get_states())

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]

    def action(self):
        """What the person is going to do"""
        print("action() Current state " + str(self.currentState))

        # return self.random_move()

        stateAction = self.get_state_action()

        if stateAction == "navigateToRememberedObj":
             print("action")
             self.move()

        elif stateAction == "":
             print("no action")
        else:
            self.random_move()
        return self.random_move()

    def navigate_to_remembered_object(self):
        """
        Starts to move to the rememberd Object
        :return: True on success
        """

        nextMove = []
        
        #First move

        # PHILS A* STUFF


        self.move(nextMove)


    def move(self, coordinates):
        """
        Moves to a given set of coordinates
        :param coordinates:
        :return: True on successful move
        """

        if self.map.check_coordinates_for_person(coordinates, self.width, self.name, self.get_edge_coordinates_array()):
            self.coordinates = coordinates
            return True

        return False

    def random_move(self):
        """Person moving randomly around the map"""

        randomNumber = randint(0, 10)
        # print(self.name + " should move " + str(randomNumber))
        newCoordinates = 0
        # print(self.name + " random number " + str(randomNumber) + " -- initial coords " + str(self.coordinates))
        if randomNumber <= 2: #person move up
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]

        elif randomNumber <= 4: #Person move down
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]

        elif randomNumber <= 6: #person move right
            newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]

        elif randomNumber <= 8: #Person move left
            newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]

        # PERSON NEEDS TO SEE IF THERE IS SOMETHING OCCUPING THIS SPACE
        # ADD THAT IN
        if isinstance(newCoordinates, list):
            edgeCoordinates = self.get_edge_coordinates_array()

            if self.map.check_coordinates_for_person(newCoordinates, self.width, self.name, edgeCoordinates):
                self.coordinates = newCoordinates


        # randomNumber = randint(0, 10)
        # # print(self.name + " should move " + str(randomNumber))
        # newCoordinates = 0
        # print(self.name + " random number " + str(randomNumber) + " -- initial coords " + str(self.coordinates))
        # if randomNumber <= 2: #person move up
        #     newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]
        #
        # elif randomNumber <= 4: #Person move down
        #     newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]
        #
        # elif randomNumber <= 6: #person move right
        #     newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]
        #
        # elif randomNumber <= 8: #Person move left
        #     newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]
        #
        # # if randomNumber is <=10 then person has chosen to stay
        #
        # # if newCoordinates is not None:
        # if isinstance(newCoordinates, list):
        #     if self.map.check_coordinates(newCoordinates):
        #         self.map.add_to_map(self, newCoordinates)
        #         self.map.remove_from_map(self.coordinates)
        #         self.coordinates = newCoordinates
        #
        # # print(self.name + " at coordinates " + str(self.coordinates))
        # return self.coordinates;

    def get_edge_coordinates_array(self):
        """Gets the edge coordinates of the circle"""
        edge_coordinates = []
        x = 0
        xCoord = self.coordinates[0]
        yCoord = self.coordinates[1]

        while x < 360:
            coord = self.map.angleMath(x, xCoord, yCoord, self.width)
            edge_coordinates.append(coord)

            x += 1

        return edge_coordinates

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
        print("get state action " + str(self.currentState))

        action = "moveRandom"

        if self.currentState == self.defaultState:
            print(self.name + " in greatest need")
            self.currentState = self.stateMachine.get_next_state()
        else:
            print("not greatest need")

        if "want" in str(self.currentState):
            print("here")
            # Person has a want desire
            if self.want_action(self.currentState):
                action = "navigateToRememberedObj"

        elif "find" in str(self.currentState):
            # Person trying to find an object
            print(self.name + " finding object")
            if self.find_object(self.rememberedObj):
                action = "navigateToRememberedObj"

        elif "move" in str(self.currentState):
            # Person moving to object
            print(self.name + " Person moving to object")
            action = "navigateToRememberedObj"

        elif self.currentState == "orderDrink":
            # Person is ordering their drink
            print(self.name + " Ordering a drink")

        elif self.currentState == "dance":
            # Person will dance
            print(self.name + " is dancing")
            self.stateMachine.get_next_state()

        return action

    def want_action(self, wantState):
        """The people want to do something"""
        if wantState == "wantDrink":
            print("wantDrink")
            searchObject = "Bar"

        elif wantState == "wantDance":
            print("want dance")
            searchObject = "DanceFloor"

        else:
            print("want Toilet")
            searchObject = "Toilet"

        print("Search object " + searchObject)
        self.rememberedObj = searchObject

        return self.find_object(searchObject)

    def find_object(self, searchObject):
        """This function does the find function of a person
        :param searchObject: The object you want to look for
        :return Returns True if there are objects, false if it cant find one
        """

        closestObj = self.get_closest_object_from_memory(searchObject)

        returnString = ""

        if closestObj is False or closestObj is None:
            returnString = "randomMove"
        else:
            self.rememberedObj = closestObj
            self.rememberedCoords = closestObj.get_coordinates()
            self.rememberedColour = closestObj.get_colour()

        

        # # objects = self.map.get_objects_in_range(searchObject, self.coordinates, self.sight)
        # 
        # colourCode = self.map.get_object_colour_code(searchObject)
        # print("object colour code : " + str(colourCode))
        # objects = self.map.person_look_for_object(self.coordinates, self.angle, self.vision, colourCode)
        # 
        # print("find_object objects " + str(objects))
        # 
        # return False
        # if not objects:
        #     # This is when there are no objects in range and you want the person to wander to keep looking
        #     print("no objects in range")
        #     self.rememberedCoords = "search"
        #     return False
        # 
        # else:
        #     # Objects exist, find out closest
        #     self.work_out_closest_object(objects)
        #     return True

    def work_out_closest_object(self, objects):
        """ Works out which of the seen objects are closest"""

        smallestDifference = "null"
        newCoords = []
        returnedObject = None

        for obj in objects:
            objCoords = obj["coordinates"]
            xDiff = abs(self.coordinates[0] - objCoords[0])
            yDiff = abs(self.coordinates[1] - objCoords[1])
            totalDifference = xDiff + yDiff

            if totalDifference < smallestDifference:
                smallestDifference = totalDifference
                newCoords = objCoords
                returnedObject = obj

        return returnedObject
        self.rememberedCoords = newCoords



    def add_states_to_machine(self):
        """This is where the object will add states to its statemachine"""
        # print("Adding states to machine")
        for key, value in self.states.items():
            # print("\ncurrentState " + key)
            # print("currentValue " + str(value))
            self.stateMachine.add_state(key, value[1], value[0])

    def clear_vision(self):
        """This method wipes the vison"""
        self.vision = []

    def add_to_vision(self,id):
        """Adds to the vision array if it isn't aready in there"""
        vision = self.vision
        #variable to see if the id is already in the vision
        already_there = False
        for people in vision:
            #Cheacks to see if the person is already in the vision
            if id == people:
                already_there = True
        # if it isnt then it adds it to the array
        if already_there == False:
            vision.append(id)

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

        if not self.memory[key]:
            self.memory[key].append(obj)
            return True

        if self.check_obj_already_known(obj) is None:
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

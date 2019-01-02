# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018
from random import randint
from People.stateMachine import StateMachine

class Person:
    coordinates = [0,1]
    name = ""
    # map is None
    map = 0
    sight = 8

    rememberedObj = ""
    rememberedCoords = []

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

    def __init__(self, name):
        self.name = name

        self.stateMachine = StateMachine("person")
        self.add_states_to_machine()

        self.currentState = self.defaultState
        self.stateMachine.set_current_state(self.currentState)
        print(self.stateMachine.get_states())

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]

    def action(self):
        """What the person is going to do"""
        print("Current state " + str(self.currentState))

        stateAction = self.get_state_action()

        if stateAction == "navigateToCoords":
            print("action")

        elif stateAction == "":
            print("no action")
        else:
            self.random_move()
        # return self.random_move()

    def random_move(self):
        """Person moving randomly around the course"""

        randomNumber = randint(0, 10)
        # print(self.name + " should move " + str(randomNumber))
        newCoordinates = 0
        print(self.name + " random number " + str(randomNumber) + " -- initial coords " + str(self.coordinates))
        if randomNumber <= 2: #person move up
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]

        elif randomNumber <= 4: #Person move down
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]

        elif randomNumber <= 6: #person move right
            newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]

        elif randomNumber <= 8: #Person move left
            newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]

        # if randomNumber is <=10 then person has chosen to stay

        # if newCoordinates is not None:
        if isinstance(newCoordinates, list):
            if self.map.check_coordinates(newCoordinates):
                self.map.add_to_map(self, newCoordinates)
                self.map.remove_from_map(self.coordinates)
                self.coordinates = newCoordinates

        # print(self.name + " at coordinates " + str(self.coordinates))
        return self.coordinates;

    def store_coordinates(self, coordinates):
        """Storing a set of coordinates"""
        self.coordinates = coordinates

    def get_coordinates(self):
        """Getting stored coordinates"""
        return self.coordinates

    def get_state_action(self):
        """Causes the person to act based on their current state"""
        print("get state action")

        action = "moveRandom"

        if self.currentState == self.defaultState:
            print(self.name + " in greatest need")
            self.currentState = self.stateMachine.get_next_state()

        if "want" in self.currentState:
            # Person has a want desire
            if self.want_action(self.currentState):
                action = "navigateToCoords"

        elif "find" in self.currentState:
            # Person trying to find an object
            print(self.name + " finding object")
            if self.find_object(self.rememberedObj):
                action = "navigateToCoords"

        elif "move" in self.currentState:
            # Person moving to object
            print(self.name + " Person moving to object")
            action = "navigateToCoords"

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

        self.rememberedObj = searchObject

        return self.find_object(searchObject)

    def find_object(self, searchObject):
        """This function does the find function of a person
        :return Returns Ture if there are objects, false if it cant find one
        """
        objects = self.map.get_objects_in_range(searchObject, self.coordinates, self.sight)

        if not objects:
            # This is when there are no objects in range and you want the person to wander to keep looking
            print("no objects in range")
            self.rememberedCoords = "search"
            return False

        else:
            # Objects exist, find out closest
            self.work_out_closest_object(objects)
            return True

    def work_out_closest_object(self, objects):
        """ Works out which of the seen objects are closest"""

        smallestDifference = "null"
        newCoords = []

        for obj in objects:
            objCoords = obj["coordinates"]
            xDiff = abs(self.coordinates[0] - objCoords[0])
            yDiff = abs(self.coordinates[1] - objCoords[1])
            totalDifference = xDiff + yDiff

            if totalDifference < smallestDifference:
                smallestDifference = totalDifference
                newCoords = objCoords

        self.rememberedCoords = newCoords



    def add_states_to_machine(self):
        """This is where the object will add states to its statemachine"""
        print("Adding states to machine")
        for key, value in self.states.items():
            print("\ncurrentState " + key)
            print("currentValue " + str(value))
            self.stateMachine.add_state(key, value[1], value[0])

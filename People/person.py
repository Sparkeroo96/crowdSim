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

    # Persons "needs" first value is importance second is how much they want to do it
    needs = [["toilet", 1, 0],
             ["thirst", 2, 0],
             ["entertainment", 3, 0],
             ["freshAir", 3, 0]
            ]
    currentState = "Idle"
    stateMachine = ""

    states = {
        "greatestNeed": [["usedToilet", "drinkDrink", "danced"], ["wantDrink", "wantToilet", "wantDance"]],

        "wantDrink": [["isGreatestNeed"], ["findBar", "orderDrink"]],
        "findBar": [["notAtBar"], ["moveToBar"]],
        "moveToBar": [["found", "notFound"], ["orderDrink", "moveToBar"]],
        "orderDrink": [["atBar"], ["drink"]],
        "drink": [["getDrink"], ["drinkDrink"]],

        "wantDance": [["isGreatestNeed"], ["dance", "findDanceFloor"]],
        "findDanceFloor": [["notAtDanceFloor", "notFound"], ["moveToDanceFloor"]],
        "moveToDanceFloor": [["notAtDanceFloor", "found"], ["dance", "moveToDanceFloor"]],
        "dance": [["atDanceFloor"], ["greatestNeed"]],

        "wantToilet": [["isGreatestNeed"], ["findToilet", "useToilet"]],
        "findToilet": [["notAtToilet"], ["moveToilet"]],
        "moveToilet": [["foundToilet", "notFoundToilet"], ["moveToilet", "useToilet"]],
        "useToilet": [["atToilet"], ["usedToilet"]]
    }
    # gender = "" Use this one to determine which bathroom, later

    def __init__(self, name):
        self.name = name
        self.stateMachine = StateMachine("person")
        print(self.stateMachine.get_states())

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]

    def action(self):
        """What the person is going to do"""
        return self.move()

    def move(self):
        """Person moving randomly around the course"""

        randomNumber = randint(0, 10)
        # print(self.name + " should move " + str(randomNumber))
        newCoordinates = 0
        print(self.name + " random number " + str(randomNumber) + " -- initial coords " +  str(self.coordinates))
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
            if self.map.check_coordinates(newCoordinates) == True:
                self.map.add_to_map(self,newCoordinates)
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

    def find_greatest_need(self):
        """Function is to help a person find out what they want to do next, based on their needs
        Also considers them depending on their priority"""

        for need in self.needs():
            print("THis need")

    def add_states_to_machine(self):
        """This is where the object will add states to its statemachine"""
        print("Adding states to machine")
        for key, value in self.states:
            print("currentState " + key)
            print("currentValue " + value)
            self.stateMachine.add_state(key, value[1], value[0])
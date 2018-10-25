# Class manages the simulation in progress
# Will initi the map and the people
# Created by Sam Parker

from People.person import Person
from Map.map_main import MapMain
from random import randint


class Simulation:

    arrayPeople = []
    map = None

    def __init__(self):
        print("Simulation running")

    def start_simulation(self):
        """Starts the simulation"""
        self.create_people(10)
        self.create_map()
        self.populate_people_to_map()

    def create_people(self, numberOfPeople):
        """Creates a number of people and adds to the array of people"""
        print("Creating people class")

        for x in range(numberOfPeople):
            print(x)
            person = Person()
            self.arrayPeople.append(person)

    def create_map(self, xLength, yLength):
        """Creates a map object"""
        print("Creating Map")
        map = MapMain()
        self.map = map
        # self.map.

    def populate_people_to_map(self):
        """Adds people to the map"""
        mapLength = self.map.get_map_length()
        mapHeight = self.map.get_map_height()

        for person in self.arrayPeople:
            print("adding person to map");
            addedToMap = False

            while addedToMap == False:
                randomX = randint(0, mapLength)
                randomY = randint(0, mapHeight)
                coordinates = [randomX, randomY]

                if self.map.check_coordinates(coordinates) == 1:
                    self.map.add_to_map(coordinates)
                    person.store_coordinates(coordinates)
                    addedToMap = True


    def run_simulation(self):
        """Runs the simulation"""
        for x in range(100):
            self.step_simulation()

    def step_simulation(self):
        """Takes one step in the simulatio"""
        # self.map.step();



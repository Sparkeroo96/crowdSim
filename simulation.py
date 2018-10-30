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
        self.create_people(5)
        self.create_map(10, 10)
        self.populate_people_to_map()

    def create_people(self, numberOfPeople):
        """Creates a number of people and adds to the array of people"""
        print("Creating people class")

        for x in range(numberOfPeople):
            person = Person()
            self.arrayPeople.append(person)

    def create_map(self, xLength, yLength):
        """Creates a map object"""
        print("Creating Map")
        map = MapMain()
        self.map = map
        self.map.map_generate(xLength, yLength)

    def populate_people_to_map(self):
        print("In populat")
        """Adds people to the map"""
        mapLength = self.map.get_map_length() - 1
        mapHeight = self.map.get_map_height() - 1
        print("map length " + str(mapLength) + " mapHeight " + str(mapHeight))

        for person in self.arrayPeople:
            print("adding person to map");
            addedToMap = False

            while addedToMap == False:
                randomX = randint(0, mapLength)
                randomY = randint(0, mapHeight)
                coordinates = [randomX, randomY]

                if self.map.check_coordinates(coordinates) == 1:
                    self.map.add_to_map(person, coordinates)
                    # person.store_coordinates(coordinates)
                    person.add_map(self.map, coordinates)
                    addedToMap = True


    def run_simulation(self):
        """Runs the simulation"""
        print("In run simulation")
        for x in range(100):
            self.step_simulation()

    def step_simulation(self):
        print("Stepping simulation")
        """Takes one step in the simulation"""
        for person in self.arrayPeople:
            person.action()

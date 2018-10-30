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
        print("Simulation init")

    def start_simulation(self):
        """Starts the simulation"""
        self.create_people(5)
        self.create_map(10, 10)
        self.populate_people_to_map()

    def create_people(self, numberOfPeople):
        """Creates a number of people and adds to the array of people"""
        for x in range(numberOfPeople):
            person = Person("Person " + str(x))
            self.arrayPeople.append(person)

    def create_map(self, xLength, yLength):
        """Creates a map object"""
        self.map = MapMain()
        self.map.map_generate(xLength, yLength)

    def populate_people_to_map(self):
        """Adds people to the map"""
        mapLength = self.map.get_map_length() - 1
        mapHeight = self.map.get_map_height() - 1

        for person in self.arrayPeople:
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
        x = 0
        for x in range(100):
            self.step_simulation()
            x += 1

    def step_simulation(self):
        """Takes one step in the simulation"""
        for person in self.arrayPeople:
            person.action()

# Class manages the simulation in progress
# Will initi the map and the people
# Created by Sam Parker

from People import *
# from People.person import Person
from Map.map_main import MapMain
from random import randint
from GUI.GuiController import GuiController


class Simulation:
    gui = None
    arrayPeople = []
    map = None

    def __init__(self):
        print("Simulation init")

    def set_gui(self,gui1):
        global gui
        gui = gui1

    def get_gui(self):
        global gui
        return gui

    def start_simulation(self):
        """Starts the simulation"""
        self.create_people(5)
        self.create_map(15, 15)
        self.populate_people_to_map()
        gui = GuiController()
        self.set_gui(gui)
        gui.init_grid(self.map)
        gui.redraw()


    def create_people(self, numberOfPeople):
        """Creates a number of people and adds to the array of people"""
        for x in range(numberOfPeople):
            # person = Person("Person " + str(x))
            # newPerson = person.Person("Person " + str(x))
            newPerson = flockingPerson.FlockingPerson("Person " + str(x))
            self.arrayPeople.append(newPerson)

    def create_map(self, xLength, yLength):
        """Creates a map object"""
        self.map = MapMain()
        self.map.map_generate(xLength, yLength)

    def populate_people_to_map(self):
        """Adds people to the map"""
        mapLength = self.map.get_map_length() - 1
        mapHeight = self.map.get_map_height() - 1

        x = 3
        for person in self.arrayPeople:
            addedToMap = False

            while addedToMap == False:
                randomX = randint(0, mapLength)
                randomY = randint(0, mapHeight)
                coordinates = [randomX, randomY]
                # coordinates = [x, 10]

                if self.map.check_coordinates(coordinates) == 1:
                    self.map.add_to_map(person, coordinates)
                    # person.store_coordinates(coordinates)
                    person.add_map(self.map, coordinates)
                    addedToMap = True
            x += 7


    def run_simulation(self):
        """Runs the simulation"""
        x = 0
        print(str(self.map.get_map()))
        for x in range(100):
            self.step_simulation()
            x += 1
            gui = self.get_gui()
            gui.redraw()

        print(self.map.get_map())

    def step_simulation(self):
        """Takes one step in the simulation"""
        for person in self.arrayPeople:
            person.action()

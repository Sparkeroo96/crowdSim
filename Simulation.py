# Class manages the simulation in progress
# Will initi the map and the people
# Created by Sam Parker

from People.person import Person
from Map.map_main import MapMain
from GUI.GuiController import GuiController


class Simulation:

    arrayPeople = []
    map = None

    def __init__(self):
        print("Simulation running")

    def start_simulation(self):
        self.create_people(10)
        self.create_map()
        self.populate_people_to_map()

    def create_people(self, numberOfPeople):
        print("Creating people class")

        for x in range(numberOfPeople):
            print(x)
            person = Person()
            self.arrayPeople.append(person)

    def create_map(self):
        print("Creating Map")
        map = MapMain()
        self.map = map

    def populate_people_to_map(self):
        for x in len(self.map):
            print("Adding People To Map")



    def step_simulation(self):
        self.map.step();

    def run_simulation(self):
        for x in range(100):
            self.step_simulation()

    # @staticmethod
    def test_gui(self):
        self.GuiController.init_grid()


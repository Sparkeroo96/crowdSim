# Class manages the simulation in progress
# Will initi the map and the people
# Created by Sam Parker

from People import person
from Map import map_main
from random import randint
# from GUI.GuiController import GuiControllerw
print('Hello0')
from GUI import test
print('Hello1')
# from Data import map_data

class simulation:
    gui = None
    arrayPeople = []
    map = None

    def __init__(self):
        print("Simulation init")

    # def set_gui(self,gui1):
    #     global gui
    #     gui = gui1
    #
    # def get_gui(self):
    #     global gui
    #     return gui
    #
    # def welcome_page(self):
    #     """Creates the window for the application to run"""
    #     gui = GuiController()
    #     self.set_gui(gui)
    #     #Calls the method in the main GUI to create the main screen
    #     gui.init_master(self)
    #     #gui.init_welcome_page(map)
    #
    #
    #
    # def start_simulation(self):
    #     """Starts the simulation"""
    #     self.create_people(5)
    #     self.create_map(12, 10)
    #     self.populate_people_to_map()
    #     gui = self.get_gui()
    #     gui.init_simulation_frame(self.map)
    #     gui.manage_frames()
    #     self.run_simulation()
    #
    # def create_people(self, numberOfPeople):
    #     """Creates a number of people and adds to the array of people"""
    #     for x in range(numberOfPeople):
    #         person = Person("Person " + str(x))
    #         self.arrayPeople.append(person)
    #
    # def defult_map(self):
    #     """Creates a defult size for the welcome page"""
    #     self.map = MapMain()
    #     map = self.map.defult_map()
    #     return map
    #
    # def create_map(self, xLength, yLength):
    #     """Creates a map object"""
    #     self.map = MapMain()
    #     self.map.map_generate(xLength, yLength)
    #
    # def populate_people_to_map(self):
    #     """Adds people to the map"""
    #     mapLength = self.map.get_map_length() - 1
    #     mapHeight = self.map.get_map_height() - 1
    #
    #     for person in self.arrayPeople:
    #         addedToMap = False
    #
    #         while addedToMap == False:
    #             randomX = randint(0, mapLength)
    #             randomY = randint(0, mapHeight)
    #             coordinates = [randomX, randomY]
    #
    #             if self.map.check_coordinates(coordinates) == 1:
    #                 self.map.add_to_map(person, coordinates)
    #                 # person.store_coordinates(coordinates)
    #                 person.add_map(self.map, coordinates)
    #                 addedToMap = True
    #
    #
    # def run_simulation(self):
    #     """Runs the simulation"""
    #     print("In run simulation")
    #     x = 0
    #     for x in range(100):
    #         self.step_simulation()
    #         x += 1
    #         gui = self.get_gui()
    #         gui.manage_frames()
    #
    # def step_simulation(self):
    #     """Takes one step in the simulation"""
    #     for person in self.arrayPeople:
    #         person.action()

    def test(self):
        print('Moo:3')
        gui = test()
        gui.test()

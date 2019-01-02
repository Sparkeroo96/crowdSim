# Class manages the simulation in progress
# Will initi the map and the people
# Created by Sam Parker

from Environment.environment_locations import EnvironmentLocations
from People.person import Person
from Map.map_main import MapMain
from random import randint
from GUI.GuiController import GuiController


class Simulation:
    gui = None
    arrayPeople = []
    arrayEnvObjects = []
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
        # self.create_env_objects()
        self.create_people(2)
        self.create_map(12, 14)
        self.populate_env_objects_to_map()
        self.populate_people_to_map()
        gui = GuiController()
        self.set_gui(gui)
        gui.init_grid(self.map)
        # print("1")
        gui.redraw()
        # print('2')

    def create_people(self, numberOfPeople):
        """Creates a number of people and adds to the array of people"""
        for x in range(numberOfPeople):
            person = Person("Person " + str(x))
            self.arrayPeople.append(person)

    # def create_env_objects(self):
    #         envObjects = EnvObject()
    #         barObjects = BarObject()
    #         """Append the cords in the envObjects Array"""
    #         self.arrayEnvObjects.append(envObjects)
    #         self.arrayEnvObjects.append(barObjects)
    #         #print(self.arrayEnvObjects[1].env_object_name())
    #         #print(len(self.arrayEnvObjects))

    def create_map(self, xLength, yLength):
        """Creates a map object"""
        self.map = MapMain()
        self.map.map_generate(xLength, yLength)

    def populate_env_objects_to_map(self):
        envLocations = EnvironmentLocations()
        # print(envLocations.location_array(0))
        """Iterates through the for loop"""
        add = 0
        """Adds environment objects to the map"""
        for i in envLocations.get_array():
            print(envLocations.location_array(add))
            addedToMap = False
            while addedToMap == False:
                if self.map.check_coordinates(envLocations.location_array(add)) == 1:
                    self.map.add_env_objects_to_map(envLocations.location_array(add))
                    i.add_map(self.map, envLocations.location_array(add))
                    addedToMap = True
            add += 1

            # for envObject in self.arrayEnvObjects:
            #     print(envObject)
            #     print("testing")
            #     addedToMap = False
            #     while addedToMap == False:
            #         # coordinates = envLocations.location_array(0)
            #         """ need to think of a new way of adding coordinates in"""
            #         coordinates = envObject.get_cords()
            #         if self.map.check_coordinates(coordinates) == 1:
            #             self.map.add_env_objects_to_map(coordinates)
            #             """ stores a map """
            #             envObject.add_map(self.map, coordinates)
            #             addedToMap = True

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
            # print("Redraw")
            gui = self.get_gui()
            gui.redraw()

    def step_simulation(self):
        """Takes one step in the simulation"""
        for person in self.arrayPeople:
            person.action()

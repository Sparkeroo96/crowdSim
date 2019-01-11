"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
import math
from Data import map_data
from time import sleep
from People.person import Person

class RunningMain:

    # data = map_data.map_data()
    # pygame.init()

    data = None

    # RGB Colours defined
    white = (255,255,255)
    black = (0,0,0)
    green = (51, 204, 51)
    red = (255, 0, 0)

    display = None

    def __init__(self):
        self.data = map_data.map_data(self)
        pygame.init()

        # Getting intial data to start the main loop for the simulation method
        objectArray = self.data.map_default()

        self.display = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Crowd Simulation ")

        clock = pygame.time.Clock()
        exit = False
        # Main loop for the applicaion
        while not exit:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    exit = True

            self.draw_display(objectArray)

            # display.fill(self.white)
            # # Goes though the map array object
            # for object in objectArray:
            #     object.action()
            #     # print("object")
            #     coordinates = object.get_coordinates()
            #     angle = object.get_angle()
            #     width = object.get_width()
            #     colour = object.get_colour()
            #
            #     shape = object.get_shape()
            #     # print("shape = " + shape)
            #     # the process of adding a person and the funcitons that get called
            #     if shape == "circle":
            #         # Creating the cicle with the variables provided
            #         pygame.draw.circle(display, colour, coordinates, round(width/2))
            #         # Maths to add the pixcels to represent the eyes
            #         eyes = self.data.person_eyes(object.coordinates, object.angle, round(object.width/2))
            #         display.set_at((eyes[0][0],eyes[0][1]), self.white)
            #         display.set_at((eyes[1][0],eyes[1][1]), self.white)
            #         # print(vision)
            #         # print(objectArray)
            #
            #     elif shape == "rectangle":
            #         # objects
            #         height = object.get_height()
            #         pygame.draw.rect(display, self.black, [coordinates[0], coordinates[1], width, height])
            #
            # for object in objectArray:
            #     if shape == 'circle':
            #         # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes
            #         vision = self.data.personVision(object.coordinates[0],object.coordinates[1],object.angle)
            #         # clears the person vision from the previous ittoration
            #         object.clear_vision()
            #         # goes though every coordinates and works out what colour is in that pixcel
            #         for cord in vision:
            #             # display.set_at((cord[0],cord[1]), black)
            #             # try and catch to prevent out of array exceptions
            #             try:
            #                 # gets the colour at the cordiate
            #                 colour = display.get_at((cord[0],cord[1]))
            #                 # if it is red then it must be a person
            #                 if colour == (255,0,0,255): #Red person
            #                 # calls a function that returns the id of the person they can see
            #                     whichPerson = self.data.whichPerson(cord)
            #                     # adds to the persons vision array in their object
            #                     object.add_to_vision(whichPerson)
            #             except IndexError:
            #                 nothing = 0

            #FOR TESTING PURPOSES
            sleep(1)
            # END OF SLEEP

            pygame.display.update()
            clock.tick(30)
        pygame.quit()
        quit()

    def draw_display(self, objectArray):
        """
        Draws the display
        :param display: The pygame display
        :param objectArray: The objects that you wish to draw
        :return:
        """
        self.display.fill(self.white)
        # Goes though the map array object
        for obj in objectArray:
            obj.action()
            # print("object")
            coordinates = obj.get_coordinates()
            angle = obj.get_angle()
            width = obj.get_width()
            colour = obj.get_colour()

            shape = obj.get_shape()
            # print("shape = " + shape)
            # the process of adding a person and the funcitons that get called
            if shape == "circle":
                # Creating the cicle with the variables provided
                pygame.draw.circle(self.display, colour, coordinates, round(width / 2))
                # Maths to add the pixcels to represent the eyes
                eyes = self.data.person_eyes(obj.coordinates, obj.angle, round(obj.width / 2))
                self.display.set_at((eyes[0][0], eyes[0][1]), self.white)
                self.display.set_at((eyes[1][0], eyes[1][1]), self.white)
                # print(vision)
                # print(objectArray)

            elif shape == "rectangle":
                # objects
                height = obj.get_height()
                pygame.draw.rect(self.display, self.black, [coordinates[0], coordinates[1], width, height])

        for obj in objectArray:
            # if shape == 'circle':
            if isinstance(obj, Person):
                # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes

                sight = obj.get_sight()
                coordinates = obj.get_coordinates()

                vision = self.data.personVision(coordinates[0], coordinates[1], obj.angle, sight)
                # clears the person vision from the previous ittoration
                obj.clear_vision()
                # goes though every coordinates and works out what colour is in that pixcel
                for cord in vision:
                    # display.set_at((cord[0],cord[1]), black)
                    # try and catch to prevent out of array exceptions
                    try:
                        # gets the colour at the cordiate
                        colour = self.display.get_at((cord[0], cord[1]))
                        # if it is red then it must be a person

                        if colour != (255, 255, 255, 255):
                            # Its an object of some kind
                            seenObj = self.data.what_object

                            obj.add_to_vision(seenObj)
                            obj.add_to_memory(obj)

                        # if colour == (255, 0, 0, 255):  # Red person
                        #     # calls a function that returns the id of the person they can see
                        #     whichPerson = self.data.what_object(cord)
                        #     # adds to the persons vision array in their object
                        #     obj.add_to_vision(whichPerson)

                    except IndexError:
                        nothing = 0


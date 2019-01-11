"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
import math
from Data import map_data
<<<<<<< HEAD
class runningMain:

    data = map_data.map_data()
    pygame.init()

    # RGB Colours defined
    white = (255,255,255)
    black = (0,0,0)
    green = (51, 204, 51)
    red = (255, 0, 0)

    display = None
    # Getting intial data to start the main loop for the simulation method
    objectArray = data.map_default()

display = pygame.display.set_mode((800,600))
pygame.display.set_caption("Crowd Simulation ")
pause = False
clock = pygame.time.Clock()
exit = False
wall = False
drag = False
# Main loop for the applicaion
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause

    display.fill(white)
    # Pauses the simulation and alows for editing function
    while pause:
        for event in pygame.event.get():
            print(event)
            #Pauses sim
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                #Allows wall adding
                if event.key == pygame.K_w:
                    print("making wall")
                    wall = True
            # Gets the starting cordinates for the walls
            if event.type == pygame.MOUSEBUTTONDOWN and wall:
                x1, y1 = event.pos
                drag = True
            # gets the width and height for the walls and creates the object
            if event.type == pygame.MOUSEBUTTONUP and wall:
                x2, y2 = event.pos
                width = x1 - x2
                width = width * -1
                height = y1 - y2
                height = height * -1
                data.add_wall_to_map([x1,y1],width,height)
                pygame.draw.rect(display,black,[x1,y1,width,height])
                pygame.display.update()
                drag = not drag
            # quits if x is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    # Goes though the map array object
    for object in objectArray:
        object.action()
        # print("object")
        coordinates = object.get_coordinates()
        angle = object.get_angle()
        width = object.get_width()
        colour = object.get_colour()

        shape = object.get_shape()
        # print("shape = " + shape)
        # the process of adding a person and the funcitons that get called
        if shape == "circle":
            # Creating the cicle with the variables provided
            pygame.draw.circle(display, colour, coordinates, round(width/2))
            # Maths to add the pixcels to represent the eyes
            eyes = object.person_eyes(object.coordinates, object.angle, round(object.width/2))
            display.set_at((eyes[0][0],eyes[0][1]),white)
            display.set_at((eyes[1][0],eyes[1][1]),white)
            # print(vision)
            # print(objectArray)

        elif shape == "rectangle":
            # objects
            coordinates = object.get_coordinates()
            pygame.draw.rect(display, black, [coordinates[0],coordinates[1], object.get_xSize(), object.get_ySize()])

    for object in objectArray:
        if shape == 'circle':
            # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes
            vision = object.personVision(object.coordinates[0],object.coordinates[1],object.angle)
            # clears the person vision from the previous ittoration
            object.clear_vision()
            # goes though every coordinates and works out what colour is in that pixcel
            for cord in vision:
                # display.set_at((cord[0],cord[1]), black)
                # try and catch to prevent out of array exceptions
                try:
                    # gets the colour at the cordiate
                    colour = display.get_at((cord[0],cord[1]))
                    # if it is red then it must be a person
                    if colour == (255,0,0,255): #Red person
                    # calls a function that returns the id of the person they can see
                        whichPerson = data.whichPerson(cord)
                        # adds to the persons vision array in their object
                        object.add_to_vision(whichPerson)
                except IndexError:
                    nothing = 0
    pygame.display.update()
    clock.tick(30)
pygame.quit()
quit()
=======
from time import sleep


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
        for object in objectArray:
            object.action()
            # print("object")
            coordinates = object.get_coordinates()
            angle = object.get_angle()
            width = object.get_width()
            colour = object.get_colour()

            shape = object.get_shape()
            # print("shape = " + shape)
            # the process of adding a person and the funcitons that get called
            if shape == "circle":
                # Creating the cicle with the variables provided
                pygame.draw.circle(self.display, colour, coordinates, round(width / 2))
                # Maths to add the pixcels to represent the eyes
                eyes = self.data.person_eyes(object.coordinates, object.angle, round(object.width / 2))
                self.display.set_at((eyes[0][0], eyes[0][1]), self.white)
                self.display.set_at((eyes[1][0], eyes[1][1]), self.white)
                # print(vision)
                # print(objectArray)

            elif shape == "rectangle":
                # objects
                height = object.get_height()
                pygame.draw.rect(self.display, self.black, [coordinates[0], coordinates[1], width, height])

        for object in objectArray:
            if shape == 'circle':
                # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes
                vision = self.data.personVision(object.coordinates[0], object.coordinates[1], object.angle)
                # clears the person vision from the previous ittoration
                object.clear_vision()
                # goes though every coordinates and works out what colour is in that pixcel
                for cord in vision:
                    # display.set_at((cord[0],cord[1]), black)
                    # try and catch to prevent out of array exceptions
                    try:
                        # gets the colour at the cordiate
                        colour = display.get_at((cord[0], cord[1]))
                        # if it is red then it must be a person
                        if colour == (255, 0, 0, 255):  # Red person
                            # calls a function that returns the id of the person they can see
                            whichPerson = self.data.whichPerson(cord)
                            # adds to the persons vision array in their object
                            object.add_to_vision(whichPerson)
                    except IndexError:
                        nothing = 0

>>>>>>> task_6

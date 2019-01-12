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

    data = None

    # RGB Colours defined
    white = (255,255,255)
    black = (0,0,0)
    green = (51, 204, 51)
    red = (255, 0, 0)

    display = None
    pause = None

    def __init__(self):
        pygame.init()
        self.data = map_data.map_data(self)

        # Getting intial data to start the main loop for the simulation method
        objectArray = self.data.map_default()

        self.display = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Crowd Simulation ")

        pause = False
        clock = pygame.time.Clock()
        exit = False
        wall = False
        drag = False
        # Main loop for the applicaion

        print("before while")
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause

            # Function that runs the main program
            self.key_buttons()
            self.draw_display(objectArray)
            pygame.display.update()
            clock.tick(30)

        pygame.quit()
        quit()

    def key_buttons(self):
        while self.pause:
            for event in pygame.event.get():
                # print(event)
                #Pauses sim
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
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
                    # print(x1)
                    # print(y1)
                    # print(height)
                    # print(width)
                    # print()
                    self.data.add_wall_to_map([x1,y1],width,height)
                    pygame.draw.rect(self.display,self.black,[x1,y1,width,height])
                    pygame.display.update()
                    drag = not drag
                # quits if x is pressed
                if event.type == pygame.QUIT:
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
                eyes = obj.person_eyes(coordinates, angle, round(width / 2))
                self.display.set_at((eyes[0][0], eyes[0][1]), self.white)
                self.display.set_at((eyes[1][0], eyes[1][1]), self.white)
                # print(vision)
                # print(objectArray)

            elif shape == "rectangle":
                # objects

                # coordinates = obj.get_coordinates()
                # height = obj.get_ySize()
                # width = obj.get_xSize()
                height = obj.get_height()
                # width = obj.get_width()
                pygame.draw.rect(self.display, self.black, [coordinates[0], coordinates[1], width, height])

        for obj in objectArray:
            # if obj.get_shape() == 'circle':
            if isinstance(obj, Person):
                print("isinstance " + str(obj))
                # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes

                sight = obj.get_sight()
                coordinates = obj.get_coordinates()

                # vision = self.data.personVision(coordinates[0], coordinates[1], obj.angle, sight)
                vision = obj.personVision(coordinates[0], coordinates[1], obj.angle, sight)
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

                            seenObj = self.data.what_object(cord)
                            obj.add_to_vision(seenObj)
                            obj.add_to_memory(seenObj)

                        # if colour == (255, 0, 0, 255):  # Red person
                        #     # calls a function that returns the id of the person they can see
                        #     whichPerson = self.data.what_object(cord)
                        #     # adds to the persons vision array in their object
                        #     obj.add_to_vision(whichPerson)

                    except IndexError:
                        nothing = 0
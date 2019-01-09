"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
import math
from Data import map_data
from time import sleep

data = map_data.map_data()
pygame.init()

# RGB Colours defined
white = (255,255,255)
black = (0,0,0)
green = (51, 204, 51)
red = (255, 0, 0)

# Getting intial data to start the main loop for the simulation method
objectArray = data.map_default()

display = pygame.display.set_mode((800,600))
pygame.display.set_caption("Crowd Simulation ")

clock = pygame.time.Clock()
exit = False
# Main loop for the applicaion
while not exit:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            exit = True
    display.fill(white)
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
            eyes = data.person_eyes(object.coordinates, object.angle, round(object.width/2))
            display.set_at((eyes[0][0],eyes[0][1]),white)
            display.set_at((eyes[1][0],eyes[1][1]),white)
            # print(vision)
            # print(objectArray)

        elif shape == "rectangle":
            # objects
            height = object.get_height()
            pygame.draw.rect(display, black, [coordinates[0], coordinates[1], width, height])

    for object in objectArray:
        if shape == 'circle':
            # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes
            vision = data.personVision(object.coordinates[0],object.coordinates[1],object.angle)
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

    #FOR TESTING PURPOSES
    sleep(1)
    # END OF SLEEP
    
    pygame.display.update()
    clock.tick(30)
pygame.quit()
quit()

"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
from Data import map_data
"""Constant for grid"""
CONSTANT = 1
data = map_data.map_data()
pygame.init()

# RGB Colours defined
white = (255,255,255)
black = (0,0,0)
green = (51, 204, 51)
red = (255, 0, 0)

# Getting intial data to start the main loop for the simulation method
objectArray = data.map_default()

display = pygame.display.set_mode((500,500))
w, h = pygame.display.get_surface().get_size()
# print(w)
# print(h)
grid = []
path = []

pygame.display.set_caption("Crowd Simulation ")
x = 0
clock = pygame.time.Clock()
exit = False
while not exit:

    # print(path)
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            exit = True
    display.fill(white)
    # for row in range(int(w / CONSTANT)):
    #     grid.append([])
    #     for column in range(int(h / CONSTANT)):
    #         grid[row].append(0)
    #         checkColour = display.get_at((row, column))
    #         pygame.draw.rect(display,
    #                          white,
    #                          [(CONSTANT * 2) * column + CONSTANT,
    #                           (CONSTANT * 2) * row + CONSTANT,
    #                           CONSTANT,
    #                           CONSTANT])
    """Currently prints the a* path"""
    # if x == 0:
    #     x1 = data.get_e_coords()[0][0]
    #     x2 = data.get_e_coords()[0][1]
    #     y1 = data.get_p_coords()[0][0]
    #     y2 = data.get_p_coords()[0][1]
    #     path = astar.aStar(grid, (x1, x2), (y1, y2))
    #     x += 1

    # display.fill(white)
    """Placeholder wall"""
    """x, y, ?"""
    # locations = []
    # map_data.map_data.set_walls()
    """Each object that gets added into the array"""
    for object in objectArray:
        object.action()
        # print("object")
        coordinates = object.get_coordinates()
        angle = object.get_angle()
        width = object.get_width()
        colour = object.get_colour()

        shape = object.get_shape()
        # print("shape = " + shape)
        if shape == "circle":
            # People
            # print("here " + str(coordinates))
            pygame.draw.circle(display, colour, coordinates, width)
            """Displays the colour it currently uses"""
            # print(display.get_at(coordinates)[:3])
            if path != []:
                for coord in path:
                    pygame.draw.circle(display, colour, coord, width)
        elif shape == "rectangle":
            # objects
            height = object.get_height()
            pygame.draw.rect(display, colour, [coordinates[0], coordinates[1], width, height])
        elif shape == "wall":

            height = object.get_height()
            # print(angle, width, height)
            pygame.draw.rect(display, colour, [coordinates[0], coordinates[1], width, height])





    # print(display.get_at((51, 51))[:3])
        # display.fill(red, (0, 100, 200, 200))

        # NEED TO ADD VISION STUFF
        # LEAVE FOR CHRIS?

    # Going though the data set and assigning the different objects to the screen
    # for object in array:
    #     # Adding the people to the map
    #     if object[0]  == 'person':
    #         xCoordinate = object[2][0]
    #         yCoordinate = object[2][1]
    #         angle = object[3]
    #         width = object[4]
    #         pygame.draw.circle(display, red, [xCoordinate,yCoordinate],width)
    #         vision = data.personVision(object[1])
    #         previous = 0
    #         for cord in vision:
    #             # display.set_at((cord[0],cord[1]),black)
    #             try:
    #                 colour = display.get_at((cord[0],cord[1]))
    #                 if colour == (255,0,0,255): #Red person
    #                     whichPerson = data.whichPerson(cord)
    #                     if previous != whichPerson and whichPerson != None:
    #                         print(previous)
    #                         print(whichPerson)
    #                         print(" ")
    #                     previous = whichPerson
    #                     # print("I see someone!")
    #             except IndexError:
    #                 nothing = 0
    #                 # print()
    #                 # break
    #     if object[0] == 'wall':
    #         xCoordinate = object[1][0]
    #         yCoordinate = object[1][1]
    #         width = object[2][0]
    #         height = object[2][1]
    #         pygame.draw.rect(display,black,[xCoordinate,yCoordinate,width, height])
    # # exit = True
    # data.moveRandomly()
    # print(display.get_at((400, 100))[:3])


        """Prints the color at coord 200, 200"""
        # if x < CONSTANT:
        #     colour = display.get_at((11 + x, 11))[:3]
        #     # if colour == (255, 255, 255):
        #     print(colour)
        #     x += 1
    """Draws a white grid over the black surface"""

    pygame.display.update()
    clock.tick(4)
pygame.quit()
quit()

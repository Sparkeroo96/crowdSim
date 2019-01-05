"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
"""
import pygame
import time

from Data import map_data
from Algorithm import a_star

data = map_data.map_data()
astar = a_star
pygame.init()

# RGB Colours defined
white = (255,255,255)
black = (0,0,0)
green = (51, 204, 51)
red = (255, 0, 0)
yellow = (255,255,0)
# Getting intial data to start the main loop for the simulation method
array = data.getMap()
HEIGHT = 20
WIDTH = 20
MARGIN = 5

display = pygame.display.set_mode((505, 505))
pygame.display.set_caption("Crowd Simulation ")


clock = pygame.time.Clock()
exit = False
grid = []
for row in range(20):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(20):
        grid[row].append(0)
grid[4][1] = 4
grid[4][2] = 4
grid[4][3] = 4
grid[4][4] = 4
grid[4][5] = 4
grid[4][6] = 4

while not exit:
    """a* Path algo, need to insert person coords & object coords """
    path = astar.aStar(grid, (0, 0), (1, 2))
    print(path)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    display.fill(white)
    """GUI Grid"""
    for row in range(20):
        for column in range(20):
            color = white
            pygame.draw.rect(display,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])





    # Going though the data set and assigning the different objects to the screen
    for object in array:
        # print("testing")
        # print(object)
        # Adding the people to the map
        if object[0]  == 'person':
            xCoordinate = object[2][0]
            yCoordinate = object[2][1]
            angle = object[3]
            width = object[4]
            pygame.draw.circle(display, red, [xCoordinate,yCoordinate],width)
            vision = data.personVision(object[1])
            previous = 0
            for cord in vision:
                # display.set_at((cord[0],cord[1]),black)
                try:
                    colour = display.get_at((cord[0],cord[1]))
                    if colour == (255,0,0,255): #Red person
                        whichPerson = data.whichPerson(cord)
                        if previous != whichPerson and whichPerson != None:
                            print(previous)
                            print(whichPerson)
                            print(" ")
                        previous = whichPerson
                        # print("I see someone!")
                except IndexError:
                    nothing = 0
                    # print()
                    # break
        if object[0] == 'wall':
            xCoordinate = object[1][0]
            yCoordinate = object[1][1]
            width = object[2][0]
            height = object[2][1]
            pygame.draw.rect(display,black,[xCoordinate,yCoordinate,width, height])
        if object[0] == 'Drinks Bar':
            pygame.draw.rect(display, yellow, [object[2], object[3], object[4], object[5]])
    # exit = True
    data.moveRandomly(0)
    pygame.display.update()
    clock.tick(30)
pygame.quit()
quit()

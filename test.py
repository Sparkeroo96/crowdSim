import pygame
from Data import map_data

data = map_data.map_data()
pygame.init()

# RGB Colours defined
white = (255,255,255)
black = (0,0,0)
green = (51, 204, 51)
red = (255, 0, 0)
# Getting intial data to start the main loop for the simulation method
array = data.getMap()

display = pygame.display.set_mode((800,600))
pygame.display.set_caption("Crowd Simulation ")

clock = pygame.time.Clock()
exit = False
while not exit:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            exit = True
    display.fill(white)
    # Going though the data set and assigning the different objects to the screen
    for object in array:
        # Adding the people to the map
        if object[0]  == 'person':
            xCoordinate = object[2][0]
            yCoordinate = object[2][1]
            angle = object[3]
            width = object[4]
            pygame.draw.circle(display, red, [xCoordinate,yCoordinate],width)
            vision = data.personVision(object[1])
            for cord in vision:
                display.set_at((cord[0],cord[1]),black)
                try:
                    colour = display.get_at((cord[0],cord[1]))
                    if colour == (255,0,0,255): #Red person
                        print()
                except IndexError:
                    print('Out of area')
                    # break
        if object[0] == 'wall':
            xCoordinate = object[1][0]
            yCoordinate = object[1][1]
            width = object[2][0]
            height = object[2][1]
            pygame.draw.rect(display,black,[xCoordinate,yCoordinate,width, height])
    # exit = True
    data.moveRandomly()
    pygame.display.update()
    clock.tick(30)
pygame.quit()
quit()

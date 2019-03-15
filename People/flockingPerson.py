#Class is person except they now have flocking functionality
#Created by Sam Parker 13/11/18

from People.person import Person
from random import getrandbits

class FlockingPerson(Person):

    repulsion = 2
    attraction = 5

    # moveUpCount = 0
    # moveDownCount = 0
    # moveLeftCount = 0
    # moveRightCount = 0
    moveXPlane = 0
    moveYPlane = 0


    def action(self):
        objects = self.map.get_objects_in_range(FlockingPerson, self.coordinates, self.sight)
        self.set_move_direction(objects)
        self.move_with_direction(objects)

    def move_with_direction(self, direction):
        """Move in the direction given"""
        newCoordinates = 0
        # print("move up " + str(self.moveUpCount))
        # print("move down " + str(self.moveDownCount))
        # print("move left " + str(self.moveLeftCount))
        # print("move right " + str(self.moveRightCount))
        if self.moveUpCount > max(self.moveDownCount, self.moveLeftCount, self.moveRightCount):
            print("obj moving up")
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 1]

        elif self.moveDownCount > max(self.moveUpCount, self.moveLeftCount, self.moveRightCount):
            print("obj moving down")
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 1]

        elif self.moveLeftCount > max(self.moveUpCount, self.moveDownCount, self.moveRightCount):
            print("obj moving left")
            newCoordinates = [self.coordinates[0] - 1, self.coordinates[1]]

        elif self.moveRightCount > max(self.moveUpCount, self.moveDownCount, self.moveLeftCount):
            newCoordinates = [self.coordinates[0] + 1, self.coordinates[1]]
            print(self.name + " obj moving right " + str(self.coordinates) + " new " + str(newCoordinates))

        else:
            #should do something if nothing stands out
            print("None is greater than another, move randomly??")
            self.random_move()

        if isinstance(newCoordinates, list):
            if self.map.check_coordinates(newCoordinates) == True:
                self.map.add_to_map(self, newCoordinates)
                self.map.remove_from_map(self.coordinates)
                print(self.name + " old coords " + str(self.coordinates) + " new coords " + str(newCoordinates))
                self.coordinates = newCoordinates
            else:
                print("Not coords")

    def set_move_direction(self,objects):
        """Chooses the best direction to move in based on nearby objects"""
        self.moveUpCount = 0
        self.moveDownCount = 0
        self.moveLeftCount = 0
        self.moveRightCount = 0

        for obj in objects:
            xDiff = self.coordinates[0] - obj['coordinates'][0]
            yDiff = self.coordinates[1] - obj['coordinates'][1]

            if xDiff <= self.repulsion and xDiff > 0:
                #If object is to close and to the left
                self.moveRightCount += 1
                continue
            elif abs(xDiff) <= self.repulsion and xDiff != 0:
                #obj is to close to the right
                print(self.name + " is repeling left " + str(xDiff) + " " + str(self.repulsion))
                self.moveLeftCount += 1
                continue
            elif yDiff <= self.repulsion and yDiff > 0:
                #obj is too close and below
                self.moveUpCount += 1
                #Changed as y goes down not up as it ascends
                # self.moveDownCount += 1
                continue

            elif abs(yDiff)<= self.repulsion and yDiff != 0:
                #obj to close and above
                self.moveDownCount += 1
                # self.moveUpCount += 1
                continue
            else:
                print(self.name + " is attracting " + str(xDiff) + " / " + str(yDiff))
                #Not being repulsed by the object but attracted
                self.choose_attract_direction(xDiff, yDiff)


    def choose_attract_direction(self, xDiff, yDiff):
        """Out of all the objects that are there figures out the best way to move to be attracted to an object"""
        #NOTE MAYBE HAVE TO ADD SOMETHING HERE TO DO IF WE ARE IN ATTRACTION MOVE COMPLETLY RANDOMLY THERE
        if abs(xDiff) > abs(yDiff) and abs(xDiff) >= self.attraction:
            #Further away in the x plane
            self.attract_x_plane(xDiff)

        elif abs(yDiff) > abs(xDiff) and abs(yDiff) >= self.attraction:
            #Further away in y plane
            self.attract_y_plane(yDiff)

        elif abs(yDiff) < self.attraction and abs(xDiff) < self.attraction:
            print("in attract range move random")
        else:
            print("Choosing random attract " + str(self.attraction) + " / " + str(xDiff) + " " + str(yDiff))
            #Equal distance to attract in x and y, move randomly
            randomBoolean = bool(getrandbits(1))
            if randomBoolean is True:
                self.attract_x_plane(xDiff)
            else:
                self.attract_y_plane(yDiff)

    def attract_x_plane(self,xDiff):
        """Move the object in x plane"""
        if xDiff > 0:
            # self.moveLeftCount += 1
            print(self.name + " increment Left " + str(xDiff))
            self.moveLeftCount += 1
        else:
            # self.moveRightCount += 1
            self.moveRightCount += 1
            print(self.name + " increment Right " + str(xDiff))

    def attract_y_plane(self, yDiff):
        """Move object in y plane"""
        if yDiff > 0:
            print(self.name + " increment up " + str(yDiff))
            self.moveUpCount += 1
        else:
            print(self.name + " increment down " + str(yDiff))
            self.moveDownCount += 1

    def set_repulsion(self, newRepulsion):
        self.repulsion = newRepulsion

    def set_attraction(self, newAttraction):
        self.attraction = newAttraction

    def get_repulsion(self):
        return self.repulsion

    def get_attraction(self):
        return self.attraction

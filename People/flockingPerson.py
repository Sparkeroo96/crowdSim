#Class is person except they now have flocking functionality
#Created by Sam Parker 13/11/18

from People.person import Person

class flockingPerson(Person):

    repulsion = 2
    attraction = 5

    def action(self):
        objects = self.map.get_objects_in_range(self, flockingPerson, self.coordinates, self.sight)
        self.move_with_direction(objects)

    def move_with_direction(self, direction):
        """Move in the direction given"""
        print("Move direction ")

    def choose_move_direction(self,objects):
        """Chooses the best direction to move in based on nearby objects"""
        moveUpCount = 0
        moveDownCount = 0
        moveLeftCount = 0
        moveRightCount = 0

        for obj in objects:
            xDiff = self.coordinates[0] - obj['coordinates'][0]
            yDiff = self.coordinates[1] - obj['coordinates'][1]

            if xDiff <= self.repulsion and xDiff > 0:
                #If object is to close and to the right
                moveLeftCount += 1
                continue
            elif abs(xDiff) <= self.repulsion:
                #obj is to close to the left
                moveRightCount += 1
                continue
            elif yDiff <= self.repulsion and yDiff > 0:
                #obj is too close and below
                moveUpCount += 1
                continue
            elif abs(yDiff)<= self.repulsion:
                #obj to close and above
                moveDownCount += 1;
                continue

    def choose_attract_direction(self, xDiff, yDiff):

        if abs(xDiff) > abs(yDiff):
            print("x")
            if xDiff > 0:
                return "left"
            else:
                return "right"

        elif abs(yDiff) > abs(xDiff):
            print("y")
            if yDiff > 0:
                return "up"
            else:
                return "down"

        else:
            print("Random")



    def set_repulsion(self, newRepulsion):
        self.repulsion = newRepulsion

    def set_attraction(self, newAttraction):
        self.attraction = newAttraction

    def get_repulsion(self):
        return self.repulsion

    def get_attraction(self):
        return self.attraction

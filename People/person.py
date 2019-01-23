# Class is the generic class for people moving around a board
# Created by Sam 23/10/2018
from random import randint
from People.stateMachine import StateMachine
from Algorithm import a_starv2
import math
import time

# data = map_data()
class Person:
    coordsToMove = []
    coordinates = [50, 50]
    #Was size but chris has angle and width so using that instead
    size = [30,10]
    angle = 30
    width = 10
    name = ""
    # map is None
    map = 0
    sight = 8
    #Persons colour for display on map
    colour = [255, 0, 0]
    shape = "circle"
    counter = 0
    """There are cords contained within the path finding array"""

    rememberedObj = ""
    rememberedCoords = []

    # Persons "needs" first value is importance second is how much they want to do it
    #Not in use currently might remove them
    needs = [["toilet", 1, 0],
             ["thirst", 2, 0],
             ["entertainment", 3, 0],
             ["freshAir", 3, 0]
            ]

    defaultState = "greatestNeed"
    currentState = "greatestNeed"
    stateMachine = ""

    states = {
        "greatestNeed": [["usedToilet", "drinkDrink", "danced"], ["wantDrink", "wantToilet", "wantDance"]],

        "wantDrink": [["isGreatestNeed"], ["findBar", "orderDrink"]],
        "findBar": [["notAtBar"], ["moveToBar"]],
        "moveToBar": [["found", "notFound"], ["orderDrink", "moveToBar"]],
        "orderDrink": [["atBar"], ["drink"]],
        "drink": [["getDrink"], ["greatestNeed"]],

        "wantDance": [["isGreatestNeed"], ["dance", "findDanceFloor"]],
        "findDanceFloor": [["notAtDanceFloor", "notFound"], ["moveToDanceFloor"]],
        "moveToDanceFloor": [["notAtDanceFloor", "found"], ["dance", "moveToDanceFloor"]],
        "dance": [["atDanceFloor"], ["greatestNeed"]],

        "wantToilet": [["isGreatestNeed"], ["findToilet", "useToilet"]],
        "findToilet": [["notAtToilet"], ["moveToilet"]],
        "moveToilet": [["foundToilet", "notFoundToilet"], ["moveToilet", "useToilet"]],
        "useToilet": [["atToilet"], ["greatestNeed"]],
    }
    # gender = "" Use this one to determine which bathroom, later

    def __init__(self, name, coords, size):
        self.name = name

        if coords:
            self.coordinates = coords
        if size:
            self.size = size
        else:
            self.size = [30,10]

        self.stateMachine = StateMachine("person")
        self.add_states_to_machine()

        self.currentState = self.defaultState
        self.stateMachine.set_current_state(self.currentState)

        """These cords store waypoints needed to move using a*"""
        cords = []
        self.cords = cords

    def add_map(self, newMap, newCoordinates):
        """Storing the generated map"""
        self.map = newMap
        self.coordinates = newCoordinates

    def startingLoc(self):
        return [2,3]


    def action(self):
        """What the person is going to do"""
        #print("Current state " + str(self.currentState))

        # return self.random_move()
        randomNumber = randint(0, 10)
        if self.cords:
            return self.aStarMove()
        elif randomNumber <= 8:
            return self.random_move()
        elif randomNumber >= 9:
            return self.aStarMove()

        stateAction = self.get_state_action()

        if stateAction == "navigateToCoords":
            print("action")

        elif stateAction == "":
            print("no action")
        else:
            self.random_move()
        # return self.random_move()

    def aStarMove(self):
        print("A Star Move triggered on person class by" + str(self.name) + " at cords " + str(self.coordinates))
        newCoordinates = self.logical_move()
        print("A Star cords" + str(newCoordinates))
        if isinstance(newCoordinates, list):
            # print("person" + self.name + str(newCoordinates))
            self.coordinates = newCoordinates

    def random_move(self):
        """Person moving randomly around the map"""

        randomNumber = randint(0, 12)



        newCoordinates = 0
        # print(self.name + " random number " + str(randomNumber) + " -- initial coords " + str(self.coordinates))
        """Random Movement"""
        if randomNumber <= 2: #person move up
            newCoordinates = [self.coordinates[0], self.coordinates[1] - 10]
        elif randomNumber == 4: #Person move down
            newCoordinates = [self.coordinates[0], self.coordinates[1] + 10]
        elif randomNumber <= 6: #person move right
            newCoordinates = [self.coordinates[0] + 10, self.coordinates[1]]
        elif randomNumber >= 8:
            if self.name == "person 1":
                self.set_cords_from_algo()
        if isinstance(newCoordinates, list):
            # print("person" + self.name + str(newCoordinates))
            self.coordinates = newCoordinates

    def store_coordinates(self, coordinates):
        """Storing a set of coordinates"""
        self.coordinates = coordinates

    def get_coordinates(self):
        """Getting stored coordinates"""
        return self.coordinates

    def get_angle(self):
        """Returns the objects angle"""
        return self.angle

    def get_width(self):
        """Returns the objects size"""
        return self.width

    def get_size(self):
        """returns persons size"""
        return self.size

    def get_height(self):
        """Returns the objects height"""
        return self.height

    def get_shape(self):
        """Returns the shape of the object to draw"""
        return self.shape

    def get_colour(self):
        """Returns the persons colour"""
        return self.colour

    def get_state_action(self):
        """Causes the person to act based on their current state"""
        print("get state action")

        action = "moveRandom"

        if self.currentState == self.defaultState:
            print(self.name + " in greatest need")
            self.currentState = self.stateMachine.get_next_state()

        if "want" in self.currentState:
            # Person has a want desire
            if self.want_action(self.currentState):
                action = "navigateToCoords"

        elif "find" in self.currentState:
            # Person trying to find an object
            print(self.name + " finding object")
            if self.find_object(self.rememberedObj):
                action = "navigateToCoords"

        elif "move" in self.currentState:
            # Person moving to object
            print(self.name + " Person moving to object")
            action = "navigateToCoords"

        elif self.currentState == "orderDrink":
            # Person is ordering their drink
            print(self.name + " Ordering a drink")

        elif self.currentState == "dance":
            # Person will dance
            print(self.name + " is dancing")
            self.stateMachine.get_next_state()

        return action

    def want_action(self, wantState):
        """The people want to do something"""
        if wantState == "wantDrink":
            print("wantDrink")
            searchObject = "Bar"

        elif wantState == "wantDance":
            print("want dance")
            searchObject = "DanceFloor"

        else:
            print("want Toilet")
            searchObject = "Toilet"

        self.rememberedObj = searchObject

        return self.find_object(searchObject)

    def find_object(self, searchObject):
        """This function does the find function of a person
        :return Returns Ture if there are objects, false if it cant find one
        """
        objects = self.map.get_objects_in_range(searchObject, self.coordinates, self.sight)

        if not objects:
            # This is when there are no objects in range and you want the person to wander to keep looking
            print("no objects in range")
            self.rememberedCoords = "search"
            return False

        else:
            # Objects exist, find out closest
            self.work_out_closest_object(objects)
            return True

    def work_out_closest_object(self, objects):
        """ Works out which of the seen objects are closest"""

        smallestDifference = "null"
        newCoords = []

        for obj in objects:
            objCoords = obj["coordinates"]
            xDiff = abs(self.coordinates[0] - objCoords[0])
            yDiff = abs(self.coordinates[1] - objCoords[1])
            totalDifference = xDiff + yDiff

            if totalDifference < smallestDifference:
                smallestDifference = totalDifference
                newCoords = objCoords

        self.rememberedCoords = newCoords


    def add_states_to_machine(self):
        """This is where the object will add states to its statemachine"""
       # print("Adding states to machine")
        for key, value in self.states.items():
           # print("\ncurrentState " + key)
           # print("currentValue " + str(value))
            self.stateMachine.add_state(key, value[1], value[0])

    def angleMath(self, angle, xcord, ycord, vision):
        """This is the maths that returns the amount the x and y cordianes need to change to produce the cordinates
        of the new loaction
        :pram angle they are are looking at
        :pram xcord of the person who is direction looking
        :pram ycord of the person who is looking
        :pram vision is the lengh that they can see
        :retrun the amount the orignial coordinate would need to change to create the new one
         """
        # These variables will be chnaged into number to change
        veritcal = 0
        horizontal = 0
        # The math.sin and cos works in radians so this converts the number to radians
        angle1 = math.radians(angle)
        # These 4 if statements do the maths that takes the lengh of their vision, and the angle that they are directionLooking
        # then returns the value that the point would have to change

        if 1 <= angle and angle <= 90:
            veritcal = round(vision * math.sin(math.radians(90) - angle1))
            veritcal = veritcal * -1
            # #print(veritcal)
            horizontal = round(vision * math.cos(math.radians(90) - angle1))
            # #print(horizontal)
        if 90 < angle and angle <= 180:
            # #print("BR")
            veritcal = round(vision * math.sin(angle1 - math.radians(90)))
            horizontal = round(vision * math.cos(angle1 - math.radians(90)))
        if 180 < angle and angle <= 270:
            # #print("BL")
            veritcal = round(vision * math.sin(math.radians(270) - angle1))
            horizontal = round(vision * math.cos(math.radians(270) - angle1))
            horizontal = horizontal * -1
        if 270 < angle and angle <= 360:
            # #print('TL')
            veritcal = round(vision * math.cos(math.radians(360) - angle1))
            veritcal = veritcal * -1
            horizontal = round(vision * math.sin(math.radians(360) - angle1))
            horizontal = horizontal * -1
        return [veritcal, horizontal]

    def coords_between_two_points(self, cord1, cord2):
        """This is a funciton the takes 2 coordinates and returns all the cordinates that are between them
        :pram cord1 is the first cordinate
        :pram cord2 is the second
        :retrun is the array of cordinates between the two points
        """
        # Gets the angle of the line
        angleRad = math.atan2(cord2[1] - cord1[1], cord2[0] - cord1[0])
        # Converts it to degrees
        angleDeg = math.degrees(angleRad)
        # works out the distance between the two cordinates
        distance = math.pow(cord1[0] - cord2[0], 2) + math.pow(cord2[1] - cord2[1], 2)
        distanceRoot = math.sqrt(distance)
        result = []
        x = 1
        # Goes though each itoration and works out what the cordiante is and adds it to the array
        while x <= distanceRoot:
            lineCoords = self.angleMath(angleDeg, cord1[0], cord1[1], x)
            result.append(lineCoords)
            print(lineCoords)
            x = x + 1
        return result

    def move_to_closest_node(self):
        current = self.coordinates

    """gets the cord from the a* stuff and returns the cords needed"""
    def set_cords_from_algo(self):
        locations = None
        """Need to change this counter stuff"""
        """If the current cords are the nearest state"""
        while self.find_nearest_waypoint() != self.coordinates:
            self.go_nearest_waypoint()
        locations = a_starv2.run_astar(self.coordinates, self.destination())
        if not locations:
            print("""NO PATH FOUND IN SET CORDS """)
            self.action()
            # print("me" + str(locations))
        else:
            for location in locations:
                self.store_waypoints(location)
                # locations.pop(0)
                # self.cords.append((location[0], location[1]))
                    # coords.append((location[0] * 50, locations[1] * 50))
            # return self.cords

    """Stores the waypoints in cords var"""
    def store_waypoints(self, cord):
        print("CORDS FOR A*" + str(cord))
        self.cords.append((cord[0], cord[1]))

    """Returns the destination the person wants to achieve"""
    """Current Placeholder"""
    def destination(self):
        random = randint(0, 15)
        if random <= 5:
            dest = [450, 450]
        elif random <= 10:
            dest = [100, 0]
        else:
            print("Last Stop")
            dest = [0, 450]
        return dest


    """The person actually knows where to move, unlike random"""
    def logical_move(self):
        # newCoordinates = [400, 100]
        """Cords are actuall present"""
        while self.cords:
            newCoordinates = [self.cords[0][0], self.cords[0][1]]
            if isinstance(newCoordinates, list):

                self.coordinates = newCoordinates
                self.cords.pop(0)
                return newCoordinates
            # print(newCoordinates)

    def find_nearest_waypoint(self):
        cords = []
        currentX = self.coordinates[0]
        currentY = self.coordinates[1]
        currentX = int(50 * round(float(currentX / 50)))
        currentY = int(50 * round(float(currentY / 50)))
        cords.append(currentX)
        cords.append(currentY)
        return cords
        # print(current)

    def go_nearest_waypoint(self):
        dest = self.find_nearest_waypoint()
        current = self.coordinates

        self.coordinates = self.find_nearest_waypoint()

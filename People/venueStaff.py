"""
Class is the staff of the venue
State machine is different to normal person
Created by Sam 24/01/2019
"""

from People.person import Person
from Objects.bar import Bar
from Objects.toilet import Toilet
from Objects.danceFloor import DanceFloor
from random import randint

class VenueStaff(Person):

    colour = (0, 255, 0) #Green

    states = {
        "greatestNeed": [["usedToilet", "servedBar"], ["wantToilet", "workAtBar"]],

        "workAtBar": [["works here"], ["findBar"]],
        "findBar": [["notAtBar"], ["moveToBar"]],
        "moveToBar": [["found", "notFound"], ["moveToBar", "checkWorkingSpaceAtBar"]],
        "checkWorkingSpaceAtBar": [["atBar"], ["findBar", "serveBar"]],
        "serveBar": [["spaceAtBar"], ["greatestNeed"]],

        "wantToilet": [["isGreatestNeed"], ["findToilet", "useToilet"]],
        "findToilet": [["notAtToilet"], ["moveToToilet"]],
        "moveToToilet": [["foundToilet", "notFoundToilet"], ["moveToilet", "useToilet"]],
        "useToilet": [["atToilet"], ["greatestNeed"]],
    }

    working_object = None
    unavailable_objects = None

    def action(self):
        """
        Same as main function just adjusted to have the bar staffs actions as well
        :return:
        """

        self.currentState = self.stateMachine.get_current_state()

        if self.wait_on_action_count():
            return "Waiting"

        stateAction = self.get_state_action()
        print("currentState: " + self.currentState + " / stateAction " + stateAction)

        if stateAction == "navigateToRememberedObj":
            self.navigate_to_remembered_object()

        elif stateAction == "rotate":
            # print("no action")
            self.person_rotate()

        elif stateAction == "wait":
            # The person sits there and waits
            print(self.name + " waiting")

        elif stateAction == "serveDrink":
            self.serve_drink_at_bar()

        else:
            self.random_move()



    def assign_self_working_object(self, obj):
        """
        Attempts to assign self to the working object
        :return: True on success
        """

        if obj.staff_start_working_here() is True:
            self.working_object = obj
            return True

        else:
            self.unavailable_objects.append(obj)
            return False

    def serve_drink_at_bar(self):
        """
        Attempts to serve a drink at the bar if the staff is available
        :return:
        """
        print("here")

    def get_state_action(self):
        action = "moveRandom"

        if self.currentState == self.defaultState:
            self.currentState = self.stateMachine.get_next_state()

        if "want" in str(self.currentState):
            # Person has a want desire
            if self.want_action(self.currentState):
                action = "navigateToRememberedObj"
                self.rotate = 0
                self.advance_state_machine()

            else:
                action = "rotate"

        elif "find" in str(self.currentState):
            action = self.find_action()

        elif "move" in str(self.currentState):
            # Person moving to object
            print(self.name + " Person moving to object")
            action = "navigateToRememberedObj"

            # If the person is next to the thing they are supposed to be on like a bar, advance the state again
            objectSize = [self.rememberedObj.get_width(), self.rememberedObj.get_height()]
            rememberedObjectCoords = self.rememberedObj.get_coordinates()
            rectangleCoordRanges = self.map.get_coordinates_range(rememberedObjectCoords, objectSize)
            selfEdge = self.get_edge_coordinates_array()

            if self.map.check_circle_overlap_rectangle(selfEdge, rectangleCoordRanges):
                print("at target")
                self.advance_state_machine()
            else:
                print("not at target")

        elif self.currentState == "useToilet":

            action = "wait"
            self.use_toilet()
            # Toilet is free and now you are using it
            # self.clear_remembered_object()

        elif "checkWorkingSpaceAt" in self.currentState:
            # Needs to check theres space to work at the bar
            self.check_working_space_at_object()

        return action

    def check_working_space_at_object(self):
        """
        Checks to see if theres space to work at an object
        :return: True on success
        """

        if self.rememberedObj.check_free_staff_space():
            # Only want to do this if can see object
            return True


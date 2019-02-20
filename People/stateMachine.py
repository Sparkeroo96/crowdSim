from random import randint

class StateMachine:

    #Function states which class the machine is for, could be a person
    stateMachineFor = ""
    #Dictionary of possible states
    states = {}
    currentState = ""
    #Needs of a human
    overall_needs = None

    def __init__(self, machineFor):
        self.stateMachineFor = machineFor

    def set_current_state(self, state):
        self.currentState = state

    def add_state(self, stateName, nextState, requirement):
        if stateName not in self.states:
            self.create_new_state(stateName)

        self.add_next_states(stateName, nextState)

        self.states[stateName]["requirement"] = requirement

    def create_new_state(self, stateName):
        """Function creates a brand new state, stops overwriting old data"""
        self.states[stateName] = {}
        self.states[stateName]["requirement"] = []
        self.states[stateName]["nextStates"] = []

    def add_next_states(self, stateName, nextState):
        """Add all of the next states to the dictionarys next states"""
        if isinstance(nextState, list) is False:
            self.states[stateName]["nextStates"].append(nextState)
            return

        for state in nextState:
            self.states[stateName]["nextStates"].append(state)

    def get_current_state(self):
        return self.currentState

    def get_current_state_properties(self):
        currentState = self.get_current_state()
        return self.get_state(currentState)

    def get_state(self, stateName):
        return self.states.get(stateName)

    def get_state_next_states(self, stateName):
        state = self.get_state(stateName)
        print("stateName: " + stateName)
        print("stateNameNextStates:" + str(state["nextStates"]))
        return state["nextStates"]

    def get_state_requirment(self, stateName):
        state = self.get_state(stateName)
        return state["requirement"]

    def get_states(self):
        """Returns all possible states for this machine
        @:return returns an array of possible options
        """
        return self.states.keys()

    def get_stateMachineFor(self):
        """Tells you what object this state machine is for"""
        return self.stateMachineFor

    def check_next_state_fine(self, nextState):
        """Checks to see if the next state is fine,
        @:param nextState the state you wish to be in
        @:return Returns true if fine, false if not
        """
        nextStates =  self.states[self.currentState][nextState]

        for x in nextStates:
            if x == nextState:
                print(nextState + " is a possible next state")
                return True

        return False

    """
    Once there is a need within the idle state, we need to pass
    the next state to start the right SM transitions.
    
    :param n = need of person
    """
    def get_need_state(self, n):
        nextStates = self.get_state_next_states(self.currentState)
        need = n
        for state in nextStates:
            if str(need) in state:
                self.set_current_state(state)
                return state

    def get_next_state(self):
        """Function gets next state and moves into it"""
        nextStates = self.get_state_next_states(self.currentState)

        statesCount = len(nextStates)
        if statesCount == 1:
            #Only 1 next state, moving there
            selectedNextState = nextStates[0]

        else:
            """Need to remove the random off the next state"""
            selectedNextState = self.__get_random_next_state(nextStates, statesCount)

        # selectedNextState =  "wantDrink"
        """THIS IS WHERE THE STATE CHANGES"""
        # selectedNextState =  "wantToilet"


        self.set_current_state(selectedNextState)

        return selectedNextState

    def __get_random_next_state(self, nextStates, statesCount):
        """Function randomly picks a next state from the given next options,
        Don't call this function call get_next_state
        """
        print("statesCount " + str(statesCount))
        random = randint(0, statesCount - 1)
        return nextStates[random]

    def choose_next_state(self, nextState):
        """
        Function moves to given state if possible
        :param nextState: The state you want to move to
        :return: True on success
        """
        possibleNextStates = self.get_state_next_states(self.currentState)

        for state in possibleNextStates:
            if state == nextState:
                self.currentState = nextState
                return nextState

        return False

    def set_current_needs(self, needs):
        self.overall_needs = needs

    def get_current_needs(self):
        return self.overall_needs



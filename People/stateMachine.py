
class StateMachine:

    #Function states which class the machine is for, could be a person
    stateMachineFor = ""
    #Dictionary of possible states
    states = {}
    currentState = ""

    def __init__(self, machineFor):
        self.stateMachineFor = machineFor

    def set_current_state(self, state):
        self.currentState = state

    def add_state(self, stateName, nextState, requirement):
        if stateName not in self.states:
            self.createNewState(stateName)

        self.addState(stateName, nextState)

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

    def get_state_next_states(self,stateName):
        state = self.get_state(stateName)
        return state["nextStates"]

    def get_state_requirment(self, stateName):
        state = self.get_state(stateName)
        return state["requirement"]

    def get_states(self):
        """Returns all possible states for this machine"""
        return self.states.keys()

    def get_stateMachineFor(self):
        return self.stateMachineFor
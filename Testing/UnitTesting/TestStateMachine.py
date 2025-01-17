import unittest
from People import stateMachine
import numpy

class TestStateMachine(unittest.TestCase):
    def setUp(self):
        """Needed to set up an instance of a state machine."""

        """Set up a state machine instance"""
        self.test_machine = stateMachine.StateMachine("test")
        """Set up states for machine"""
        self.states = {
            "state 1": [["req 1"], ["state 2", "state 3"]],
            "state 2": [["req 2"], ["state 3"]],
            "state 3": [["req 3"], ["state 4"]],
            "state 4": [[], ["state 1"]],
        }
        """Add the states in the machine"""
        for key, value in self.states.items():
            self.test_machine.add_state(key, value[1], value[0])

        """Begin state machine on state 1"""
        self.test_machine.set_current_state("state 1")

    def test_get_current_state(self):
        """
        Tests if the current state is initiated and set to 'state 1'
        """
        result = self.test_machine.get_current_state()
        self.assertEqual(result, "state 1")

    def test_get_current_state_properties(self):
        """
        Test to see if get current state properties outputs the states it is linked to

        """

        result = self.test_machine.get_current_state_properties()
        self.assertTrue(result)

    def test_next_states(self):
        """
        Tests if the get state next states returns the states linked
        Testing state 4s' next states
        :return: True, 'State 1'
        """
        result = self.test_machine.get_state_next_states("state 4")
        self.assertTrue(result)

    def test_get_next_state_random_option(self):
        result = self.test_machine.get_next_state()
        intended_results = self.test_machine.get_state_next_states("state 1")
        self.assertIn(result, intended_results)

    def test_get_next_state_only_one_option(self):
        self.test_machine.set_current_state("state 4")
        result = self.test_machine.get_next_state()
        intended_result = "state 1"
        self.assertEqual(result, intended_result)

    def test_choose_next_state_true(self):
        result = self.test_machine.choose_next_state("state 2")
        self.assertEqual(result, "state 2")

    def test_choose_next_state_false(self):
        result = self.test_machine.choose_next_state("state 4")
        self.assertFalse(result)


    def test_get_all_states(self):
        """
        Tests to see if all states are returned in a given state machine
        :return:
        """
        result = self.test_machine.get_all_states()
        for r in result:
            self.assertIn(r, result)








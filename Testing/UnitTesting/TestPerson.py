import unittest
from People import *
from People.person import Person
from Objects.bar import Bar
from Algorithm import a_starv2
import numpy


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.testPerson = person.Person("person 1", [100, 100], 10, 0, 0)

        self.testPerson2 = person.Person("person 2", [20, 30], 10, 0, 0)
        self.newBar = Bar([450, 450], "Bar", 30, 20)
        self.testPerson2.add_to_memory(self.newBar)
    def test_set_up(self):
        """
        Testing the setup method
        :return: True as the persons name is "person 1"
        """
        result = "person 1"
        self.assertEqual(self.testPerson.get_name(), result)

    # def test_person_memory(self):
    #     """TO DO"""
    #     """SHOULD PASS BUT TESTPERSON PICKS UP THE MEMORY"""
    #     self.assertFalse(self.testPerson.memory, {'Bar': [], 'DanceFloor': [], 'Toilet': []})

    def test_person_rotate(self):
        """
        Tests if person rotates 30 degrees
        Start = 0
        Return 30
        :return: True as person has rotated 30 degrees
        """
        result = 30
        self.assertEqual(self.testPerson.person_rotate(), result)

    # def test_get_closest_object_from_memory(self):
    #     """
    #     TEST FAILS - Should return false as testperson has not added bar into memory
    #     :return:
    #     """
    #     self.assertEqual(self.testPerson.get_closest_object_from_memory("Bar"), False)

    def test_find_object_true(self):
        """
        Tests if it can find object. Should resturn true as it does not have bar in memory
        :return:
        """
        self.assertTrue(self.testPerson2.find_object("Bar"))

    def test_get_edge_coordinates_array(self):
        """
        Tests to see if the edge coordinates get printed
        :return:
        """
        data = [101, 101]
        self.assertTrue(self.testPerson.get_edge_coordinates_array(data))

    def test_find_nearest_waypoint(self):
        self.assertEqual(self.testPerson2.find_nearest_waypoint(), [0, 50])

    def test_coords_between_two_points(self):
        """
        FUNCTION CURRENTLY NOT IN USE
        :return:
        """
        data_cord1 = [0, 0]
        data_cord2 = [2, 2]
        self.assertTrue(self.testPerson.coords_between_two_points(data_cord1, data_cord2))

    def test_navigate_to_remembered_object(self):
        print("to do")

    def test_set_cords_from_algo(self):
        print("to do")

    def test_store_waypoints(self):
        """
        Tests the store waypoints function appends to the cords variable in order for a* to trigger
        """
        data = [0, 450]
        self.testPerson.store_waypoints(data)
        self.assertListEqual(self.testPerson.cords, [(0, 450)])

    # def test_set_cords_from_algo_second(self):
    #     a_starv2.store_all_nodes(numpy.zeros((10, 10), int))
    #     self.testPerson2.coordinates = self.testPerson2.find_nearest_waypoint()
    #     print(self.testPerson2.coordinates, self.testPerson2.destination())
    #     self.testPerson2.set_cords_from_algo()
    #     self.assertFalse(self.testPerson.cords)
    # def test_move(self):
    #     data = [200, 200]
    #     self.assertTrue(self.testPerson.move(data))


if __name__ == '__main__':
    unittest.main()
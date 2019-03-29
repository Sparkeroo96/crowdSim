import unittest
from Data import map_data
from unittest.mock import MagicMock
from People import person
from Objects import bar
from unittest import mock

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        """Creating a map"""
        self.map = map_data.map_data(None, 0)
        """Map default generates all the people on a map"""
        """First person in the map data array"""
        self.testPerson1 = self.map.mapData[0]

    def test_map_data(self):
        """
        Tests map data is generated when setting up map_default
        :return:
        """
        self.assertIsNotNone(self.map.mapData)

    def test_check_coordinates_for_person(self):
        print("to do")
        # self.map.check_coordinates_for_person()

    def test_get_edge_coordinates_array(self):
        """
        Test the cords are [0, 50]
        """
        self.assertEqual(self.testPerson1.get_coordinates(), [0, 50])
        test_current_cords = self.testPerson1.get_coordinates()
        """Test to check if the get edge coords array returns the coords around the current cords"""
        self.assertTrue(self.testPerson1.get_edge_coordinates_array(test_current_cords))

    # def test_get_object_colour_code(self):
    #     """
    #     tests the object colour code. I've used a person to test this
    #     :return: True. RGB value of 255, 0, 0 (Red for a person)
    #     """
    #     result = self.map.get_object_colour_code("Person")
    #     self.assertEqual(result, [255, 0, 0])

    def test_mock(self):
        """
        Testing the mock classes
        :return:
        """
        mock = MagicMock(name="test")
        mock.return_value = 30000


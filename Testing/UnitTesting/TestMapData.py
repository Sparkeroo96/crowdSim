import unittest
from Data import map_data

import numpy

class TestMapData(unittest.TestCase):
    def setUp(self):
        self.test_map = map_data.map_data(None, 0)

    # def test_map_default(self):
    #     """
    #     Tests the map_default method. This will return true if the array is generated with the corresponding adding
    #     :return: Trey
    #     """
    #     self.assertTrue(self.test_map.map_default())

    def test_add_people_to_map(self):
        """
        Tests the add people to map function
        :return:
        """
        """Adding no one to the map should return false"""
        self.assertFalse(self.test_map.add_people_to_map(0))
        """Adding one person will assert true"""
        self.assertFalse(self.test_map.add_people_to_map(1))
        with self.assertRaises(TypeError):
            result = self.test_map.add_people_to_map("test")

    def test_get_object_colour_code(self):
        print("to do")

    def test_person_vision(self):
        data_x1 = 50
        data_y1 = 50
        data_angle = 30
        data_vision = None
        """Tests if array is printed"""
        self.assertTrue(self.test_map.personVision(data_x1, data_y1, data_angle, data_vision))

    def test_angleMath(self):
        data_angle = 30
        data_xcord = 50
        data_ycord = 50
        data_vision = 100
        """Checks it returns an array"""
        self.assertTrue(self.test_map.angleMath(data_angle, data_xcord, data_ycord, data_vision))

    def test_check_coordinates_for_person(self):
        print("to do")

    def test_check_circle_touch(self):
        print("to do - Need to create instances of people for this")

    def test_check_person_touching_object(self):
        print("to do - Need to create a rect and a circle to test")

    def test_check_circle_overlap_rectangle(self):
        print("to do - Need to create a rect and a circle to test")

    def test_add_bar_to_map(self):
        """Adding no one to the map should return false"""
        self.assertFalse(self.test_map.add_bar_to_map(0))
        print("to do")

    def test_get_coordinates_range(self):
        print("to do - Need to have an object created")

    def test_what_object(self):
        print("to do - Need to create an instance of mapdata")

    def test_point_in_coordinates_range(self):
        data_range = {"X": [190, 210], "Y":[190, 210]}
        """Test to check the cordinates are inside the boundaries"""
        data_coordinates_true = [200, 200]
        self.assertTrue(self.test_map.point_in_coordinates_range(data_coordinates_true, data_range))
        """Test to check coords outside of boundaries returns false"""
        data_coordinates_false = [220, 220]
        self.assertFalse(self.test_map.point_in_coordinates_range(data_coordinates_false, data_range))
        """Check incorrect parameters are false"""

    def test_person_eyes(self):
        print("to do")

    def test_add_wall_to_map(self):
        """Adds the walls into the map"""
        self.test_map.add_wall_to_map()
        """Asserts true if the walls have been added to the map"""
        self.assertTrue(self.test_map.mapData)

    def test_set_nodes(self):
        print("to do")

    def test_add_toilet_to_map(self):
        self.test_map.add_toilet_to_map(1)
        """Checks toilet has been added to mapdata"""
        self.assertTrue(self.test_map.mapData)
        print("to do - Test assetion of a list to check if toilet exists")

    def test_add_dancefloor_to_map(self):
        print("to do")

    def test_generate_nodes(self):
        print("to do")
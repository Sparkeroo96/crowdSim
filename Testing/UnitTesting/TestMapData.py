import unittest
from Data import map_data
from People import person
from test import RunningMain

import numpy

class TestMapData(unittest.TestCase):
    def setUp(self):
        self.test_map = map_data.map_data(None, 0)
        self.test_person = person.Person("person 1", [100, 100], 10, 0, 0)

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
        """Adding one person will assert true"""
        # self.gui = RunningMain()
        # test_map2 = map_data.map_data(gui, 0)
        # test_coords = self.test_person.get_coordinates()
        # test_size = self.test_person.get_width()
        # test_angle = self.test_person.get_angle()
        # self.assertTrue(test_map2.add_people_to_map(test_coords, test_size, test_angle))
        # with self.assertRaises(TypeError):
        #     result = test_map2.add_people_to_map("test", "test", "test")

    def test_person_vision_true(self):
        data_x1 = 50
        data_y1 = 50
        data_angle = 30
        data_vision = None
        result = self.test_map.personVision(data_x1, data_y1, data_angle, data_vision)
        self.assertTrue(result)

    def test_person_vision_false(self):
        data_x1 = 50
        data_y1 = 50
        data_angle = 30
        data_vision = None
        result = self.test_map.personVision(data_x1, data_y1, data_angle, data_vision)
        self.assertNotIn(result, [200, 200])

    def test_angleMath_true(self):
        data_angle = 30
        data_xcord = 50
        data_ycord = 50
        data_vision = 100
        result = self.test_map.angleMath(data_angle, data_xcord, data_ycord, data_vision)
        """Checks it returns an array"""
        print(result)
        self.assertEqual(result, [-86, 49])

    def test_angleMath_false(self):
        data_angle = 30
        data_xcord = 50
        data_ycord = 50
        data_vision = 100
        result = self.test_map.angleMath(data_angle, data_xcord, data_ycord, data_vision)
        """Checks it returns an array"""
        self.assertNotEqual(result, [90, 90])

    def test_check_coordinates_for_person(self):
        print("to do - need to have map and agents together.")

    def test_check_coordinates_in_bounds(self):
        print("Need a gui for one of the vars.")

    def test_check_circle_touch(self):
        print("to do - Need to create instances of people for this")

    def test_check_person_touching_object(self):
        print("to do - Need to create a rect and a circle to test")

    def test_check_circle_overlap_rectangle(self):
        print("to do - Need to create a rect and a circle to test")

    def test_add_bar_to_map(self):
        """Adding no one to the map should return false"""
        # self.assertTrue(self.test_map.add_bar_to_map([100, 100], 20, 20))

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
        # self.test_map.add_wall_to_map()
        # """Asserts true if the walls have been added to the map"""
        # self.assertTrue(self.test_map.mapData)

    def test_set_nodes(self):
        print("to do")

    def test_add_toilet_to_map(self):
        # self.test_map.add_toilet_to_map([200, 200], 20, 20)
        """Checks toilet has been added to mapdata"""
        # self.assertTrue(self.test_map.mapData)
        print("to do - Test assetion of a list to check if toilet exists")

    def test_add_dancefloor_to_map(self):
        print("to do")

    def test_generate_nodes(self):
        print("No return")

    def test_calculate_distance_between_two_points_true(self):
        test_c1 = [0, 0]
        test_c2 = [20, 0]
        result = self.test_map.calculate_distance_between_two_points(test_c1, test_c2)
        self.assertEqual(result, 20)

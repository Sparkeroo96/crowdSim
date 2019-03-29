import unittest
from Algorithm import a_starv2
import numpy

class TestAStar(unittest.TestCase):
    def test_astar(self):
        """
        Tests to see if a destination outside of its normal bounds returns false
        :return: False
        """
        test_array = numpy.zeros((10, 10), int)
        test_start = (0, 0)
        test_dest = (1, 11)
        result = a_starv2.astar(test_array, test_start, test_dest)
        self.assertFalse(result)

    def test_run_astar_no_grid(self):
        test_start = [0, 0]
        test_dest = [300, 300]
        result = a_starv2.run_astar(test_start, test_dest)
        self.assertFalse(result)

    def test_run_astar_with_waypoints(self):
        """Needs tweaking"""
        test_start = [0, 0]
        test_dest = [350, 350]
        a_starv2.store_all_nodes(numpy.zeros((10, 10), int))
        result = a_starv2.run_astar(test_start, test_dest)
        self.assertFalse(result)

    def test_astar_dest_outside_grid(self):
        """
        Tests to see if a destination outside of its normal bounds returns True
        :return: False
        """
        test_array = numpy.zeros((10, 10), int)
        test_start = (0, 0)
        test_dest = (1, 19)
        result = a_starv2.astar(test_array, test_start, test_dest)
        self.assertFalse(result)

    def test_astar_type_error(self):
        """
        Tests to see if a type error occurs on astar with an invalid string.
        :return: TypeError
        """
        test_array = numpy.zeros((10, 10), int)
        test_start = "1, 10"
        test_dest = (1, 9)
        with self.assertRaises(TypeError):
            result = a_starv2.astar(test_array, test_start, test_dest)
        test_start = [200, 400]
        with self.assertRaises(TypeError):
            result = a_starv2.astar(test_array, test_start, test_dest)

    def test_heuristic(self):
        """
        Test the heuristic function returns distance
        :return:
        """
        test_a = (0, 40)
        test_b = (4, 40)
        result = a_starv2.heuristic(test_a, test_b)
        self.assertEqual(result, 16)

    def test_return_waypoints(self):
        """
        Test to check return waypoints returns unique values when passed through if statements
        :return:
        """
        data = [(0, 0), (1, 1), (3, 3)]
        result = a_starv2.return_waypoints(data)
        self.assertEqual(result, data)

    def test_return_waypoints_removing_unneccesary_points(self):
        """
        Test to check return waypoints returns unique values when passed through the if statements
        :return:
        """
        data = [(0, 0), (1, 1), (1, 2), (1, 3), (3, 3)]
        expected_result = [(0, 0), (1, 1), (3, 3)]
        result = a_starv2.return_waypoints(data)
        self.assertEqual(result, expected_result)

    def test_return_waypoints_with_one_result(self):
        """
        Test to check return waypoints returns one value as a waypoint
        :return: True, as there is only one data value in the starting array
        """
        data = [(0, 0)]
        result = a_starv2.return_waypoints(data)
        self.assertEqual(result, [(0, 0)])

    def test_return_waypoints_with_no_result(self):
        """
        Test to check return waypoints returns one value as a waypoint
        :return: True, as there is only one data value in the starting array
        """
        data = []
        result = a_starv2.return_waypoints(data)
        self.assertEqual(result, None)

    def test_convert_to_simple(self):
        """
        Test to see if convert to simple converts two numbers to simpliefied coords
        The coords are in multiples of 20.
        :return: True
        """
        data = [240, 430]
        result = a_starv2.convert_to_simple(data)
        self.assertEqual(result, (12, 21))

    def test_convert_to_simple_negative_numbers(self):
        """
        Test to see if converting two negative numbers turns the result into 0, 0
        :return: True if converted correctly
        """
        data = [-20, -70]
        result = a_starv2.convert_to_simple(data)
        self.assertEqual(result, (0, 0))

    def test_convert_to_simple_false(self):
        """
        Test to see if converting two negative numbers turns the result into 0, 0
        :return: True if converted correctly
        """
        data = None
        result = a_starv2.convert_to_simple(data)
        self.assertFalse(result)

    def test_locations(self):
        """
        Test to see if the correspondng coords are converted to usable coords
        :return: True
        """
        data = [(0, 0), (1, 1), (2, 2)]
        intended_result = [(0, 0), (20, 20), (40, 40)]
        result = a_starv2.locations(data)
        self.assertEqual(result, intended_result)

    def test_store_node_details(self):
        test_locations = [[0, 0], [20, 20]]
        result = a_starv2.store_node_details(test_locations)
        self.assertTrue(result, test_locations)

    def test_get_open_nodes(self):
        test_open_nodes = [[0, 0], [10, 10]]
        test_result = [[0, 0], [200, 200]]
        a_starv2.set_open_nodes(test_open_nodes)
        result = a_starv2.get_open_nodes()
        self.assertEqual(result, test_result)

    def test_get_random_waypoint(self):
        test_open_nodes = [[0, 0], [10, 10]]
        test_result = [[0, 0], [200, 200]]
        a_starv2.set_open_nodes(test_open_nodes)
        result = a_starv2.get_random_waypoint()
        print(result)
        self.assertIn(result, test_result)


if __name__ == '__main__':
    unittest.main()


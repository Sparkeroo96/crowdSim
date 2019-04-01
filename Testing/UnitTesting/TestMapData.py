import unittest
from Data import map_data
from People import person
from Objects import wall
from Objects import bar


class TestMapData(unittest.TestCase):
    def setUp(self):
        self.test_map = map_data.map_data(None, 0)
        self.test_person = person.Person("person 1", [100, 100], 10, 0, 0)

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
        self.assertEqual(result, [-86, 49])

    def test_angleMath_with_a_different_angle(self):
        data_angle = 200
        data_xcord = 50
        data_ycord = 50
        data_vision = 100
        result = self.test_map.angleMath(data_angle, data_xcord, data_ycord, data_vision)
        """Checks it returns an array"""
        self.assertEqual(result, [93, -34])

    def test_angleMath_false(self):
        data_angle = 30
        data_xcord = 50
        data_ycord = 50
        data_vision = 100
        result = self.test_map.angleMath(data_angle, data_xcord, data_ycord, data_vision)
        """Checks it returns an array"""
        self.assertNotEqual(result, [90, 90])

    def test_point_in_coordinates_range(self):
        data_range = {"X": [190, 210], "Y":[190, 210]}
        """Test to check the cordinates are inside the boundaries"""
        data_coordinates_true = [200, 200]
        self.assertTrue(self.test_map.point_in_coordinates_range(data_coordinates_true, data_range))
        """Test to check coords outside of boundaries returns false"""
        data_coordinates_false = [220, 220]
        self.assertFalse(self.test_map.point_in_coordinates_range(data_coordinates_false, data_range))
        """Check incorrect parameters are false"""

    def test_get_coordinates_range_not_list(self):
        test_coordinates = [100, 100]
        test_object_size = 20
        result = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        self.assertTrue(result)

    def test_import_from_file_false(self):
        test_file = "../../maps_saves"
        save_name = "testdsa"
        result = self.test_map.import_from_file(test_file, save_name)
        self.assertFalse(result)

    def test_import_from_file_true(self):
        test_width = 100
        test_height = 100
        self.test_map.set_size_screen(test_height, test_width)
        test_file = "../../maps_saves"
        save_name = "test2"
        result = self.test_map.import_from_file(test_file, save_name)
        self.assertTrue(result)

    def test_check_save_name_true(self):
        test_file = "../../maps_saves"
        save_name = "test_new_map"
        result = self.test_map.check_save_name(test_file, save_name)
        self.assertTrue(result)

    def test_check_save_name_false(self):
        test_file = "../../maps_saves"
        save_name = "test2"
        result = self.test_map.check_save_name(test_file, save_name)
        self.assertFalse(result)

    def test_export_true(self):
        test_file = "../../maps_saves"
        save_name = "testing_map_export"
        test_wall = wall.Wall([200, 200], 200, 100)
        self.test_map.mapData.append(test_wall)
        result = self.test_map.export(test_file, save_name)
        self.assertTrue(result)

    def test_export_false(self):
        test_file = "../../maps_saves"
        save_name = "test2"
        result = self.test_map.export(test_file, save_name)
        self.assertFalse(result)

    def test_set_nodes_values(self):
        test_wall = wall.Wall([200, 200], 200, 100)
        self.test_map.set_nodes_values(test_wall)
        result = self.test_map.values_to_append
        self.assertTrue(result)

    def test_set_nodes_values_negative(self):
        test_wall = wall.Wall([200, 200], -100, -100)
        self.test_map.set_nodes_values(test_wall)
        result = self.test_map.values_to_append
        self.assertTrue(result)

    def test_set_nodes_values_negative_width(self):
        test_wall = wall.Wall([200, 200], 100, -100)
        self.test_map.set_nodes_values(test_wall)
        result = self.test_map.values_to_append
        self.assertTrue(result)

    def test_set_nodes_values_negative_height(self):
        test_wall = wall.Wall([200, 200], -100, 100)
        self.test_map.set_nodes_values(test_wall)
        result = self.test_map.values_to_append
        self.assertTrue(result)

    def test_generate_nodes(self):
        test_width = 100
        test_height = 100
        self.test_map.set_size_screen(test_height, test_width)
        self.test_map.generate_nodes()
        result = self.test_map.open_nodes
        print("Return to this")
        self.assertTrue(result)

    def test_calculate_starting_nodes(self):
        test_width = 20
        test_height = 20
        self.test_map.set_size_screen(test_height, test_width)
        result = self.test_map.calculate_starting_nodes()
        self.assertEqual(result, 1)

    def test_set_grid_area(self):
        test_width = 100
        test_height = 100
        self.test_map.set_size_screen(test_height, test_width)
        self.test_map.set_grid_area()
        result = self.test_map.values_to_append
        self.assertTrue(result)

    def test_get_coordinates_range_list(self):
        test_coordinates = [100, 100]
        test_object_size = [-20, -20]
        result = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        self.assertTrue(result)

    def test_check_circle_overlap_rectangle_true(self):
        test_person_2 = person.Person("person 1", [100, 100], 10, 0, 0)
        test_size = 10
        test_coords = test_person_2.get_coordinates()
        test_edge_coordinates = test_person_2.get_edge_coordinates_array(test_coords, test_size)
        test_coordinates = [100, 100]
        test_object_size = 20
        test_range = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        result = self.test_map.check_circle_overlap_rectangle(test_edge_coordinates, test_range)
        self.assertTrue(result)

    def test_check_circle_overlap_rectangle_false(self):
        test_person_2 = person.Person("person 1", [0, 0], 10, 0, 0)
        test_size = 10
        test_coords = test_person_2.get_coordinates()
        test_edge_coordinates = test_person_2.get_edge_coordinates_array(test_coords, test_size)
        test_coordinates = [100, 100]
        test_object_size = 20
        test_range = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        result = self.test_map.check_circle_overlap_rectangle(test_edge_coordinates, test_range)
        self.assertFalse(result)

    def test_check_person_touching_object_false(self):
        test_person_2 = person.Person("person 1", [0, 0], 10, 0, 0)
        test_size = 10
        test_coords = test_person_2.get_coordinates()
        test_edge_coordinates = test_person_2.get_edge_coordinates_array(test_coords, test_size)
        test_coordinates = [100, 100]
        test_object_size = 20
        test_range = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        result = self.test_map.check_circle_overlap_rectangle(test_edge_coordinates, test_range)
        self.assertFalse(result)

    def test_check_person_touching_object_true(self):
        test_person_2 = person.Person("person 1", [110, 110], 10, 0, 0)
        test_size = 10
        test_coords = test_person_2.get_coordinates()
        test_edge_coordinates = test_person_2.get_edge_coordinates_array(test_coords, test_size)
        test_coordinates = [100, 100]
        test_object_size = 20
        test_range = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        print(test_edge_coordinates)
        print(test_range)
        result = self.test_map.check_circle_overlap_rectangle(test_edge_coordinates, test_range)
        self.assertTrue(result)

    def test_check_person_touching_object_overlap_true(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        test_coords = test_person.get_coordinates()
        test_width = round(test_person.width / 2)
        test_edge = test_person.get_edge_coordinates_array(test_coords, test_width)
        test_coordinates = [100, 100]
        test_object_size = 20
        test_coord_range = self.test_map.get_coordinates_range(test_coordinates, test_object_size)
        result = self.test_map.check_person_touching_object(test_edge, test_coord_range)
        self.assertTrue(result)

    # def test_get_edge_coordinates_array(self):
    #     test_person_2 = person.Person("person 1", [100, 100], 10, 0, 0)
    #     test_size = 10
    #     test_coords = test_person_2.get_coordinates()
    #     test_edge_coordinates = test_person_2.get_edge_coordinates_array(test_coords, test_size)

    def test_what_object_true(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        self.test_map.mapData.append(test_person)
        test_person_coords = self.test_person.get_coordinates()
        result = self.test_map.what_object(test_person_coords, False)
        self.assertTrue(result)

    def test_what_object_searching_people(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        self.test_map.mapData.append(test_person)
        test_person_coords = self.test_person.get_coordinates()
        result = self.test_map.what_object(test_person_coords, True)
        self.assertTrue(result)

    def test_check_circle_touch_no_overlap(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        test_person2 = person.Person("person 1", [200, 100], 10, 0, 0)
        person1 = {
            "radius": test_person.get_width() / 2,
            "xCoord": test_person.get_coordinates()[0],
            "yCoord": test_person.get_coordinates()[1]
        }
        person2 = {
            "radius": test_person2.get_width() / 2,
            "xCoord": test_person2.get_coordinates()[0],
            "yCoord": test_person2.get_coordinates()[1]
        }
        result = self.test_map.check_circle_touch(person1, person2)
        self.assertEqual(result, -1)

    def test_check_circle_touch_overlap(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        test_person2 = person.Person("person 1", [104, 100], 10, 0, 0)
        person1 = {
            "radius": test_person.get_width() / 2,
            "xCoord": test_person.get_coordinates()[0],
            "yCoord": test_person.get_coordinates()[1]
        }
        person2 = {
            "radius": test_person2.get_width() / 2,
            "xCoord": test_person2.get_coordinates()[0],
            "yCoord": test_person2.get_coordinates()[1]
        }
        result = self.test_map.check_circle_touch(person1, person2)
        self.assertEqual(result, 0)

    def test_check_circle_touch_touching(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        test_person2 = person.Person("person 1", [110, 100], 10, 0, 0)
        person1 = {
            "radius": test_person.get_width() / 2,
            "xCoord": test_person.get_coordinates()[0],
            "yCoord": test_person.get_coordinates()[1]
        }
        person2 = {
            "radius": test_person2.get_width() / 2,
            "xCoord": test_person2.get_coordinates()[0],
            "yCoord": test_person2.get_coordinates()[1]
        }
        result = self.test_map.check_circle_touch(person1, person2)
        self.assertEqual(result, 1)

    def test_get_people_within_range_false(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        results = self.test_map.get_people_within_range([100, 100], 10, test_person)
        self.assertFalse(results)

    def test_get_objects_within_range_return_object(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        test_size = 100
        test_coords = test_person.get_coordinates()
        test_edge = test_person.get_edge_coordinates_array(test_coords, test_size)
        test_bar = bar.Bar([0, 0], "test", 200, 500)
        self.test_map.mapData.append(test_bar)
        result = self.test_map.get_objects_within_range([50, 50], 100, test_edge, test_person)
        self.assertIs(result[0], test_bar)

    def test_calculate_distance_between_two_points_true(self):
        test_c1 = [0, 0]
        test_c2 = [20, 0]
        result = self.test_map.calculate_distance_between_two_points(test_c1, test_c2)
        self.assertEqual(result, 20)

    def test_delete_object(self):
        result = self.test_map.mapData
        test_wall = wall.Wall([400, 400], 100, 100)
        self.test_map.mapData.append(test_wall)
        print(self.test_map.get_map())
        self.assertTrue(result)
        self.test_map.delete_object([401, 401])
        self.assertNotIn(result, self.test_map.get_map())
        self.assertFalse(result)

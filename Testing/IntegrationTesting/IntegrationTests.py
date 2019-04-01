import unittest
from Data import map_data
from unittest.mock import MagicMock
from People import person
from Objects.bar import Bar
from Objects.toilet import Toilet
from unittest import mock
from test import RunningMain
from Objects.danceFloor import DanceFloor
from People.person import Person


class Mock():
    def get_offset(self):
        return [0, 0]

    def get_sim_screen_width(self):
        return 600

    def get_sim_screen_height(self):
        return 600


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        """Creating a map"""
        self.test_map = map_data.map_data(Mock(), 0)
        self.test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        self.test_person_2 = person.Person("person 2", [200, 200], 10, 0, 0)
        self.test_dancefloor = DanceFloor([300, 300], 30, 30, 30)
        self.test_bar = Bar([400, 400], 30, 30, 30)
        self.test_toilet = Toilet([200, 200], "toilet", 200, 100)
        self.test_map.mapData.append(self.test_person)
        self.test_map.mapData.append(self.test_person_2)
        self.test_map.mapData.append(self.test_dancefloor)

    def test_move_inside_dance_floor(self):
        self.test_person.map = self.test_map
        self.test_person.rememberedObj = self.test_dancefloor
        self.test_person.move_inside_dance_floor()
        result = self.test_person.move(self.test_person.coordinates)
        self.assertTrue(result)

    def test_move_inside_dance_floor_negative(self):
        self.test_dancefloor = DanceFloor([0, 0], 30, 30, 30)
        self.test_person.map = self.test_map
        self.test_person.rememberedObj = self.test_dancefloor
        self.test_person.move_inside_dance_floor()
        result = self.test_person.move(self.test_person.coordinates)
        self.assertTrue(result)

    def test_set_cords_from_algo_no_locations(self):
        self.test_person.map = self.test_map
        self.test_person.rememberedObj = self.test_dancefloor
        self.assertFalse(self.test_person.set_cords_from_algo())

    def test_flock_true(self):
        self.test_person_3 = person.Person("person 2", [115, 115], 10, 0, 0)
        self.test_person_4 = person.Person("person 2", [90, 90], 10, 0, 0)
        self.test_map.mapData.append(self.test_person_3)
        self.test_map.mapData.append(self.test_person_4)
        self.test_person.map = self.test_map
        self.assertIsNone(self.test_person.flock())

    def test_random_move(self):
        self.test_person.map = self.test_map
        result = self.test_person.random_move()
        self.assertNotEqual(self.test_person.get_coordinates(), result)
        return

    def test_get_state_action_move(self):
        self.test_person.currentState = "move"
        self.test_person.rememberedObj = self.test_dancefloor
        self.test_person.map = self.test_map
        self.test_person.get_state_action()
        return

    def test_get_state_action_order_drink(self):
        """Person has ordered drink, therefore true"""
        self.test_person.currentState = "orderDrink"
        self.test_person.rememberedObj = self.test_bar
        self.test_person.map = self.test_map
        result = self.test_person.get_state_action()
        self.assertTrue(result)
        return

    def test_get_state_action_use_toilet(self):
        """Person has ordered drink, therefore true"""
        self.test_person.currentState = "useToilet"
        self.test_person.rememberedObj = self.test_toilet
        self.test_person.map = self.test_map
        result = self.test_person.get_state_action()
        self.assertTrue(result)
        return

    def test_drink_drink(self):
        self.test_person.hasDrink = True
        result = self.test_person.drink_drink()
        self.assertTrue(result)
        return

    def test_calculate_move_direction_difference(self):
        self.test_person.lastCoordinates = [95, 95]
        result = self.test_person.calculate_move_direction_difference()
        self.assertEqual(result, [5, 5])

    def test_calculate_move_direction_difference_false(self):
        self.test_person.lastCoordinates = []
        result = self.test_person.calculate_move_direction_difference()
        self.assertFalse(result)

    def test_get_flocking_parameters(self):
        self.test_person.lastCoordinates = [95, 95]
        result = self.test_person.get_flocking_parameters()
        self.assertTrue(result)

    def test_flock(self):
        self.test_person_3 = person.Person("person 2", [115, 115], 10, 0, 0)
        self.test_bar = Bar([110, 110], 30, 30, 30)
        self.test_map.mapData.append(self.test_person_3)
        self.test_person.map = self.test_map
        self.test_person.flock()
        # print(self.test_person.map.get_people_within_range(self.test_person.coordinates,
        #                                                    self.test_person.flockingDistance, self))
        # print(self.test_person.map.get_objects_within_range(self.test_person.coordinates, self.test_person.get_rejection_area(),
        #                                                     self.test_person.get_edge_coordinates_array(self.test_person.coordinates,
        #                                                                                                                                                                      self.test_person.get_rejection_area()), self.test_person))

    def test_flock_move_positive(self):
        self.test_person.map = self.test_map
        test_x = {
            "positive": 1,
            "negative": 0
        }
        test_y = {
            "positive": 1,
            "negative": 0
        }
        test_avg_angle = 0
        self.test_person.flock_move(test_avg_angle, test_x, test_y)

    def test_flock_move_negavtive(self):
        self.test_person.map = self.test_map
        test_x = {
            "positive": 0,
            "negative": 1
        }
        test_y = {
            "positive": 0,
            "negative": 1
        }
        test_avg_angle = 0
        self.test_person.flock_move(test_avg_angle, test_x, test_y)

    def test_navigate_via_astar_positive(self):
        self.test_person.astarCoords = [[120, 120]]
        self.test_person.map = self.test_map
        self.assertIsNone(self.test_person.navigate_via_astar([0, 0]))

    def test_navigate_via_astar_negative(self):
        self.test_person.astarCoords = [[70, 70]]
        self.test_person.map = self.test_map
        self.assertIsNone(self.test_person.navigate_via_astar([0, 0]))

    def test_action(self):
        self.test_person_3 = person.Person("person 2", [115, 115], 10, 0, 0)
        self.test_bar = Bar([120, 120], 30, 30, 30)
        self.test_map.mapData.append(self.test_person_3)
        self.test_map.mapData.append(self.test_bar)
        self.test_map.set_size_screen(500, 500)
        self.test_map.generate_nodes()
        self.test_person.map = self.test_map
        self.test_person.action()


    def test_count_objects_in_vision_include_people(self):
        include = True
        test_bar = Bar([120, 120], 30, 30, 30)
        self.test_person.add_to_vision(test_bar)
        self.assertTrue(self.test_person.count_objects_in_vision(include))
        return

    def test_count_objects_in_vision(self):
        include = False
        test_bar = Bar([120, 120], 30, 30, 30)
        self.test_person.add_to_vision(test_bar)
        self.assertEqual(self.test_person.count_objects_in_vision(include), 1)
        return

    def test_flock_work(self):
        test_map_2 = map_data.map_data(Mock(), 0)
        test_map_2.clear_map()
        self.test_person_3 = Person("person 3", [115, 115], 10, 0, 0)
        test_map_2.mapData.append(self.test_person_3)
        test_map_2.add_people_to_map([130, 130], 10, 0)
        test_map_2.add_people_to_map([125, 105], 10, 0)
        self.test_person_3.map = test_map_2
        print(self.test_person_3.map.mapData)
        self.test_person_3.flock()

    def test_find_closest_coordinate_high(self):
        test_my_coord = 20
        test_low_coord = 10
        test_high_coord = 0
        result = self.test_person.find_closest_coordinate(test_my_coord, test_low_coord, test_high_coord)
        self.assertEqual(result, 0)

    def test_find_closest_coordinate(self):
        test_my_coord = 20
        test_low_coord = 10
        test_high_coord = 30
        result = self.test_person.find_closest_coordinate(test_my_coord, test_low_coord, test_high_coord)
        self.assertEqual(result, 20)

    def test_action_again(self):
        self.test_bar = Bar([110, 110], 30, 30, 30)
        self.test_map.mapData.append(self.test_bar)
        self.test_person.map = self.test_map
        self.test_person.action()

    def test_action_dance(self):
        test_dancefloor = DanceFloor([50, 50], 100, 100, 100)
        self.test_person.inside_dance_floor = True
        self.test_person.rememberedObj = test_dancefloor
        self.test_person.stateMachine.set_current_state("dance")
        self.test_bar = Bar([110, 110], 30, 30, 30)
        self.test_map.mapData.append(self.test_bar)
        self.test_person.map = self.test_map
        self.test_person.action()

    def test_navigate_to_remembered_object(self):
        test_dancefloor = DanceFloor([50, 50], 100, 100, 100)
        self.test_person.rememberedObj = test_dancefloor
        self.test_person.map = self.test_map
        self.test_person.navigate_to_remembered_object()



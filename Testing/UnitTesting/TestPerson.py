import unittest
from People import *
from People.person import Person
from Objects.bar import Bar
from Objects.wall import Wall
from Algorithm import a_starv2
import numpy
from Data import map_data


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.testPerson = person.Person("person 1", [100, 100], 10, 0, 0)
        self.testPerson2 = person.Person("person 2", [20, 30], 10, 0, 0)
        self.test_bar = Bar([450, 450], "Bar", 30, 20)
        self.testPerson2.add_to_memory(self.test_bar)

    def test_get_coordinates_for_move_avoiding_collision_object_true(self):
        """requires an object to avoid."""
        test_wall = Wall([100, 100], 500, 500)
        test_target = [0, 0]
        test_attempted = [700, 700]
        """This tests that the move can be done as there is no collision"""
        result = self.testPerson.get_coordinates_for_move_avoiding_collision_object(test_target, test_wall, test_attempted)
        self.assertEqual(result, test_attempted)

    def test_get_coordinates_for_move_avoiding_collision_object_false(self):
        """requires an object to avoid."""
        test_wall = Wall([100, 100], 601, 601)
        test_target = [0, 0]
        test_attempted = [100, 100]
        test_result = [701, 700]
        """This tests that the move can be done as there is no collision"""
        result = self.testPerson.get_coordinates_for_move_avoiding_collision_object(test_target, test_wall,
                                                                                    test_attempted)
        self.assertEqual(result, test_attempted)


    def test_person_rotate(self):
        """
        Tests if person rotates 30 degrees
        Start = 0
        Return 30
        :return: True as person has rotated 30 degrees
        """
        result = 30
        self.assertEqual(self.testPerson.person_rotate(), result)

    def test_change_angle_to_move_direction(self):
        """Does not require anything"""
        test_old_coords = [0, 0]
        test_new_coords = [1, 1]
        result = self.testPerson.change_angle_to_move_direction(test_old_coords, test_new_coords)
        """Checks to see if a move diagonal will be 135.5 degrees"""
        self.assertEqual(result, 135.0)

    def test_get_angle_between_coords(self):
        test_old_coords = [0, 0]
        test_new_coords = [200, 186]
        """Tests to see if there is an angle change. The result will be a float but used assertEqual
        to find the closest whole number."""
        result = self.testPerson.get_angle_between_coords(test_old_coords, test_new_coords)
        self.assertAlmostEqual(result, 137, 0)

    def test_get_angle_between_coords_x0(self):
        test_old_coords = [0, 0]
        test_new_coords = [0, 186]
        """Tests to see if there is an angle change. The result will be a float but used assertEqual
        to find the closest whole number."""
        result = self.testPerson.get_angle_between_coords(test_old_coords, test_new_coords)
        self.assertAlmostEqual(result, 90, 0)

    def test_get_angle_between_coords_y0(self):
        test_old_coords = [0, 0]
        test_new_coords = [200, 0]
        """Tests to see if there is an angle change. The result will be a float but used assertEqual
        to find the closest whole number."""
        result = self.testPerson.get_angle_between_coords(test_old_coords, test_new_coords)
        self.assertAlmostEqual(result, 180, 0)

    def test_get_angle_between_coords_no_angle_change(self):
        test_old_coords = [0, 0]
        test_new_coords = [0, 0]
        """Tests to see if there is no angle change"""
        result = self.testPerson.get_angle_between_coords(test_old_coords, test_new_coords)
        self.assertFalse(result)

    def test_get_rejection_area(self):
        """Width is currently 10"""
        self.testPerson.width = 10
        self.testPerson.rejectionArea = 10
        result = self.testPerson.get_rejection_area()
        self.assertEqual(result, 15)

    def test_get_rejection_area_with_float(self):
        """check rejection area with a float as the two integers."""
        self.testPerson.width = 10.89
        self.testPerson.rejectionArea = 10.4
        result = self.testPerson.get_rejection_area()
        self.assertAlmostEqual(result, 16, 0)

    def test_get_state_action(self):
        """Current State is none and therfroe willl be moving randomly"""
        result = self.testPerson.get_state_action()
        self.assertEqual(result, "moveRandom")

    def test_get_state_action_different_state(self):
        """Current State is want and therfroe willl be rotating"""
        self.testPerson.currentState = "want"
        result = self.testPerson.get_state_action()
        self.assertEqual(result, "rotate")

    def test_find_action(self):
        self.testPerson.rememberedObjType = "Bar"
        result = self.testPerson.find_action()
        self.assertEqual(result, "rotate")

    def test_find_action_beyond_rotate(self):
        self.testPerson.rotate = 12
        self.testPerson.rememberedObjType = "Bar"
        result = self.testPerson.find_action()
        self.assertEqual(result, "explore")

    def test_want_action_false(self):
        """searchObject is Bar, However, we have not discovered it and therefore
        returns false."""
        test_want_state = "wantDrink"
        result = self.testPerson.want_action(test_want_state)
        self.assertFalse(result)

    def test_want_action_true(self):
        """searchObject is Bar, However, we have not discovered it and therefore
        returns false."""
        test_want_state = "wantDrink"
        result = self.testPerson2.want_action(test_want_state)
        self.assertTrue(result)

    def test_find_object(self):
        """No memory, returns False"""
        result = self.testPerson.find_object("Bar")
        self.assertFalse(result)

    def test_find_object_true(self):
        """Memory, returns True"""
        """Using person2 as they have a memory of the bar."""
        result = self.testPerson2.find_object("Bar")
        self.assertTrue(result)

    def test_clear_remembered_object(self):
        """Should empty the values we have declared"""
        self.testPerson.clear_remembered_object()
        result = self.testPerson.rememberedObj
        self.assertEqual(result, "")
        result = self.testPerson.rememberedObjType
        self.assertEqual(result, "")
        result = self.testPerson.rememberedColour
        self.assertEqual(result, "")
        result = self.testPerson.rememberedCoords
        self.assertEqual(result, [])


    def test_get_edge_coordinates_array(self):
        """
        Tests to see if the edge coordinates get printed
        :return:
        """
        data = [101, 101]
        result = self.testPerson.get_edge_coordinates_array(data, 20)
        self.assertTrue(result)

    def test_advance_state_machine(self):
        """The greatest need is the current state, which allows a selection of wants"""
        print(self.testPerson.stateMachine.get_current_state())
        result = self.testPerson.advance_state_machine()
        self.assertTrue(result)

    def test_object_in_vision_false(self):
        """Bar is not in vision and therefore false."""
        new_bar = Bar([450, 450], "Bar 2", 30, 20)
        result = self.testPerson.object_in_vision(new_bar)
        self.assertFalse(result)

    def test_object_in_vision_true(self):
        """Bar is not in vision and therefore True.
        qualifier adds the bar to the vision."""
        new_bar = Bar([0, 0], "Bar 2", 100, 50)
        qualifier = self.testPerson.add_to_vision(new_bar)
        result = self.testPerson.object_in_vision(new_bar)
        self.assertTrue(result)

    def test_add_to_memory_true(self):
        """Instance of a bar, dancefloor or toilet"""
        new_bar = Bar([0, 0], "Bar 2", 100, 50)
        result = self.testPerson.add_to_memory(new_bar)
        self.assertTrue(result)

    def test_add_to_memory_false(self):
        """Instance of a toilet, should return False"""
        new_wall = Wall([0, 0], 100, 50)
        result = self.testPerson.add_to_memory(new_wall)
        self.assertFalse(result)

    def test_add_to_memory_alread_known_object(self):
        """Should return none, as bar has already been added to memory"""
        new_bar = Bar([0, 0], "Bar 2", 100, 50)
        self.testPerson.add_to_memory(new_bar)
        result2 = self.testPerson.add_to_memory(new_bar)
        self.assertEqual(result2, None)

    def test_check_obj_already_known_true(self):
        """Need an object and its type"""
        new_bar = Bar([0, 0], "Bar 2", 100, 50)
        """Adding the memory to the bar using the add_to_bar function"""
        self.testPerson.add_to_memory(new_bar)
        """True as the bar is added and object is already known"""
        result = self.testPerson.check_obj_already_known(new_bar, "Bar")
        self.assertTrue(result)

    def test_check_obj_already_known_false(self):
        """Need an object and its type"""
        new_bar = Bar([0, 0], "Bar 2", 100, 50)
        result = self.testPerson.check_obj_already_known(new_bar, "Bar")
        self.assertFalse(result)

    def test_get_closes_object_from_memory_false(self):
        result = self.testPerson.get_closest_object_from_memory("Bar")
        self.assertFalse(result)
        return


    def test_person_vision(self):
        """Tests if a person vision exists"""
        sight = self.testPerson.get_sight()
        angle = self.testPerson.get_angle()
        coords = self.testPerson.get_coordinates()
        result = self.testPerson.personVision(coords[0], coords[1], angle, sight)
        self.assertTrue(result)

    def test_person_vision_false(self):
        """Tests if a cordinate outside the vision is inside the vision."""
        sight = self.testPerson.get_sight()
        angle = self.testPerson.get_angle()
        coords = self.testPerson.get_coordinates()
        result = self.testPerson.personVision(coords[0], coords[1], angle, sight)
        self.assertNotIn([100, 100], result)

    def test_angle_math(self):
        """As the angle has been set to 180, it should return a change of 10 to the X coord"""
        angle = 180
        coords = self.testPerson.get_coordinates()
        width = self.testPerson.get_width()
        result = self.testPerson.angleMath(angle, coords[0], coords[1], width)
        self.assertEqual(result, [10, 0])

    def test_has_ordered_drink(self):
        self.testPerson.orderedDrink = 1
        result = self.testPerson.has_ordered_drink()
        self.assertTrue(result)

    def test_set_action_count(self):
        self.testPerson.tick_rate = 1
        test_min = 3
        test_max = 10
        result = self.testPerson.set_action_count(test_min, test_max)
        self.assertTrue(result)

    def test_set_action_count_0(self):
        test_min = 3
        test_max = 10
        test_max = 10
        result = self.testPerson.set_action_count(test_min, test_max)
        self.assertEqual(result, 0)

    def test_wait_on_action_count_true(self):
        """Action count isgreater than currentaction count and should therefore return True."""
        self.testPerson.actionCount = 5
        self.testPerson.currentActionCount = 1
        result = self.testPerson.wait_on_action_count()
        self.assertTrue(result)


    def test_wait_on_action_count_false(self):
        """Action count and currentAction Counr is None and should return False."""
        result = self.testPerson.wait_on_action_count()
        self.assertFalse(result)

    def test_store_waypoints(self):
        """
        Tests the store waypoints function appends to the cords variable in order for a* to trigger
        """
        data = [0, 450]
        self.testPerson.store_waypoints(data)
        self.assertListEqual(self.testPerson.coordinates, [100, 100])

    def test_find_nearest_waypoint(self):
        result = self.testPerson2.find_nearest_waypoint()
        self.assertEqual(result, [20, 40])

    def test_check_needs_false(self):
        result = self.testPerson.check_needs()
        self.assertFalse(result)

    def test_check_needs_true_0(self):
        """Assign a value of below 0"""
        self.testPerson.brain[1][1] = 0
        result = self.testPerson.check_needs()
        self.assertTrue(result)

    def test_check_needs_true_1(self):
        """Assign a value of below 0"""
        self.testPerson.brain[1][1] = 1
        result = self.testPerson.check_needs()
        self.assertTrue(result)

    def test_check_needs_false_2(self):
        """Assign a value of below 0"""
        self.testPerson.brain[1][1] = 3
        result = self.testPerson.check_needs()
        self.assertFalse(result)


    def test_check_person_collided_with_target_false(self):
        """Person and Bar and nowhere near"""
        new_bar = Bar([450, 450], "Bar 2", 30, 20)
        result = self.testPerson.check_person_collided_with_target(new_bar)
        self.assertFalse(result)

    def test_check_person_collided_with_target_true(self):
        """Bar and Person are collided, target destination"""
        new_bar = Bar([450, 450], "Bar 2", 30, 20)
        new_person = person.Person("person 2", [450, 450], 10, 0, 0)
        new_person.rememberedObj = new_bar
        result = new_person.check_person_collided_with_target(new_bar)
        self.assertTrue(result)

    def test_increment_need(self):
        test_index = 1
        test_increment = 1000
        self.testPerson.increment_need(test_index, test_increment)
        end_result = self.testPerson.brain[test_index][1]
        self.assertEqual(end_result, 100)

    def test_check_astar_cords_is_empty_true(self):
        result = self.testPerson.check_astar_cords_is_empty()
        self.assertEqual(result, False)

    def test_check_astar_cords_is_empty_false(self):
        self.testPerson.astarCoords = [100, 100]
        result = self.testPerson.check_astar_cords_is_empty()
        self.assertFalse(result)

    def test_clear_explore_node(self):
        self.testPerson.exploreNode = [100, 100]
        self.testPerson.astarCoords = [100, 100]
        self.testPerson.clear_explore_node()
        test_result = self.testPerson.exploreNode
        test_result_2 = self.testPerson.astarCoords
        self.assertEqual(test_result, [])
        self.assertEqual(test_result_2, [])


    def test_increment_need_set_to_0(self):
        test_index = 1
        test_increment = -100
        self.testPerson.increment_need(test_index, test_increment)
        end_result = self.testPerson.brain[test_index][1]
        self.assertEqual(end_result, 0)

    def test_advance_state_machine_currently_greatest_need(self):
        result = self.testPerson.stateMachine.get_current_state()
        self.assertEqual(result, self.testPerson.stateMachine.get_current_state())

    def test_advance_state_machine_currently_want(self):
        self.testPerson.stateMachine.set_current_state("findToilet")
        self.testPerson.advance_state_machine()
        result = self.testPerson.stateMachine.get_current_state()
        self.assertEqual(result, "moveToToilet")

    def test_advance_state_machine_currently_move(self):
        self.testPerson.stateMachine.set_current_state("moveToToilet")
        self.testPerson.advance_state_machine()
        result = self.testPerson.stateMachine.get_current_state()
        self.assertEqual(result, "useToilet")

    def test_person_eyes(self):
        test_coords = self.testPerson.get_coordinates()
        test_angle = 0
        test_radius = self.testPerson.get_width()
        result = self.testPerson.person_eyes(test_coords, test_angle, round(test_radius / 2))
        self.assertEqual(result, [[98, 99], [98, 101]])
        return

if __name__ == '__main__':
    unittest.main()
import unittest
from Objects import toilet
from People import person


class TestToilet(unittest.TestCase):

    def setUp(self):
        self.test_toilet = toilet.Toilet([200, 200], "toilet", 200, 100)
        """Used to test the use of the toilets within the class."""
        self.test_person = person.Person("person", [20, 30], 10, 0, 0)
        self.test_person_2 = person.Person("person 2", [20, 30], 10, 0, 0)

    def test_person_use_toilet(self):
        """Return True, as the toilet is free for use."""
        self.assertTrue(self.test_toilet.person_use_toilet(self.test_person))

        self.assertTrue(self.test_toilet.person_use_toilet("person"))

    def test_person_is_using_toilet(self):
        """Test for the function person_stop_using_toilet
        Pre-requisite: test_person is currently at the toilet.
        :return: True. As with the test above, the person is using toilet.
        """
        self.test_toilet.person_use_toilet(self.test_person)
        self.assertTrue(self.test_toilet.person_stop_using_toilet(self.test_person))

    def test_person_not_using_toilet(self):
        """Test for the function test_person_stop_using_toilet 
        :return: False. This person is not currently using the toilet.
        """
        self.assertFalse(self.test_toilet.person_stop_using_toilet(self.test_person_2))

    def test_check_person_using_toilet(self):
        """Test for the function check_person_using_toilet
        Pre-requisite: test_person is currently at the toilet.
        :return: True. As with the test above, the person is on the toilet.
        """
        self.test_toilet.person_use_toilet(self.test_person)
        self.assertTrue(self.test_toilet.check_person_using_toilet(self.test_person))

    def test_check_person_using_toilet_is_false(self):
        """Person Instance is a string, and should return false as this is not in the array
        :return: False.
        """
        self.assertFalse(self.test_toilet.check_person_using_toilet("person"))

    def test_auto_max_users_size(self):
        """This will test the amount of toilet spaces available.
        Current Height is set to 100, so should create 5 spaces."""
        result = 5
        self.assertEqual(self.test_toilet.auto_set_max_users_size(self.test_toilet.get_height()), result)
        """This will test the amount of toilet spaces available.
                Current Height is set to 200, so should create 10 spaces."""
        result = 10
        self.assertEqual(self.test_toilet.auto_set_max_users_size(self.test_toilet.get_width()), result)

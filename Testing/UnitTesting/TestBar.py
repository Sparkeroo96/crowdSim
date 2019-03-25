from Objects import bar
from People import person
import unittest


class TestBar(unittest.TestCase):
    def setUp(self):
        self.test_bar = bar.Bar([200, 200], "test", 200, 500)
        return

    def test_serve_drink_drinksQueue_empty(self):
        result = self.test_bar.serve_drink()
        self.assertEqual(result, 0)


    def test_serve_drink_drinksQueue_contains(self):
        test_person = person.Person("person 1", [100, 100], 10, 0, 0)
        self.test_bar.drinksQueue = [test_person]
        result = self.test_bar.serve_drink()
        self.assertEqual(result, 1)

    def test_decrease_wait_timers(self):
        self.test_bar.wait_timers = [10]
        self.test_bar.decrease_wait_timers()
        test_return = self.test_bar.wait_timers
        self.assertTrue(test_return)


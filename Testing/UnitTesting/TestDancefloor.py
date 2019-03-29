import unittest
from Objects import danceFloor

class TestDanceFloor(unittest.TestCase):
    def setUp(self):
        self.test_dance_floor = danceFloor.DanceFloor([200, 200], "test", 200, 500)
        return

    def test_get_dancefloor_area(self):
        """Tests getting the dancefloor area
        :return: True
        """
        self.assertTrue(self.test_dance_floor.get_dancefloor_area())

    def test_get_random_dance_area(self):
        self.assertTrue(self.test_dance_floor.get_random_dance_area())

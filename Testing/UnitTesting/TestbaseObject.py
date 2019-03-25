from Objects import baseObject
import unittest


class TestBaseObject(unittest.TestCase):
    def setUp(self):
        self.test_base = baseObject.BaseObject([100, 100], "test_base", 20, 20)
        return

    def test_get_details(self):
        test_coords = self.test_base.get_coordinates()
        test_name = self.test_base.get_name()
        test_width = self.test_base.get_width()
        test_height = self.test_base.get_height()
        result = self.test_base.get_details()
        self.assertTrue(result)

    def test_get_coordinates(self):
        test_coords = self.test_base.get_coordinates()
        result = self.test_base.get_coordinates()
        self.assertEqual(result, test_coords)

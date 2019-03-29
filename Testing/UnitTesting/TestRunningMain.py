import unittest
from test import RunningMain
import pygame

class TestRunningMain(unittest.TestCase):
    def setUp(self):
        self.test = RunningMain()
        self.test.draw_display()
        return
    def test(self):
        self.assertTrue(True)
        return


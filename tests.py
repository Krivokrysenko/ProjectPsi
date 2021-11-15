import unittest
import Nona

class test(unittest.TestCase):

    def test_basic(self):
        Nona.loadAgent("alarm", ".AlArm")
        actual = Nona.acceptInput("alarm 7 min")
        expected = "time: 7\n unit: min"
        self.assertEqual(actual, expected)
        Nona.unloadAgent("alarm")
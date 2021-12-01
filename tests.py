import unittest
import Nona

class test(unittest.TestCase):

    def test_basic(self):
        Nona.loadAgent("alarm", ".AlArm")
        actual = Nona.acceptInput("alarm 7 min")
        expected = "time: 7\n unit: min"
        self.assertEqual(actual, expected)
        Nona.unloadAgent("alarm")

    def test_keywords(self):
        Nona.loadAgent("alarm", ".AlArm")
        actual = Nona.agentKeywords
        expected = {'alarm': ["alarm", "set an alarm", "remind me at"]}
        self.assertEqual(actual, expected)
        Nona.unloadAgent("alarm")
        self.assertEqual(Nona.loadedmods, {})
        self.assertEqual(Nona.instclasses, {})
        self.assertEqual(Nona.agentKeywords, {})
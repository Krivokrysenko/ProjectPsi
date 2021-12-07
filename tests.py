import unittest
import Nona

class test(unittest.TestCase):

    def test_basic(self):
        Nona.loadAgent("alarm", ".AlArm")
        Nona.loadAgent("timer", ".Timer")
        actual = Nona.acceptInput("alarm 7 min")
        expected = "time: 7\n unit: min"
        self.assertEqual(actual, expected)
        actual = Nona.acceptInput("timer 3")
        expected = "beep beep beep"
        self.assertEqual(actual, expected)
        Nona.unloadAgent("alarm")
        Nona.unloadAgent("timer")

    def test_keywords(self):
        Nona.loadAgent("alarm", ".AlArm")
        self.assertTrue(Nona.agentKeywords["alarm"][0] == "alarm")
        self.assertTrue(Nona.agentKeywords["alarm"][1] == "set an alarm")
        self.assertTrue(Nona.agentKeywords["alarm"][2] == "remind me at")
        Nona.unloadAgent("alarm")
        self.assertEqual(Nona.loadedmods, {})
        self.assertEqual(Nona.instclasses, {})
        self.assertEqual(Nona.agentKeywords, {})

    def test_addKeyword(self):
        Nona.loadAgent("alarm", ".AlArm")
        previous = Nona.agentKeywords["alarm"]
        Nona.addKeyword("alarm", "al arm")
        actual = Nona.agentKeywords["alarm"]
        expected = previous + ["al arm"]
        self.assertEqual(actual, expected)
        Nona.unloadAgent("alarm")

    def test_addKeyword2(self):
        Nona.loadAgent("timer", ".Timer")
        Nona.addKeyword("timer", "set a timer")
        Nona.unloadAgent("timer")
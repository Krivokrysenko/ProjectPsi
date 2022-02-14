import unittest
import Nona
import time

class test(unittest.TestCase):

    def test_basic(self):
        NonaObj = Nona.NonaClass()
        NonaObj.loadAgent("alarm", ".AlArm")
        NonaObj.loadAgent("timer", ".Timer")
        actual = NonaObj.acceptInput("alarm 7 min")
        expected = "time: 7\n unit: min"
        self.assertEqual(actual, expected)
        actual = NonaObj.acceptInput("timer 3")
        expected = "beep beep beep"
        self.assertEqual(actual, expected)
        NonaObj.unloadAgent("alarm")
        NonaObj.unloadAgent("timer")

    def test_keywords(self):
        NonaObj = Nona.NonaClass()
        NonaObj.loadAgent("alarm", ".AlArm")
        self.assertTrue(Nona.agentKeywords["alarm"][0] == "alarm")
        self.assertTrue(Nona.agentKeywords["alarm"][1] == "set an alarm")
        self.assertTrue(Nona.agentKeywords["alarm"][2] == "remind me at")
        NonaObj.unloadAgent("alarm")
        self.assertEqual(Nona.loadedmods, {})
        self.assertEqual(Nona.instclasses, {})
        self.assertEqual(Nona.agentKeywords, {})

    def test_addKeyword(self):
        NonaObj = Nona.NonaClass()
        NonaObj.loadAgent("alarm", ".AlArm")
        previous = Nona.agentKeywords["alarm"]
        NonaObj.addKeyword("alarm", "al arm")
        actual = Nona.agentKeywords["alarm"]
        expected = previous + ["al arm"]
        self.assertEqual(actual, expected)
        NonaObj.unloadAgent("alarm")

    def test_addKeyword2(self):
        Nonaobj = Nona.NonaClass()
        Nonaobj.loadAgent("timer", ".Timer")
        Nonaobj.addKeyword("timer", "set a timer")
        Nonaobj.unloadAgent("timer")

    def test_requestFromUser(self):
        NonaObj = Nona.NonaClass()
        NonaObj.loadAgent("timer", ".Timer")
        NonaObj.acceptInput("timer 4")
        NonaObj.acceptInput("timer 2")
        time.sleep(7)
        NonaObj.unloadAgent("timer")